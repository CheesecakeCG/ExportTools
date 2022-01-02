import bpy


class HWExportTools(bpy.types.Panel):
    """Main ExportTools Panel"""
    bl_label = "ExportTools"
    bl_idname = "OBJECT_PT_hwexporttools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("object.copy_attributes_to_shape_keys")
        row = layout.row()
        row.operator("object.copy_shape_keys_to_attributes")
