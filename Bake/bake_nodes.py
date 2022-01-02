import bpy
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from nodeitems_builtins import ShaderNodeCategory


class HWBakeOutputNode(bpy.types.Node):
    # === Basics ===
    # Description string
    '''Bake Output Node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    # bl_idname = 'CustomNodeType'
    # Label for nice name display
    bl_label = "Bake Output Node"
    # Icon identifieR
    bl_idname = "HWBakeOutputNode"

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    to_vertex_colors: bpy.props.BoolProperty(name="To Vertex Colors")
    image: bpy.props.PointerProperty(
        type=bpy.types.Image,
        name="Pattern",
        update=lambda s, c: s.update_pattern())

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Color")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        self.node_tree = node.node_tree.copy()

    # Free function to clean up on removal.

    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):

        row = layout.row()
        row.template_ID(self, 'image', new='image.new', open='image.open')
        # row.enabled = not self.to_vertex_colors

        # layout.prop(self, "to_vertex_colors")

        layout.operator("object.hwbakenodes")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically

    def draw_label(self):
        return "Bake Node"


node_categories = [
    # identifier, label, items list
    ShaderNodeCategory('HWBAKENODES', "Bake Nodes", items=[
        # our basic node
        NodeItem(HWBakeOutputNode.bl_idname),
    ])
]
