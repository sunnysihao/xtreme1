import json
from io import BytesIO
from typing import List, Optional
from copy import deepcopy

from .node import _check_dup, ImageRootNode, LidarBasicRootNode, LidarFusionRootNode, INDENT


class Ontology:
    __slots__ = ['classes', 'classifications', '_des_id', '_des_type', '_dataset_type', 'name', '_client']

    def __init__(
            self,
            client,
            des_type: str,
            des_id: str,
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
            new_class = DATASET_DICT[self._dataset_type].to_node(
                org_dict=c,
            )
            self.classes.append(new_class)
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
    ):
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

    def copy(self):
        new_onto = Ontology(
            client=None,
            des_type='',
            des_id='',
            dataset_type='',
            classes=[],
            classifications=[]
        )

        for c in self.classes:
            new_onto.classes.append(c.copy())
        for cf in self.classifications:
            new_onto.classifications.append(cf.copy())

        return new_onto

    def delete_online_ontology(
            self
    ):
        return self._client.delete_ontology(
            des_id=self._des_id
        )

    def delete_online_rootnode(
            self,
            root_node
    ):
        if root_node.onto_type == 'class':
            self.classes.remove(root_node)
            part1 = 'datasetClass' if 'dataset' in self._des_type else 'class'
        else:
            self.classifications.remove(root_node)
            part1 = 'datasetClassification' if 'dataset' in self._des_type else 'classification'

        endpoint = f'{part1}/delete/{root_node.id}'
        resp = self._client.api.post_request(
            endpoint=endpoint
        )

        return resp

    def update_online_rootnode(
            self,
            root_node
    ):
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

        return 'Success'

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

        return 'Success'


DATASET_DICT = {
    'IMAGE': ImageRootNode,
    'LIDAR_BASIC': LidarBasicRootNode,
    'LIDAR_FUSION': LidarFusionRootNode
}
