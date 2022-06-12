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
        if obj.data.shape_keys is None:
            return
        for sk in obj.data.shape_keys.key_blocks:
            PreserveShapekeys.copy_shape_keys_to_attributes(obj, sk)

    def copy_shape_keys_to_attributes(obj, shape_key):
        print(shape_key.name)
        # if not obj is bpy.types.Object:
        #     print("Object does not exist")
        #     return
        # if not shape_key is bpy.types.ShapeKey:
        #     print("Shapekey", shape_key.name, " does not exist")
        #     return
        if shape_key.name == "Basis":
            return
        basis = obj.data.shape_keys.key_blocks["Basis"]

        attribute = obj.data.attributes.new(
            "PV_" + shape_key.name, 'FLOAT_VECTOR', 'POINT')
        i = 0
        for v in shape_key.data:
            # print(i, v.co)
            attribute.data[i].vector = v.co - basis.data[i].co
            i += 1

    def copy_all_attributes_to_shape_keys(obj):
        for sk in obj.data.attributes:
            PreserveShapekeys.copy_attributes_to_shape_keys(obj, sk)

    def copy_attributes_to_shape_keys(obj, attribute):
        if not attribute.name.startswith("PV_"):
            return
        if attribute.name == "PV_Basis":
            return

        if obj.data.shape_keys is None:
            obj.shape_key_add(name="Basis", from_mix=False)
        basis = obj.data.shape_keys.key_blocks["Basis"]

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

    # TODO make this not crash blender
    def strip_modifiers(context, src_obj):
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

        print("Returning Object!")
        return obj
    
    
    def apply_modifiers_on_object(context, obj):
        for mod in obj.modifiers:
            try:
                bpy.ops.object.modifier_apply({'object': obj}, modifier=mod.name)
            except:
                print("Failed to apply modifier", mod.name)
        context.view_layer.update()

    def eeeapply_modifiers(context, obj):

        # Depsgraph
        depsgraph = bpy.context.evaluated_depsgraph_get()

        # Get modified object
        eval_obj = obj.evaluated_get(depsgraph)
        # new_ob = eval_obj.copy()
        # new_ob.data = eval_obj.to_mesh().copy()
        return bpy.data.objects.new("new", eval_obj.data.copy())

    def eeapply_modifiers(context, obj):
        dg = context.evaluated_depsgraph_get()

        new_obj = dg.objects.get(obj.name).copy()
        mesh = new_obj.to_mesh().copy()

        new_obj.data = mesh

        new_obj.modifiers.clear()

        return new_obj
    def eapply_modifiers(context, src_obj):
        
        print("Applying modifiers on ", src_obj.name, "...")
        # bpy.ops.object.convert(target='MESH', context={'selected_objects': [obj]})
        obj = src_obj.copy()
        obj.data = src_obj.data.copy()
        
        
        
        # Object must be in a collection for this to work
        temp_collection = bpy.data.collections.new("Temp Coll for Applying mods " + str(random.randint(0, 10000)))
        temp_collection.objects.link(obj) 
        dg = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(dg)
        # new_obj = bpy.data.objects.new("new", eval_obj.data.copy())
        new_obj = obj.copy()
        new_obj.data = eval_obj.to_mesh().copy()

        new_obj.modifiers.clear()
        temp_collection.objects.unlink(obj)
        
        bpy.data.collections.remove(temp_collection)        
        
        return new_obj

