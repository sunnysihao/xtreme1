# import warnings
# from typing import List, Dict, Optional
#
# from .node import AttrNode, OptionNode, RootNode, ImageRootNode, LidarBasicRootNode, LidarFusionRootNode
# from ..exceptions import ParamException, NameDuplicatedException
# from .._others import _to_camel
#
#
# class Nodes:
#     def __init__(
#             self,
#             nodes,
#             parent
#     ):
#         self._parent = parent
#         if len(nodes) != len(set([n.name for n in nodes])):
#             warnings.warn(
#                 f'Detect duplicated nodes.'
#             )
#         self.nodes = []
#         for node in nodes:
#             self._append(node)
#
#     def __repr__(
#             self
#     ):
#         members = [f'<{n.__class__.__name__}> {n.name}' for n in self.nodes]
#         return f'<{self.__class__.__name__}> members: {members}'
#
#     def __str__(
#             self
#     ):
#         members = [f'<{n.__class__.__name__}> {n.name}' for n in self.nodes]
#         return f'<{self.__class__.__name__}> members: {members}'
#
#     def get(
#             self,
#             name
#     ):
#         for node in self.nodes:
#             if node.name == name:
#                 return node
#
#     def _check_duplicated(
#             self,
#             node
#     ):
#         check_node = self.get(node.name)
#         if check_node:
#             sus_exception = NameDuplicatedException(
#                 message='This node already exists!'
#             )
#             if isinstance(node, (ImageRootNode, LidarBasicRootNode, LidarFusionRootNode)):
#                 if check_node.tool_type == node.tool_type:
#                     raise sus_exception
#             else:
#                 raise sus_exception
#
#     def _append(
#             self,
#             node
#     ):
#         self._check_duplicated(node=node)
#
#         self.nodes.append(node)
#         node._parent = self._parent
#
#     def remove(
#             self,
#             name
#     ):
#         self.nodes.remove(self.get(name))
#
#     def _gen_node(
#             self,
#             node_class,
#             **kwargs
#     ):
#         node = node_class(**kwargs)
#         self._append(node)
#
#         return node
#
#
# class AttrNodes(Nodes):
#     def __init__(
#             self,
#             nodes,
#             parent
#     ):
#         super().__init__(
#             nodes=nodes,
#             parent=parent
#         )
#
#     def gen_node(
#             self,
#             name: str,
#             options: List[str],
#             input_type: str = 'RADIO',
#             required: bool = False,
#     ):
#         total_options = []
#         for opt in options:
#             new_opt = OptionNode(
#                 name=opt,
#                 attrs=None
#             )
#             new_opt.attributes = AttrNodes(
#                 nodes=[],
#                 parent=new_opt
#             )
#             total_options.append(opt)
#
#         node = self._gen_node(
#             node_class=AttrNode,
#             name=name,
#             input_type=input_type,
#             required=required,
#             options=OptionNodes(
#                 nodes=total_options,
#                 parent=self
#             )
#         )
#
#         return node
#
#
# class OptionNodes(Nodes):
#     def __init__(
#             self,
#             nodes,
#             parent
#     ):
#         super().__init__(
#             nodes=nodes,
#             parent=parent
#         )
#
#     def gen_node(
#             self,
#             name: str
#     ):
#         node = self._gen_node(
#             node_class=OptionNode,
#             name=name,
#             attrs=AttrNodes(
#                 nodes=[],
#                 parent=self
#             )
#         )
#
#         return node
#
#
# class RootNodes(Nodes):
#     def __init__(
#             self,
#             nodes,
#             parent,
#             onto_type,
#             dataset_type
#     ):
#         super().__init__(
#             nodes=nodes,
#             parent=parent
#         )
#         self.onto_type = onto_type
#         self.dataset_type = dataset_type
#
#     def gen_node(
#             self,
#             name: str,
#             tool_type: str,
#             color: str = '#7dfaf2'
#     ):
#         node = self._gen_node(
#             node_class=DATASET_DICT[self.dataset_type],
#             name=name,
#             tool_type=tool_type,
#             onto_type=self.onto_type,
#             color=color
#         )
#
#         return node
#
#
# DATASET_DICT = {
#     'IMAGE': ImageRootNode,
#     'LIDAR_BASIC': LidarBasicRootNode,
#     'LIDAR_FUSION': LidarFusionRootNode
# }
