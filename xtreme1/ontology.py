import warnings
from functools import reduce
from typing import List, Dict, Optional

from .exceptions import ParamException


class Nodes:
    def __init__(
            self,
            nodes,
            parent
    ):
        self._parent = parent
        if len(nodes) != len(set([n.name for n in nodes])):
            warnings.warn(
                f'Detect duplicated nodes in <{self._parent}>. \
                Only the last one will be stored in nodes.'
            )
        self.nodes = []
        for node in nodes:
            self.append(node)

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

    def append(
            self,
            node
    ):
        assert isinstance(node, RELA_DICT[self._parent.__class__])  # noqa

        self.nodes.append(node)
        node._parent = self._parent

    def remove(
            self,
            name
    ):
        self.nodes.remove(self.get(name))

    def gen_node(
            self,
            **kwargs
    ):
        node = RELA_DICT[self._parent.__class__](**kwargs)
        self.append(node)

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
        if type(nodes) == list:
            nodes = Nodes(nodes, self)
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


class AttrsNode(Node):
    __slots__ = ['name', 'options', '_nodes', 'type', 'required']

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
        self.options = self._nodes


class OptionNode(Node):
    __slots__ = ['name', 'attributes', '_nodes']

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
        self.attributes = self._nodes


class RootNode(Node):
    __slots__ = ['_id', 'name', 'color', 'tool_type', '_nodes', 'tool_type_options',
                 'attributes', '_client', '_onto_type']

    def __init__(
            self,
            name,
            onto_type: str,
            tool_type: str,
            tool_type_options: Optional[Dict] = None,
            color: str = '#7dfaf2',
            attrs: Optional[List] = None,
            parent=None,
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            nodes=attrs,
            parent=parent,
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
        self.attributes = self._nodes
        self._onto_type = onto_type


class Ontology:
    __slots__ = ['classes', 'classifications', 'des_id', 'name', '_client', '_des_type']

    def __init__(
            self,
            client,
            des_type: str,
            classes: Optional[List] = None,
            classifications: Optional[List] = None,
            des_id: str = None
    ):
        self.des_id = des_id
        self._client = client
        self._des_type = des_type
        if classes is None:
            classes = []
        if classifications is None:
            classifications = []
        self.classes = Nodes(self._to_node(classes, onto_type='class'), self)
        self.classifications = Nodes(self._to_node(classifications, onto_type='classification'), self)

    def __repr__(
            self
    ):
        return f'<{self.__class__.__name__}> The ontology of {self.des_id}'

    def __str__(
            self
    ):
        classes = {f'<{n.__class__.__name__}> {n.name}' for n in self.classes.nodes}
        classifications = {f'<{n.__class__.__name__}> {n.name}' for n in self.classifications.nodes}
        return f'<{self.__class__.__name__}> classes: {classes}, classifications: {classifications}'

    @staticmethod
    def _to_node(
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
                    onto_type=onto_type
                )
            else:
                if 'options' in node:
                    cur_node = AttrsNode(
                        name=node['name'],
                        input_type=node['type'],
                        required=node['required'],
                        options=Ontology._to_node(node['options']),
                        id_=node.get('id')
                    )
                else:
                    cur_node = OptionNode(
                        name=node['name'],
                        attrs=Ontology._to_node(node['attributes']),
                        id_=node.get('id')
                    )

            total.append(cur_node)

        return total

    @staticmethod
    def _to_camel(
            var
    ):
        parts = var.split('_')
        return reduce(lambda x, y: x + y.capitalize(), parts)

    @staticmethod
    def to_dict(
            node
    ):
        result = {}
        attrs = ['classes', 'classifications', 'name', 'color', 'tool_type', 'tool_type_options', 'attributes',
                 'options', 'type', 'required']
        for attr_ in attrs:
            value = getattr(node, attr_, None)
            attr = Ontology._to_camel(attr_)
            if value is None:
                continue
            if type(value).__name__ == 'Nodes':
                result[attr] = []
                for child in value.nodes:
                    result[attr].append(Ontology.to_dict(child))
            else:
                result[attr] = value

        return result

    def del_ontology_cls(
            self,
            onto_type: str,
            name
    ):
        try:
            if 'class' in onto_type:
                root_node = self.classes.get(name)
                self.classes.remove(name)
            else:
                root_node = self.classifications.get(name)
                self.classifications.remove(name)
        except ValueError:
            raise ParamException(message='This node is already deleted.')

        return self._client.del_ontology_cls(
            onto_type=onto_type,
            cls_id=root_node.id,
            des_type=self._des_type
        )


RELA_DICT = {
    Ontology: RootNode,
    RootNode: AttrsNode,
    AttrsNode: OptionNode,
    OptionNode: AttrsNode
}
