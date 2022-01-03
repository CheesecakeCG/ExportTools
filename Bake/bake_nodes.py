import bpy
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from nodeitems_builtins import ShaderNodeCategory


class HWBakeOutputNode(bpy.types.Node):

    '''Bake Output Node'''

    bl_label = "Bake Output Node"
    bl_idname = "HWBakeOutputNode"

    to_vertex_colors: bpy.props.BoolProperty(name="To Vertex Colors")
    image: bpy.props.PointerProperty(
        type=bpy.types.Image,
        name="Pattern",
        update=lambda s, c: s.update_pattern())

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Color")

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


class HWBakeNormalsOutputNode(bpy.types.Node):

    '''Bake Output Node'''

    bl_label = "Bake Output Normals Node"
    bl_idname = "HWBakeNormalsOutputNode"

    to_vertex_colors: bpy.props.BoolProperty(name="To Vertex Colors")
    image: bpy.props.PointerProperty(
        type=bpy.types.Image,
        name="Pattern",
        update=lambda s, c: s.update_pattern())

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
        return "Bake Normals Node"


node_categories = [
    ShaderNodeCategory('HWBAKENODES', "Bake Nodes", items=[
        NodeItem(HWBakeOutputNode.bl_idname),
        NodeItem(HWBakeNormalsOutputNode.bl_idname)
    ])
]
