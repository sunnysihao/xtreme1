import warnings
from functools import reduce
from typing import List, Dict, Optional


class Nodes:
    def __init__(
            self,
            nodes,
            parent
    ):
        self._parent = parent
        if len(nodes) != len(set([n.name for n in nodes])):
            warnings.warn('Detect duplicated nodes. Only the last one will be stored in nodes.')
        self.nodes = set(nodes)
        for node in nodes:
            self.append(node)

    def __repr__(
            self
    ):
        members = {f'<{n.__class__.__name__}> {n.name}' for n in self.nodes}
        return f'<Nodes> members: {members}'

    def __str__(
            self
    ):
        members = {f'<{n.__class__.__name__}> {n.name}' for n in self.nodes}
        return f'<Nodes> members: {members}'

    def append(
            self,
            node
    ):
        rela_dict = {
            'ClassRoot': 'AttrsNode',
            'AttrsNode': 'OptionNode',
            'OptionNode': 'AttrsNode'
        }
        assert rela_dict[self._parent.__class__.__name__] == node.__class__.__name__

        self.nodes.add(node)
        node._parent = self._parent
        setattr(self, node.name, node)


class Node:
    __slots__ = ['name', '_nodes', '_parent']

    def __init__(
            self,
            name,
            nodes: Optional[List] = None,
            parent=None
    ):
        self._parent = parent
        if nodes is None:
            nodes = []
        if type(nodes) == list:
            nodes = Nodes(nodes, self)
        self._nodes = nodes
        self.name = name

    def __repr__(
            self
    ):
        return f'<{self.__class__.__name__}> {self.name}'

    def __str__(
            self
    ):
        return f'<{self.__class__.__name__}> {self.name}'

    def update(
            self,
            new_attrs
    ):
        for k, v in new_attrs.items():
            if k == 'name':
                if self._parent:
                    delattr(self._parent._nodes, self.name)
                    setattr(self._parent._nodes, v, self)
            setattr(self, k, v)


class AttrsNode(Node):
    __slots__ = ['name', 'options', '_nodes', 'type', 'required']

    def __init__(
            self,
            name,
            options: Optional[List] = None,
            input_type: str = 'RADIO',
            required: bool = True
    ):
        super().__init__(
            name=name,
            nodes=options
        )
        self.type = input_type
        self.required = required
        self.options = self._nodes


class OptionNode(Node):
    __slots__ = ['name', 'attributes', '_nodes']

    def __init__(
            self,
            name,
            attrs: Optional[List] = None
    ):
        super().__init__(
            name=name,
            nodes=attrs
        )
        self.attributes = self._nodes


class ClassRoot(Node):
    __slots__ = ['name', 'color', 'tool_type', '_nodes', 'tool_type_options', 'attributes']

    def __init__(
            self,
            name,
            color,
            tool_type,
            tool_type_options: Optional[Dict] = None,
            attrs: Optional[List] = None
    ):
        super().__init__(
            name=name,
            nodes=attrs
        )
        self.color = color
        self.tool_type = tool_type
        if tool_type_options is None:
            tool_type_options = {}
        self.tool_type_options = tool_type_options
        self.attributes = self._nodes


def _to_camel(
        var
):
    parts = var.split('_')
    return reduce(lambda x, y: x + y.capitalize(), parts)


def _to_dict(
        node
):
    result = {}
    attrs = ['name', 'color', 'tool_type', 'tool_type_options', 'attributes', 'options', 'type']
    for attr_ in attrs:
        value = getattr(node, attr_, None)
        attr = _to_camel(attr_)
        if value is None:
            continue
        if type(value).__name__ == 'Nodes':
            result[attr] = []
            for child in value.nodes:
                result[attr].append(_to_dict(child))
        else:
            result[attr] = value

    return result


def gen_ontology(
        classes: List[ClassRoot] = None,
        classifications: List = None
):
    result = {
        'classes': [],
        'classifications': []
    }

    for c in classes:
        result['classes'].append(_to_dict(c))

    for cf in classifications:
        result['classifications'].append(_to_dict(cf))

    return result
