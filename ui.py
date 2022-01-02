import bpy


class HWExportToolsPanel(bpy.types.Panel):
    """Main ExportTools Panel"""
    bl_label = "ExportTools"
    bl_idname = "OBJECT_PT_hwexporttools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        pass
