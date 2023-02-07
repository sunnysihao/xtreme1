import json

from typing import List, Dict, Optional

from .._others import _to_camel
from ..exceptions import NameDuplicatedException

INDENT = 4


class Node:
    __slots__ = ['name', '_parent', 'id', '_nodes']

    def __init__(
            self,
            name,
            nodes: Optional[List] = None,
            id_: Optional[int] = None,
    ):
        self.name = name
        self.id = id_
        if not nodes:
            nodes = []
        self._nodes = nodes

    def __repr__(
            self
    ):
        return f'<{self.__class__.__name__}> {self.name}'

    # def to_dict(
    #         self
    # ):
    #     result = {}
    #     attrs = ['name', 'color', 'tool_type', 'tool_type_options', 'attributes',
    #              'options', 'type', 'required']
    #     for attr_ in attrs:
    #         value = getattr(self, attr_, None)
    #         attr = _to_camel(attr_)
    #         if value is None:
    #             continue
    #         if type(value).__name__ == 'Nodes':
    #             result[attr] = []
    #             for child in value.nodes:
    #                 result[attr].append(child.to_dict())
    #         else:
    #             result[attr] = value
    #
    #     return result

    def _check_dup(
            self,
            new_name
    ):
        names = [x.name for x in self._nodes]
        if new_name in names:
            raise NameDuplicatedException(message='This label already exists!')


class AttrNode(Node):
    __slots__ = ['name', '_nodes', 'id', 'type', 'required']

    def __init__(
            self,
            name,
            options: Optional[List[str]] = None,
            input_type: str = 'RADIO',
            required: bool = False,
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            id_=id_
        )
        self.type = input_type
        self.required = required
        if not options:
            options = []
        for opt in options:
            self.add_option(opt)

    def __str__(
            self
    ):
        self_intro = {
            'name': self.name,
            'options': [n.name for n in self._nodes],
            'type': self.type,
            'required': self.required
        }
        self_intro = json.dumps(self_intro, indent=' ' * INDENT)

        return f"<{self.__class__.__name__}>\n{self_intro}"

    @property
    def options(
            self
    ):
        return self._nodes

    def add_option(
            self,
            name
    ):
        self._check_dup(
            new_name=name
        )

        new_opt = OptionNode(
            name=name
        )
        self._nodes.append(new_opt)

        return new_opt

    @staticmethod
    def to_node(
            node_dict
    ):
        new_attr_node = AttrNode(
            name=node_dict['name'],
            input_type=node_dict['type'],
            required=node_dict['required']
        )

        options = node_dict['options']
        for opt in options:
            new_opt_node = OptionNode.to_node(opt)
            new_attr_node.options.append(new_opt_node)

        return new_attr_node


class OptionNode(Node):
    __slots__ = ['name', 'id', '_nodes']

    def __init__(
            self,
            name,
            id_: Optional[int] = None
    ):
        super().__init__(
            name=name,
            id_=id_
        )
        self._nodes = []

    def __str__(
            self
    ):
        self_intro = {
            'name': self.name,
            'attributes': [n.name for n in self._nodes],
        }
        self_intro = json.dumps(self_intro, indent=' ' * INDENT)

        return f"<{self.__class__.__name__}>\n{self_intro}"

    @property
    def attributes(
            self
    ):
        return self._nodes

    def add_attribute(
            self,
            name,
            input_type: str = 'RADIO',
            required: bool = False
    ):
        self._check_dup(
            new_name=name
        )

        new_attr = AttrNode(
            name=name,
            input_type=input_type,
            required=required
        )
        self._nodes.append(new_attr)

        return new_attr

    @staticmethod
    def to_node(
            node_dict
    ):
        new_opt_node = OptionNode(
            name=node_dict['name']
        )

        attrs = node_dict['attributes']
        for attr in attrs:
            new_attr_node = AttrNode.to_node(attr)
            new_opt_node._nodes.append(new_attr_node)

        return new_opt_node


class RootNode(Node):
    __slots__ = ['_id', 'name', '_nodes', '_client', 'onto_type']

    def __init__(
            self,
            name,
            client,
            attrs,
            onto_type: str = 'class',
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            nodes=attrs,
            id_=id_
        )
        onto_type = onto_type.lower()
        self.onto_type = onto_type
        self._client = client

    @property
    def attributes(
            self
    ):
        return self._nodes

    def add_attribute(
            self,
            name,
            input_type: str = 'RADIO',
            required: bool = False
    ):
        self._check_dup(
            new_name=name
        )

        new_attr = AttrNode(
            name=name,
            input_type=input_type,
            required=required
        )
        self._nodes.append(new_attr)

        return new_attr

        # def delete_cls(
        #         self
        # ):
        #     if 'dataset' in self._parent.des_type:
        #         endpoint = f'dataset{self.onto_type.capitalize()}/delete/{self.id}'
        #     else:
        #         endpoint = f'{self.onto_type.capitalize()}/delete/{self.id}'
        #
        #     resp = self._parent._client.api.post_request(
        #         endpoint=endpoint
        #     )
        #
        #     if self.onto_type == 'class':
        #         self._parent.classes.remove(self.name)
        #     else:
        #         self._parent.classifications.remove(self.name)
        #
        #     return resp

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


