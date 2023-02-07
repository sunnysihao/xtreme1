import json
from typing import List, Optional

from .node import ImageRootNode, LidarBasicRootNode, LidarFusionRootNode, INDENT


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

    @staticmethod
    def _get(
            nodes,
            target
    ):
        for node in nodes:
            if node.name == target:
                return node

    def get_class(
            self,
            name
    ):
        return self._get(
            nodes=self.classes,
            target=name
        )

    def get_classification(
            self,
            name
    ):
        return self._get(
            nodes=self.classifications,
            target=name
        )

    def delete_online_ontology(
            self
    ):
        return self._client.delete_ontology(
            des_id=self.des_id
        )

    def delete_online_class(
            self,
            name
    ):
        target_node = self.get_class(name)
        if not target_node:
            return False

        self.classes.remove(target_node)

        part1 = 'datasetClass' if 'dataset' in self.des_type else 'class'
        endpoint = f'{part1}/delete/{target_node.id}'

        self._client.api.post_request(
            endpoint=endpoint
        )

    def delete_online_classification(
            self,
            name
    ):
        target_node = self.get_classification(name)
        if not target_node:
            return False

        self.classifications.remove(target_node)

        part1 = 'datasetClassification' if 'dataset' in self.des_type else 'classification'
        endpoint = f'{part1}/delete/{target_node.id}'

        self._client.api.post_request(
            endpoint=endpoint
        )

    def add_class(
            self,
            name,
            **kwargs
    ):
        new_class = DATASET_DICT[self.dataset_type](
            name=name,
            client=self._client,
            **kwargs
        )

        self.classes.append(new_class)

        return new_class


# def import_ontology(
#         self,
#         onto,
#         des_id: str,
#         des_type: str = 'dataset',
# ):
#     endpoint = 'ontology/importByJson'
#
#     data = {
#         'desType': des_type.upper(),
#         'desId': des_id
#     }
#
#     file = BytesIO(json.dumps(onto.to_dict()).encode())
#     files = {
#         'file': ('ontology.json', file)
#     }
#
#     return self.api.post_request(
#         endpoint=endpoint,
#         data=data,
#         files=files
#     )

DATASET_DICT = {
    'IMAGE': ImageRootNode,
    'LIDAR_BASIC': LidarBasicRootNode,
    'LIDAR_FUSION': LidarFusionRootNode
}
