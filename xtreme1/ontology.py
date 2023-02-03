import warnings
from typing import List, Dict, Optional

from .exceptions import ParamException, NameDuplicatedException
from ._others import _to_camel


class Nodes:
    def __init__(
            self,
            nodes,
            parent
    ):
        self._parent = parent
        if len(nodes) != len(set([n.name for n in nodes])):
            warnings.warn(
                f'Detect duplicated nodes.'
            )
        self.nodes = []
        for node in nodes:
            self._append(node)

    def __repr__(
            self
    ):
        members = [f'<{n.__class__.__name__}> {n.name}' for n in self.nodes]
        return f'<{self.__class__.__name__}> members: {members}'

    def __str__(
            self
    ):
        members = [f'<{n.__class__.__name__}> {n.name}' for n in self.nodes]
        return f'<{self.__class__.__name__}> members: {members}'

    def get(
            self,
            name
    ):
        for node in self.nodes:
            if node.name == name:
                return node

    def _check_duplicated(
            self,
            node
    ):
        check_node = self.get(node.name)
        if check_node:
            sus_exception = NameDuplicatedException(
                message='This node already exists!'
            )
            if isinstance(node, RootNode):
                if check_node.tool_type == node.tool_type:
                    raise sus_exception
            else:
                raise sus_exception

    def _append(
            self,
            node
    ):
        assert isinstance(node, NODE_DICT[self._parent.__class__])  # noqa
        self._check_duplicated(node=node)

        self.nodes.append(node)
        node._parent = self._parent

    def remove(
            self,
            name
    ):
        self.nodes.remove(self.get(name))

    def _gen_node(
            self,
            **kwargs
    ):
        node = NODE_DICT[self._parent.__class__](**kwargs)
        self._append(node)

        return node


class AttrNodes(Nodes):
    def __init__(
            self,
            nodes,
            parent
    ):
        super().__init__(
            nodes=nodes,
            parent=parent
        )

    def gen_node(
            self,
            name: str,
            options: List[str],
            input_type: str = 'RADIO',
            required: bool = False,
    ):
        node = self._gen_node(
            name=name,
            input_type=input_type,
            required=required
        )

        for opt in options:
            opt_node = OptionNode(
                name=opt
            )
            node.options._append(opt_node)

        return node


class OptionNodes(Nodes):
    def __init__(
            self,
            nodes,
            parent
    ):
        super().__init__(
            nodes=nodes,
            parent=parent
        )

    def gen_node(
            self,
            name: str
    ):
        node = self._gen_node(
            name=name
        )

        return node


class RootNodes(Nodes):
    def __init__(
            self,
            nodes,
            parent,
            onto_type
    ):
        super().__init__(
            nodes=nodes,
            parent=parent
        )
        self.onto_type = onto_type

    def gen_node(
            self,
            name: str,
            tool_type: str,
            color: str = '#7dfaf2'
    ):
        node = self._gen_node(
            name=name,
            tool_type=tool_type,
            onto_type=self.onto_type,
            color=color
        )

        return node


class Node:
    __slots__ = ['name', '_nodes', '_parent', 'id']

    def __init__(
            self,
            name,
            nodes: Optional[List] = None,
            parent=None,
            id_: Optional[int] = None,
    ):
        self.name = name
        self._parent = parent
        if nodes is None:
            nodes = []
        self._nodes = nodes
        self.id = id_

    def __repr__(
            self
    ):
        return f'<{self.__class__.__name__}> {self.name}'

    def __str__(
            self
    ):
        return f'<{self.__class__.__name__}> {self.name}'

    def to_dict(
            self
    ):
        result = {}
        attrs = ['name', 'color', 'tool_type', 'tool_type_options', 'attributes',
                 'options', 'type', 'required']
        for attr_ in attrs:
            value = getattr(self, attr_, None)
            attr = _to_camel(attr_)
            if value is None:
                continue
            if type(value).__name__ == 'Nodes':
                result[attr] = []
                for child in value.nodes:
                    result[attr].append(child.to_dict())
            else:
                result[attr] = value

        return result


