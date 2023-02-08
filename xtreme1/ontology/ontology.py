import json
from io import BytesIO
from typing import List, Optional

from .node import _check_dup, ImageRootNode, LidarBasicRootNode, LidarFusionRootNode, INDENT


class Ontology:
    __slots__ = ['classes', 'classifications', 'des_id', 'des_type', 'dataset_type', 'name', '_client']

    def __init__(
            self,
            client,
            des_type: str,
            des_id: str,
            dataset_type: str,
            classes: Optional[List] = None,
            classifications: Optional[List] = None,
    ):
        self.des_id = des_id
        self._client = client
        self.des_type = des_type
        self.dataset_type = dataset_type.upper()
        self.classes = []
        self.classifications = []
        if classes is None:
            classes = []
        if classifications is None:
            classifications = []
        for c in classes:
            new_class = DATASET_DICT[self.dataset_type].to_node(
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
        return f'<{self.__class__.__name__}> The ontology of {self.des_type} {self.des_id}'

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

        new_class = DATASET_DICT[self.dataset_type](
            name=name,
            **kwargs
        )

        self.classes.append(new_class)

        return new_class

    def delete_online_ontology(
            self
    ):
        return self._client.delete_ontology(
            des_id=self.des_id
        )

    def delete_online_rootnode(
            self,
            root_node
    ):
        if root_node.onto_type == 'class':
            self.classes.remove(root_node)
            part1 = 'datasetClass' if 'dataset' in self.des_type else 'class'
        else:
            self.classifications.remove(root_node)
            part1 = 'datasetClassification' if 'dataset' in self.des_type else 'classification'

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

        if 'ontology' in self.des_type:
            endpoint = f'{onto_type}/update/{node_id}'
            onto_dict['ontologyId'] = self.des_id
        else:
            endpoint = f'dataset{onto_type.capitalize()}/update/{node_id}'
            onto_dict['datasetId'] = self.des_id

        resp = self._client.api.post_request(
            endpoint=endpoint,
            payload=onto_dict

        )

        return resp

    def _import_ontology(
            self
    ):
        endpoint = 'ontology/importByJson'

        data = {
            'desType': self.des_type.upper(),
            'desId': self.des_id
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
            self
    ):
        existing_onto = self._client.query_ontology(
            des_id=self.des_id,
            des_type=self.des_type
        )

        existing_class_ids = [x.id for x in existing_onto.classes]
        existing_classification_ids = [x.id for x in existing_onto.classifications]

        dup_classes = []
        cur_classes = self.classes
        for i in range(-len(cur_classes), 0):
            if cur_classes[i].id in existing_class_ids:
                dup_classes.append(cur_classes.pop(i))

        dup_classifications = []
        cur_classifications = self.classifications
        for i in range(-len(cur_classifications), 0):
            if cur_classifications[i].id in existing_classification_ids:
                dup_classifications.append(cur_classifications.pop(i))

        return dup_classes, dup_classifications

    def import_ontology(
            self,
            replace=False
    ):
        dup_classes, dup_classifications = self._split_dup_nodes()

        self._import_ontology()

        if replace:
            for c in dup_classes:
                self.update_online_rootnode(c)
            for cf in dup_classifications:
                self.update_online_rootnode(cf)

        return True


DATASET_DICT = {
    'IMAGE': ImageRootNode,
    'LIDAR_BASIC': LidarBasicRootNode,
    'LIDAR_FUSION': LidarFusionRootNode
}
