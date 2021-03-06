from bpy import data as D
from math import *
from mathutils import *
from bpy import context as C
from .bake_nodes import HWBakeOutputNode, HWBakeNormalsOutputNode
import random
import bpy


class HWBakeAllNodesOperator(bpy.types.Operator):
    bl_idname = "object.hwbake_all_nodes"
    bl_label = "Bake All Nodes In Selected Objects"

    def execute(self, context):
        already_baked = []
        for obj in context.selected_objects:
            for mat in obj.data.materials:
                if already_baked.count(mat) != 0:
                    print("Skipping " + mat.name + " because it's already been baked.")
                    continue
                already_baked.append(mat)
                for n in mat.node_tree.nodes:
                    bake_node(n, mat)
                    bake_normal_node(n, mat)

        return {'FINISHED'}


def bake_node(n, mat):
    if n.bl_idname != HWBakeOutputNode.bl_idname:
        return
    if len(n.inputs['Color'].links) != 1:
        return
    if n.mute:
        return
    hitlist = []

    img = n.image

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    texture_node = new_emphemeral_node('ShaderNodeTexImage', nodes, hitlist)

    texture_node.select = True
    nodes.active = texture_node
    texture_node.image = img  # Assign the image to the node

    emit_node = new_emphemeral_node('ShaderNodeEmission', nodes, hitlist)
    emit_output_socket = emit_node.outputs['Emission']
    input_socket = n.inputs['Color'].links[0].from_socket
    old_ouput = get_active_output(nodes)
    output = new_emphemeral_node('ShaderNodeOutputMaterial', nodes, hitlist)
    output_socket = output.inputs['Surface']
    set_as_active_output(output)

    mat.node_tree.links.new(input_socket, emit_node.inputs['Color'])
    mat.node_tree.links.new(emit_output_socket, output_socket)

    bpy.ops.object.bake(type='EMIT')

    clean_up_nodes(nodes, hitlist)


def bake_normal_node(n, mat):
    if n.bl_idname != HWBakeNormalsOutputNode.bl_idname:
        return
    if n.mute:
        return
    hitlist = []

    img = n.image

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    texture_node = new_emphemeral_node('ShaderNodeTexImage', nodes, hitlist)

    texture_node.select = True
    nodes.active = texture_node
    texture_node.image = img  # Assign the image to the node

    bpy.ops.object.bake(type='NORMAL')

    clean_up_nodes(nodes, hitlist)


def set_as_active_output(my_node):
    nodes = my_node.id_data.nodes
    for node in nodes:
        if node.type == 'OUTPUT_MATERIAL':
            node.is_active_output = False
        my_node.is_active_output = True


def get_active_output(nodes):
    for node in nodes:
        if node.type == 'OUTPUT_MATERIAL' and node.is_active_output:
            return node
    for node in nodes:
        if node.type == 'OUTPUT_MATERIAL':
            return node


def new_emphemeral_node(type_name, nodes, hitlist):
    node = nodes.new(type_name)
    node.name = str(random.getrandbits(16))
    hitlist.append(node)
    return node


def clean_up_nodes(nodes, hitlist):
    for n in nodes:
        if n in hitlist:
            nodes.remove(n)
