from typing import List, Dict, Optional

from .node import AttrNode, OptionNode, AttrNodes, OptionNodes, RootNodes
from ..exceptions import ParamException, NameDuplicatedException
from .._others import _to_camel


class Ontology:
    __slots__ = ['classes', 'classifications', 'des_id', 'des_type', 'dataset_type', 'name', '_client', ]

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
        self.dataset_type = dataset_type
        if classes is None:
            classes = []
        if classifications is None:
            classifications = []
        self.classes = RootNodes(
            nodes=self._to_node(classes, onto_type='class'),
            parent=self,
            onto_type='class',
            dataset_type=self.dataset_type
        )
        self.classifications = RootNodes(
            nodes=self._to_node(classifications, onto_type='classification'),
            parent=self,
            onto_type='classification',
            dataset_type=self.dataset_type
        )

    def __repr__(
            self
    ):
        return f'<{self.__class__.__name__}> The ontology of {self.des_type} {self.des_id}'

    def __str__(
            self
    ):
        classes = {f'<{n.__class__.__name__}> {n.name}' for n in self.classes.nodes}
        classifications = {f'<{n.__class__.__name__}> {n.name}' for n in self.classifications.nodes}
        return f'<{self.__class__.__name__}> classes: {classes}, classifications: {classifications}'

    @classmethod
    def _to_node(
            cls,
            ontos,
            onto_type=None
    ):
        total = []
        for node in ontos:

            if 'toolType' in node:
                cur_node = RootNode(
                    name=node['name'],
                    color=node['color'],
                    tool_type=node['toolType'],
                    tool_type_options=node['toolTypeOptions'],
                    attrs=Ontology._to_node(node['attributes']),
                    id_=node.get('id'),
                    onto_type=onto_type,
                    client=cls._client
                )
            else:
                if 'options' in node:
                    cur_node = AttrNode(
                        name=node['name'],
                        input_type=node['type'],
                        required=node['required'],
                        options=cls._to_node(node['options']),
                        id_=node.get('id')
                    )
                else:
                    cur_node = OptionNode(
                        name=node['name'],
                        attrs=cls._to_node(node['attributes']),
                        id_=node.get('id')
                    )

            total.append(cur_node)

        return total

    def to_dict(
            self
    ):
        result = {
            'classes': [cls.to_dict() for cls in self.classes.nodes],
            'classifications': [cls.to_dict() for cls in self.classifications.nodes]
        }

        return result

    def delete_ontology(
            self
    ):
        return self._client.delete_ontology(
            des_id=self.des_id
        )

#
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


# NODE_DICT = {
#     Ontology: RootNode,
#     RootNode: AttrNode,
#     AttrNode: OptionNode,
#     OptionNode: AttrNode
# }
