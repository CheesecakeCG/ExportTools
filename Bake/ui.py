import bpy


class HWBakePanel(bpy.types.Panel):
    """Bake Panel"""
    bl_label = "Bake"
    bl_parent_id = "OBJECT_PT_hwexporttools"
    bl_idname = "OBJECT_PT_hwbakepanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        self.layout.operator("object.hwbakenodes")
