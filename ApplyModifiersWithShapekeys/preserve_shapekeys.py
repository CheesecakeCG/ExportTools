import re
import bpy
import random

class LossyModifierStrip(bpy.types.Operator):
    bl_idname = "object.lossy_modifier_strip"
    bl_label = "Strip Modifiers keeping Shapekeys (lossy)"

    def execute(self, context):
        for obj in context.selected_objects:
            PreserveShapekeys.strip_modifiers(context, obj)
            context.collection.objects.link(obj)
        print(self.bl_label, "executed!")
        return {'FINISHED'}

class CopyShapeKeysToAttributesOperator(bpy.types.Operator):
    bl_idname = "object.copy_shape_keys_to_attributes"
    bl_label = "Copy Shape Keys To Attributes"

    def execute(self, context):
        for obj in context.selected_objects:
            PreserveShapekeys.copy_all_shape_keys_to_attributes(obj)
        print(self.bl_label, "executed!")
        return {'FINISHED'}


class CopyAttributesToShapeKeysOperator(bpy.types.Operator):
    bl_idname = "object.copy_attributes_to_shape_keys"
    bl_label = "Copy Attributes To Shape Keys"

    def execute(self, context):
        for obj in context.selected_objects:
            PreserveShapekeys.copy_all_attributes_to_shape_keys(obj)


        print(self.bl_label, "executed!")
        return {'FINISHED'}


class MixdownMeshes(bpy.types.Operator):
    bl_idname = "object.mixdown_meshes"
    bl_label = "Mixdown Meshes"

    def execute(self, context):
        for obj in context.selected_objects:
            PreserveShapekeys.strip_modifiers(context, obj)
            

        bpy.ops.object.join()

        print(self.bl_label, "executed!")
        return {'FINISHED'}


class PreserveShapekeys():
    def copy_all_shape_keys_to_attributes(obj):

        if not obj.type == "MESH": return 
        if obj.data.shape_keys is None:
            return
        for sk in obj.data.shape_keys.key_blocks:
            PreserveShapekeys.copy_shape_keys_to_attributes(obj, sk)

    def copy_shape_keys_to_attributes(obj, shape_key):
        if not obj.type == "MESH": return 
        if obj.data.shape_keys is None: return

        print(shape_key.name)

        # if shape_key.name == "Basis":
        #     return
        basis = obj.data.shape_keys.key_blocks[0]

        attribute = obj.data.attributes.new(
            "PV_" + shape_key.name, 'FLOAT_VECTOR', 'POINT')
        i = 0
        for v in shape_key.data:
            # print(i, v.co)
            attribute.data[i].vector = v.co - basis.data[i].co
            i += 1

    def copy_all_attributes_to_shape_keys(obj):
        if not obj.type == "MESH": return 
        for sk in obj.data.attributes:
            PreserveShapekeys.copy_attributes_to_shape_keys(obj, sk)

    def copy_attributes_to_shape_keys(obj, attribute):
        if not obj.type == "MESH": return 
        if not attribute.name.startswith("PV_"):
            return
        # if attribute.name == "PV_Basis":
        #     return

        if obj.data.shape_keys is None:
            obj.shape_key_add(name="HWTMP_Basis", from_mix=False)
        basis = obj.data.shape_keys.key_blocks[0]

        print(attribute.name)
        # if not obj is bpy.types.Object:
        #     print("Object does not exist")
        #     return
        # if not attribute is bpy.types.Attribute:
        #     print("Shapekey", shape_key.name, " does not exist")
        #     return
        shape_key = obj.shape_key_add(name=attribute.name.removeprefix("PV_"), from_mix=False)
        i = 0
        for v in attribute.data:
            # print(i, v.vector)
            shape_key.data[i].co = v.vector + basis.data[i].co
            i += 1

        if basis.name == "HWTMP_Basis":
            obj.shape_key_remove(basis)

    # TODO make this not crash blender
    def strip_modifiers(context, src_obj):
        if not src_obj.type == "MESH": return 
        obj = src_obj.copy()
        obj.data = src_obj.data.copy()
        context.collection.objects.link(obj)
        print("Backing up shapekeys...")
        PreserveShapekeys.copy_all_shape_keys_to_attributes(obj)

        print("Clearing shapekeys...")
        obj.shape_key_clear()

        print("Evaluating mesh...")
        PreserveShapekeys.apply_modifiers_on_object(context, obj)

        print("Restoring backup...")
        PreserveShapekeys.copy_all_attributes_to_shape_keys(obj)

        print("Returning Object!", obj.name)
        return obj
    
    
    def apply_modifiers_on_object(context, obj):
        for mod in obj.modifiers:
            try:
                bpy.ops.object.modifier_apply({'object': obj}, modifier=mod.name)
            except:
                print("Failed to apply modifier", mod.name)
        context.view_layer.update()

  
