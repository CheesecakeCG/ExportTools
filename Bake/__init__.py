import bpy
import nodeitems_utils
from nodeitems_utils import NodeItem, register_node_categories, unregister_node_categories

from .bake_nodes import *


def register():
    nodeitems_utils.register_node_categories('HWBAKE_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('HWBAKE_NODES')