class ImageRootNode(RootNode):
    __slots__ = ['_id', 'name', 'color', 'tool_type', 'tool_type_options',
                 '_nodes', '_client', 'onto_type']

    def __init__(
            self,
            name,
            client,
            tool_type: str = 'BOUNDING_BOX',
            attrs: Optional[List] = None,
            color: str = '#7dfaf2',
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            client=client,
            attrs=attrs,
            onto_type='class',
            id_=id_
        )
        self.tool_type = tool_type.upper()
        self.tool_type_options = {}
        self.color = color

    def __str__(
            self
    ):
        self_intro = {
            'name': self.name,
            'color': self.color,
            'toolType': self.tool_type,
            'toolTypeOptions': self.tool_type_options,
            'attributes': [n.name for n in self._nodes],
        }
        self_intro = json.dumps(self_intro, indent=' ' * INDENT)

        return f"<{self.__class__.__name__}>\n{self_intro}"

    @staticmethod
    def to_node(
            node_dict,
            client
    ):
        new_root = ImageRootNode(
            name=node_dict['name'],
            client=client,
            tool_type=node_dict['toolType'],
            color=node_dict['color'],
            id_=node_dict['id']
        )

        attrs = node_dict['attributes']
        for attr in attrs:
            new_attr_node = AttrNode.to_node(attr)
            new_root._nodes.append(new_attr_node)

        return new_root


class LidarBasicRootNode(RootNode):
    __slots__ = ['_id', 'name', 'color', 'tool_type', 'tool_type_options',
                 '_nodes', '_client', 'onto_type']

    def __init__(
            self,
            name,
            client,
            tool_type: str = 'CUBOID',
            tool_type_options: Optional[Dict] = None,
            attrs: Optional[List] = None,
            color: str = '#7dfaf2',
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            client=client,
            attrs=attrs,
            onto_type='class',
            id_=id_
        )
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
        self.color = color

    def __str__(
            self
    ):
        self_intro = {
            'name': self.name,
            'color': self.color,
            'toolType': self.tool_type,
            'toolTypeOptions': self.tool_type_options,
            'attributes': [n.name for n in self._nodes],
        }
        self_intro = json.dumps(self_intro, indent=' ' * INDENT)

        return f"<{self.__class__.__name__}>\n{self_intro}"

    @staticmethod
    def to_node(
            node_dict,
            client
    ):
        new_root = LidarBasicRootNode(
            name=node_dict['name'],
            client=client,
            tool_type=node_dict['toolType'],
            tool_type_options=node_dict['toolTypeOptions'],
            color=node_dict['color'],
            id_=node_dict['id']
        )

        attrs = node_dict['attributes']
        for attr in attrs:
            new_attr_node = AttrNode.to_node(attr)
            new_root._nodes.append(new_attr_node)

        return new_root


class LidarFusionRootNode(RootNode):
    __slots__ = ['_id', 'name', 'color', 'tool_type', 'tool_type_options',
                 '_nodes', '_client', 'onto_type']

    def __init__(
            self,
            name,
            client,
            tool_type: str = 'CUBOID',
            tool_type_options: Optional[Dict] = None,
            attrs: Optional[List] = None,
            color: str = '#7dfaf2',
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            client=client,
            attrs=attrs,
            onto_type='class',
            id_=id_
        )
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
        self.color = color

    def __str__(
            self
    ):
        self_intro = {
            'name': self.name,
            'color': self.color,
            'toolType': self.tool_type,
            'toolTypeOptions': self.tool_type_options,
            'attributes': [n.name for n in self._nodes],
        }
        self_intro = json.dumps(self_intro, indent=' ' * INDENT)

        return f"<{self.__class__.__name__}>\n{self_intro}"

    @staticmethod
    def to_node(
            node_dict,
            client
    ):
        new_root = LidarFusionRootNode(
            name=node_dict['name'],
            client=client,
            tool_type=node_dict['toolType'],
            tool_type_options=node_dict['toolTypeOptions'],
            color=node_dict['color'],
            id_=node_dict['id']
        )

        attrs = node_dict['attributes']
        for attr in attrs:
            new_attr_node = AttrNode.to_node(attr)
            new_root._nodes.append(new_attr_node)

        return new_root