class AttrNode(Node):
    __slots__ = ['name', '_parent', 'id', 'options', '_nodes', 'type', 'required']

    def __init__(
            self,
            name,
            options: Optional[List] = None,
            input_type: str = 'RADIO',
            required: bool = False,
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            nodes=options,
            id_=id_
        )
        self.type = input_type
        self.required = required
        self.options = OptionNodes(
            nodes=self._nodes,
            parent=self
        )


class OptionNode(Node):
    __slots__ = ['name', 'id', 'attributes', '_nodes', '_parent']

    def __init__(
            self,
            name,
            attrs: Optional[List] = None,
            id_: Optional[int] = None
    ):
        super().__init__(
            name=name,
            nodes=attrs,
            id_=id_
        )
        self.attributes = AttrNodes(
            nodes=self._nodes,
            parent=self
        )


class RootNode(Node):
    __slots__ = ['_id', 'name', 'color', 'tool_type', '_nodes', 'tool_type_options',
                 'attributes', '_client', 'onto_type']

    def __init__(
            self,
            name,
            client,
            tool_type: str,
            onto_type: str = 'class',
            color: str = '#7dfaf2',
            attrs: Optional[List] = None,
            tool_type_options: Optional[Dict] = None,
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            nodes=attrs,
            id_=id_
        )
        self.color = color
        self.tool_type = tool_type.upper()
        if tool_type_options is None:
            tool_type_options = {}
            if self.tool_type in ['CUBOID']:
                tool_type_options = {
                    "width": [],
                    "height": [],
                    "length": [],
                    "points": [],
                    "isStandard": False,
                    "isConstraints": False
                }
        self.tool_type_options = tool_type_options
        self.attributes = AttrNodes(
            nodes=self._nodes,
            parent=self
        )
        onto_type = onto_type.lower()
        self._check_onto_type(onto_type)
        self.onto_type = onto_type
        self._client = client

    @staticmethod
    def _check_onto_type(
            onto_type
    ):
        if onto_type not in ['class', 'classification']:
            raise ParamException(message="Ontology type can only be either 'class' or 'classification'")

    def delete_cls(
            self
    ):
        if 'dataset' in self._parent.des_type:
            endpoint = f'dataset{self.onto_type.capitalize()}/delete/{self.id}'
        else:
            endpoint = f'{self.onto_type.capitalize()}/delete/{self.id}'

        resp = self._parent._client.api.post_request(
            endpoint=endpoint
        )

        if self.onto_type == 'class':
            self._parent.classes.remove(self.name)
        else:
            self._parent.classifications.remove(self.name)

        return resp

    # def update_cls(
    #         self,
    #         des_id: str,
    #         des_type: str = 'dataset',
    #         onto_id: Optional[str] = None,
    # ):
    #     onto_dict = Ontology.to_dict(onto)
    #
    #     if 'ontology' in des_type:
    #         endpoint = f'{onto_type}/update/{onto_id}'
    #         onto_dict['ontologyId'] = des_id
    #     else:
    #         endpoint = f'dataset{onto_type.capitalize()}/update/{onto_id}'
    #         onto_dict['datasetId'] = des_id
    #
    #     resp = self.api.post_request(
    #         endpoint=endpoint,
    #         payload=onto_dict
    #
    #     )
    #
    #     return resp


class Ontology:
    __slots__ = ['classes', 'classifications', 'des_id', 'name', '_client', 'des_type']

    def __init__(
            self,
            client,
            des_type: str,
            des_id: str,
            classes: Optional[List] = None,
            classifications: Optional[List] = None
    ):
        self.des_id = des_id
        self._client = client
        self.des_type = des_type
        if classes is None:
            classes = []
        if classifications is None:
            classifications = []
        self.classes = RootNodes(
            nodes=self._to_node(classes, onto_type='class'),
            parent=self,
            onto_type='class'
        )
        self.classifications = RootNodes(
            nodes=self._to_node(classifications, onto_type='classification'),
            parent=self,
            onto_type='classification'
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


NODE_DICT = {
    Ontology: RootNode,
    RootNode: AttrNode,
    AttrNode: OptionNode,
    OptionNode: AttrNode
}
