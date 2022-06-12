import bpy


class HWShapekeysPanel(bpy.types.Panel):
    """Shape Keys Tools Panel"""
    bl_label = "Shape Key Handling"
    bl_parent_id = "OBJECT_PT_hwexporttools"
    bl_idname = "OBJECT_PT_hwshapekeysPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.copy_shape_keys_to_attributes")
        row.operator("object.copy_attributes_to_shape_keys")

        layout.operator("object.lossy_modifier_strip")
