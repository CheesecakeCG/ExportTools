import bpy


class CopyShapeKeysToAttributesOperator(bpy.types.Operator):
    bl_idname = "object.copy_shape_keys_to_attributes"
    bl_label = "Copy Shape Keys To Attributes"

    def execute(self, context):
        for sk in context.active_object.data.shape_keys.key_blocks:
            PreserveShapekeys.copy_shape_keys_to_attributes(context.active_object, sk)
        print(self.bl_label, "executed!")
        return {'FINISHED'}


class CopyAttributesToShapeKeysOperator(bpy.types.Operator):
    bl_idname = "object.copy_attributes_to_shape_keys"
    bl_label = "Copy Attributes To Shape Keys"

    def execute(self, context):
        for at in context.active_object.data.attributes:
            PreserveShapekeys.copy_attributes_to_shape_keys(context.active_object, at)

        print(self.bl_label, "executed!")
        return {'FINISHED'}


class MixdownMeshes(bpy.types.Operator):
    bl_idname = "object.mixdown_meshes"
    bl_label = "Mixdown Meshes"

    def execute(self, context):
        for ob in context.selected_objects:
            for at in context.active_object.data.attributes:
                PreserveShapekeys.copy_attributes_to_shape_keys(context.active_object, at)

            bpy.ops.object.shape_key_remove(all=True)
            for sk in context.active_object.data.shape_keys.key_blocks:
                PreserveShapekeys.copy_shape_keys_to_attributes(context.active_object, sk)

        print(self.bl_label, "executed!")
        return {'FINISHED'}


class PreserveShapekeys():
    def copy_shape_keys_to_attributes(obj, shape_key):
        print(shape_key.name)
        # if not obj is bpy.types.Object:
        #     print("Object does not exist")
        #     return
        # if not shape_key is bpy.types.ShapeKey:
        #     print("Shapekey", shape_key.name, " does not exist")
        #     return
        attribute = obj.data.attributes.new(
            "PV_" + shape_key.name, 'FLOAT_VECTOR', 'POINT')
        i = 0
        for v in shape_key.data:
            # print(i, v.co)
            attribute.data[i].vector = v.co
            i += 1

    def copy_attributes_to_shape_keys(obj, attribute):
        if not attribute.name.startswith("PV_"):
            return
        if attribute.name == "PV_Basis":
            return
        print(attribute.name)
        # if not obj is bpy.types.Object:
        #     print("Object does not exist")
        #     return
        # if not attribute is bpy.types.Attribute:
        #     print("Shapekey", shape_key.name, " does not exist")
        #     return
        shape_key = obj.shape_key_add(
            name=attribute.name.removeprefix("PV_"), from_mix=False)
        i = 0
        for v in attribute.data:
            # print(i, v.vector)
            shape_key.data[i].co = v.vector
            i += 1
