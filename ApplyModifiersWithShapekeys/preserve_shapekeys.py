import bpy


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
            PreserveShapekeys.copy_all_shape_keys_to_attributes(obj)

            # context.active_object = ob
            # bpy.ops.object.shape_key_remove(all=True)

        bpy.ops.object.convert(target='MESH')

        for obj in context.selected_objects:
            PreserveShapekeys.copy_all_attributes_to_shape_keys(obj)

        bpy.ops.object.join()

        print(self.bl_label, "executed!")
        return {'FINISHED'}


class PreserveShapekeys():
    def copy_all_shape_keys_to_attributes(obj):
        for sk in obj.data.shape_keys.key_blocks:
            PreserveShapekeys.copy_shape_keys_to_attributes(context.active_object, sk)

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
        for sk in obj.data.shape_keys.key_blocks:
            PreserveShapekeys.copy_shape_keys_to_attributes(obj, sk)

    def copy_attributes_to_shape_keys(obj, attribute):
        if not attribute.name.startswith("PV_"):
            return
        if attribute.name == "PV_Basis":
            return
        basis = obj.data.shape_keys.key_blocks["Basis"]
        if basis is None:
            basis = obj.shape_key_add(name="Basis", from_mix=False)
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
