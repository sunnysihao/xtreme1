import json
from io import BytesIO
from typing import List, Dict, Optional
from copy import deepcopy

from .node import _check_dup, RootNode, ImageRootNode, LidarBasicRootNode, LidarFusionRootNode, INDENT


class Ontology:
    __slots__ = ['_client', '_des_id', '_des_type', '_dataset_type', 'classes', 'classifications']

    def __init__(
            self,
            client,
            des_type: str,
            des_id: int,
            dataset_type: str,
            classes: Optional[List] = None,
            classifications: Optional[List] = None,
    ):
        self._client = client
        self._des_id = des_id
        self._des_type = des_type
        self._dataset_type = dataset_type.upper()
        self.classes = []
        self.classifications = []
        if classes is None:
            classes = []
        if classifications is None:
            classifications = []
        for c in classes:
            if type(c) == dict:
                new_class = DATASET_DICT[self._dataset_type].to_node(
                    org_dict=c,
                )
                self.classes.append(new_class)
            elif isinstance(c, RootNode):
                self.classes.append(c)
        # for cf in classifications:
        #     new_classification = DATASET_DICT[self.dataset_type].to_node(
        #                 org_dict=cf,
        #     )
        #     self.classifications.append(new_classification)

    def __repr__(
            self
    ):
        return f'<{self.__class__.__name__}> The ontology of {self._des_type} {self._des_id}'

    def __str__(
            self
    ):
        self_intro = {
            'classes': [f'<{n.__class__.__name__}> {n.name}' for n in self.classes],
            'classifications': [f'<{n.__class__.__name__}> {n.name}' for n in self.classifications],
        }
        self_intro = json.dumps(self_intro, indent=' ' * INDENT)

        return f"<{self.__class__.__name__}>\n{self_intro}"

    def to_dict(
            self
    ) -> Dict:
        """
        Turn this `Ontology` object into a `dict`.

        Returns
        -------
        Dict
            A standard `dict` of ontology.
        """
        result = {
            'classes': [c.to_dict() for c in self.classes],
            'classifications': [cf.to_dict() for cf in self.classifications]
        }

        return result

    def add_class(
            self,
            name,
            **kwargs
    ):
        """
        Add an `RootNode` object to the classes of an `Ontology` object.

        Parameters
        ----------
        name: str
            The name of a new class.
        kwargs:
            The args needed to create a `RootNode`. For example:
            ImageRootNode needs `name`, `tool_type` and `color`
            If you forget to pass a parameter such as `color`,
            it's also an option to edit it after the `RootNode` is created.

        Returns
        -------
        RootNode
            The new `RootNode`.
            Notice that it's already in its parent node.
        """
        _check_dup(
            nodes=self.classes,
            new_name=name
        )

        new_class = DATASET_DICT[self._dataset_type](
            name=name,
            **kwargs
        )

        self.classes.append(new_class)

        return new_class

    def copy(
            self
    ):
        """
        Generate a copy of current `Ontology` object, which can be used to import to another ontology.

        Returns
        -------
        Ontology
            A copy of current `Ontology` object.
        """
        new_onto = SampleOntology(
            des_type=self._des_type,
            des_id=self._des_id,
            classes=[c.copy() for c in self.classes],
            classifications=[cf.copy() for cf in self.classifications]
        )

        return new_onto

    def delete_online_ontology(
            self,
            is_sure: bool = False
    ) -> bool:
        """
        Delete the ontology in your online 'ontology center'.
        Notice that an ontology attached to a dataset can not be deleted.

        Parameters
        ----------
        is_sure: bool, default False
            Sure or not sure to delete this ontology.

        Returns
        -------
        bool
            True: delete complete.
            False: user is not sure to delete the ontology or the ontology is already deleted.
        """
        return self._client.delete_ontology(
            des_id=self._des_id,
            is_sure=is_sure
        )

    def delete_online_rootnode(
            self,
            root_node: RootNode,
            is_sure: bool = False
    ):
        """
        Delete a class/classification in your online ontology.

        Parameters
        ----------
        root_node: RootNode
            A `RootNode` object.
        is_sure: bool, default False
            Sure or not sure to delete this dataset.

        Returns
        -------
        bool
            True: delete complete.
            False: user is not sure to delete the `RootNode` or the `RootNode` is already deleted.
        """
        if is_sure:
            try:
                if root_node.onto_type == 'class':
                    self.classes.remove(root_node)
                    part1 = 'datasetClass' if 'dataset' in self._des_type else 'class'
                else:
                    self.classifications.remove(root_node)
                    part1 = 'datasetClassification' if 'dataset' in self._des_type else 'classification'
            except ValueError:
                return False

            endpoint = f'{part1}/delete/{root_node.id}'
            resp = self._client.api.post_request(
                endpoint=endpoint
            )

            return resp

        return False

    def update_online_rootnode(
            self,
            root_node: RootNode
    ) -> True:
        """
        Overwrite an online class/classification.

        Parameters
        ----------
        root_node: RootNode
            A `RootNode` object.

        Returns
        -------
        True
            True: update complete.
        """
        onto_dict = root_node.to_dict()
        onto_type = root_node.onto_type
        node_id = root_node.id

        if 'ontology' in self._des_type:
            endpoint = f'{onto_type}/update/{node_id}'
            onto_dict['ontologyId'] = self._des_id
        else:
            endpoint = f'dataset{onto_type.capitalize()}/update/{node_id}'
            onto_dict['datasetId'] = self._des_id

        self._client.api.post_request(
            endpoint=endpoint,
            payload=onto_dict
        )

        return True

    def _import_ontology(
            self
    ):
        endpoint = 'ontology/importByJson'

        data = {
            'desType': self._des_type.upper(),
            'desId': self._des_id
        }

        file = BytesIO(json.dumps(self.to_dict()).encode())
        files = {
            'file': ('ontology.json', file)
        }

        return self._client.api.post_request(
            endpoint=endpoint,
            data=data,
            files=files
        )

    def _split_dup_nodes(
            self,
    ):
        existing_onto = self._client.query_ontology(
            des_id=self._des_id,
            des_type=self._des_type
        )

        existing_class_ids = [x.id for x in existing_onto.classes]
        existing_classification_ids = [x.id for x in existing_onto.classifications]

        dup_classes = []
        cur_classes = deepcopy(self.classes)
        for i in range(-len(cur_classes), 0):
            if cur_classes[i].id in existing_class_ids:
                dup_classes.append(cur_classes.pop(i))

        dup_classifications = []
        cur_classifications = deepcopy(self.classifications)
        for i in range(-len(cur_classifications), 0):
            if cur_classifications[i].id in existing_classification_ids:
                dup_classifications.append(cur_classifications.pop(i))

        return cur_classes, cur_classifications, dup_classes, dup_classifications

    def import_ontology(
            self,
            ontology=None,
            replace=False
    ):
        """
        Import this `Ontology` object to your online dataset or ontology center.

        Parameters
        ----------
        ontology: SampleOntology
            A `SampleOntology` object generated by `copy()` method.
        replace: bool, default False
            Whether overwrite the online class/classification if `id` is duplicate.
        Returns
        -------
        bool
            True: import complete.
        """
        if ontology:
            ontology._des_id = self._des_id
            ontology._des_type = self._des_type
            ontology._dataset_type = self._dataset_type
            ontology._client = self._client
            cur_onto = ontology
        else:
            cur_onto = self

        no_dup_classes, no_dup_classifications, dup_classes, dup_classifications = cur_onto._split_dup_nodes()
        new_onto = deepcopy(cur_onto)
        new_onto.classes = no_dup_classes
        new_onto.classifications = no_dup_classifications
        new_onto._import_ontology()

        if replace:
            for c in dup_classes:
                cur_onto.update_online_rootnode(c)
            for cf in dup_classifications:
                cur_onto.update_online_rootnode(cf)

        return True


class SampleOntology(Ontology):
    def __init__(
            self,
            des_type,
            des_id,
            classes: Optional[List] = None,
            classifications: Optional[List] = None,
    ):
        super().__init__(
            client=None,
            des_type=des_type,
            des_id=des_id,
            dataset_type='',
            classes=classes,
            classifications=classifications
        )

    def __repr__(
            self
    ):
        return f'<{self.__class__.__name__}> The ontology copy of {self._des_type} {self._des_id}'


DATASET_DICT = {
    'IMAGE': ImageRootNode,
    'LIDAR_BASIC': LidarBasicRootNode,
    'LIDAR_FUSION': LidarFusionRootNode
}
