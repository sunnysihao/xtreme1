import json

from typing import List, Dict, Optional, Union

from ..exceptions import NameDuplicatedException

INDENT = 4


class Node:
    __slots__ = ['name', '_parent', 'id', '_nodes']

    total_attrs = []
    total_keys = []

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

    def to_dict(
            self
    ):
        result = {}
        for i in range(len(self.total_attrs)):
            attr = self.total_attrs[i]
            k = self.total_keys[i]
            value = getattr(self, attr, None)
            if value is None:
                continue
            if attr == '_nodes':
                result[k] = []
                for node in value:
                    result[k].append(node.to_dict())
            else:
                result[k] = value

        return result

    def _check_dup(
            self,
            new_name
    ):
        names = [x.name for x in self._nodes]
        if new_name in names:
            raise NameDuplicatedException(message='This label already exists!')

    @staticmethod
    def _parse_dict(
            node_dict
    ):
        return {}, []

    @classmethod
    def to_node(
            cls,
            org_dict
    ):
        cur_args, cur_child_nodes = cls._parse_dict(org_dict)
        new_node = cls(
            **cur_args
        )

        for child in cur_child_nodes:
            new_child_node = NODE_MAP[cls].to_node(child)
            new_node._nodes.append(new_child_node)

        return new_node


class AttrNode(Node):
    __slots__ = ['name', '_nodes', 'id', 'type', 'required']

    total_attrs = ['name', 'id', 'type', 'required', '_nodes']
    total_keys = ['name', 'id', 'type', 'required', 'options']

    def __init__(
            self,
            name,
            options: Optional[List[str]] = None,
            input_type: str = 'RADIO',
            required: bool = False,
            id_: Optional[str] = None,
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
            name: Union[str, List[str]]
    ):
        if type(name) == str:
            name = [name]

        for single in name:
            self._check_dup(
                new_name=single
            )

            new_opt = OptionNode(
                name=single
            )
            self._nodes.append(new_opt)

        return self._nodes

    @staticmethod
    def _parse_dict(
            node_dict
    ):
        kwargs = {
            'name': node_dict['name'],
            'input_type': node_dict['type'],
            'required': node_dict['required'],
        }

        child_nodes = node_dict['options']

        return kwargs, child_nodes


class OptionNode(Node):
    __slots__ = ['name', 'id', '_nodes']

    total_attrs = ['name', 'id', '_nodes']
    total_keys = ['name', 'id', 'attributes']

    def __init__(
            self,
            name,
            id_: Optional[str] = None
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
    def _parse_dict(
            node_dict
    ):
        kwargs = {
            'name': node_dict['name']
        }

        child_nodes = node_dict['attributes']

        return kwargs, child_nodes


class RootNode(Node):
    __slots__ = ['id', 'name', '_nodes', 'onto_type']

    def __init__(
            self,
            name,
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
    __slots__ = ['id', 'name', 'color', 'tool_type', 'tool_type_options',
                 '_nodes', 'onto_type']

    total_attrs = ['name', 'id', 'tool_type', 'tool_type_options', '_nodes']
    total_keys = ['name', 'id', 'toolType', 'toolTypeOptions', 'attributes']

    def __init__(
            self,
            name,
            tool_type: str = 'BOUNDING_BOX',
            attrs: Optional[List] = None,
            color: str = '#7dfaf2',
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
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
    def _parse_dict(
            node_dict
    ):
        kwargs = {
            'name': node_dict['name'],
            'tool_type': node_dict['toolType'],
            'color': node_dict['color'],
            'id_': node_dict['id']
        }

        child_nodes = node_dict['attributes']

        return kwargs, child_nodes


class LidarBasicRootNode(RootNode):
    __slots__ = ['id', 'name', 'color', 'tool_type', 'tool_type_options',
                 '_nodes', 'onto_type']

    total_attrs = ['name', 'id', 'tool_type', 'tool_type_options', '_nodes']
    total_keys = ['name', 'id', 'toolType', 'toolTypeOptions', 'attributes']

    def __init__(
            self,
            name,
            tool_type: str = 'CUBOID',
            tool_type_options: Optional[Dict] = None,
            attrs: Optional[List] = None,
            color: str = '#7dfaf2',
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
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
    def _parse_dict(
            node_dict
    ):
        kwargs = {
            'name': node_dict['name'],
            'tool_type': node_dict['toolType'],
            'tool_type_options': node_dict['toolTypeOptions'],
            'color': node_dict['color'],
            'id_': node_dict['id']
        }

        child_nodes = node_dict['attributes']

        return kwargs, child_nodes


class LidarFusionRootNode(RootNode):
    __slots__ = ['id', 'name', 'color', 'tool_type', 'tool_type_options',
                 '_nodes', 'onto_type']

    total_attrs = ['name', 'id', 'tool_type', 'tool_type_options', '_nodes']
    total_keys = ['name', 'id', 'toolType', 'toolTypeOptions', 'attributes']

    def __init__(
            self,
            name,
            tool_type: str = 'CUBOID',
            tool_type_options: Optional[Dict] = None,
            attrs: Optional[List] = None,
            color: str = '#7dfaf2',
            id_: Optional[int] = None,
    ):
        super().__init__(
            name=name,
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
    def _parse_dict(
            node_dict
    ):
        kwargs = {
            'name': node_dict['name'],
            'tool_type': node_dict['toolType'],
            'tool_type_options': node_dict['toolTypeOptions'],
            'color': node_dict['color'],
            'id_': node_dict['id']
        }

        child_nodes = node_dict['attributes']

        return kwargs, child_nodes


NODE_MAP = {
    Node: None,
    ImageRootNode: AttrNode,
    LidarBasicRootNode: AttrNode,
    LidarFusionRootNode: AttrNode,
    AttrNode: OptionNode,
    OptionNode: AttrNode
}
