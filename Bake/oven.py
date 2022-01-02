from bpy import data as D
from math import *
from mathutils import *
from bpy import context as C
from .bake_nodes import HWBakeOutputNode
import random
import bpy


class HWBakeNodesOperator(bpy.types.Operator):
    bl_idname = "object.hwbakenodes"
    bl_label = "Bake All Nodes"

    def execute(self, context):
        for obj in context.selected_objects:
            texture_image_name = 'HWBakedTexture'
            # You can choose your texture size (This will be the de bake image)
            image_name = obj.name + '_BakedTexture'

            #Due to the presence of any multiple materials, it seems necessary to iterate on all the materials, and assign them a node + the image to bake.
            for mat in obj.data.materials:
                for n in mat.node_tree.nodes:
                    if n.bl_idname == HWBakeOutputNode.bl_idname:
                        if len(n.inputs['Color'].links) != 1:
                            continue
                        hitlist = []

                        img = n.image

                        mat.use_nodes = True  # Here it is assumed that the materials have been created with nodes, otherwise it would not be possible to assign a node for the Bake, so this step is a bit useless
                        nodes = mat.node_tree.nodes
                        texture_node = new_emphemeral_node('ShaderNodeTexImage', nodes, hitlist)

                        texture_node.name = texture_image_name
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
                        # old_output_source = output.inputs['Surface'].links[0].from_socket

                        mat.node_tree.links.new(input_socket, emit_node.inputs['Color'])
                        mat.node_tree.links.new(emit_output_socket, output_socket)

                        bpy.ops.object.bake(type='EMIT')

                        clean_up_nodes(nodes, hitlist)

        return {'FINISHED'}


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
