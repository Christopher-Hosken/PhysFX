import bpy
import bmesh
from bpy.types import Operator
from modules.funcs import show_message_box

def arrdiff(a, b):
    return (a - b).normalized()

class PhysFXToolsPro_OT_GlueBodies(Operator): 
    bl_label = "Glue"
    bl_idname = 'physfxtoolspro.gluebodies'
    bl_description = "Glue selected rigidbodies together."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        _collection = bpy.context.collection
        _objects = bpy.context.selected_objects
        depsgraph = context.evaluated_depsgraph_get()
        props = context.scene.physfxtoolspro_props

        try:
            bpy.ops.rigidbody.world_add()
        except:
            pass

        if (props.glue_collection):   
            if _collection.name == "Scene Collection":
                show_message_box("Uh oh!", "Cannot glue 'Scene Collection'!", "ERROR")
                return {'CANCELLED'}
            else:
                _objects = _collection.objects
                gluecollectionname = _collection.name + "_glue"
        else:
            gluecollectionname = "_glue"

        gluecollection = bpy.data.collections.get(gluecollectionname)
        if gluecollection is None:
            gluecollection = bpy.data.collections.new(gluecollectionname)

        if gluecollectionname not in _collection:
            _collection.children.link(gluecollection)

        for idx, obj_a in enumerate(_objects):
            if obj_a.type == "MESH":
                mesh_a = depsgraph.objects.get(obj_a.name, None)
                if mesh_a is not None:
                    for __, obj_b in enumerate(_objects[idx+1:]):
                        if obj_b.type == "MESH":
                            mesh_b = depsgraph.objects.get(obj_b.name, None)
                            if mesh_b is not None:
                                try:
                                    is_obj_a_intersection, obj_a_intersection_point = obj_a.ray_cast(obj_a.location - obj_a.location, arrdiff(obj_a.location, obj_b.location))[:2]
                                    is_obj_b_intersection, obj_b_intersection_point = obj_b.ray_cast(obj_b.location - obj_b.location, arrdiff(obj_b.location, obj_a.location))[:2]
                                
                                except RuntimeError:
                                    show_message_box('Uh oh!', 'A Runtime Error occured.', "ERROR")
                                    return {'CANCELLED'}
                                
                                obj_a_intersection_point += obj_b.location
                                obj_b_intersection_point += obj_a.location

                                if (is_obj_a_intersection and is_obj_b_intersection):
                                    print(obj_a.name, obj_b.name)
                                    if (obj_a_intersection_point - obj_b_intersection_point).length_squared <= props.glue_distance:
                                        name = f"Glue-[{obj_a.name}, {obj_b.name}]"
                                        

                                        mesh = bpy.data.meshes.new(name)
                                        constraint_obj = bpy.data.objects.new(name, mesh)
                                        constraint_obj.name = name
                                        constraint_obj.color = (1, 1, 1, 1)
                                        constraint_obj.display_type = 'WIRE'
                                        constraint_obj.show_in_front = True

                                        gluecollection.objects.link(constraint_obj)

                                        context.view_layer.objects.active = constraint_obj

                                        if not constraint_obj.data.is_editmode:
                                            bpy.ops.object.mode_set(mode='EDIT')


                                        constraint_mesh = bmesh.from_edit_mesh(constraint_obj.data)
                                        v1 = constraint_mesh.verts.new(obj_a.location)
                                        v2 = constraint_mesh.verts.new(obj_b.location)
                                        constraint_mesh.edges.new([v1, v2])
                                        bmesh.update_edit_mesh(constraint_obj.data)
                                        constraint_mesh.free()
                                        bpy.ops.object.mode_set(mode='OBJECT')
                                        bpy.ops.rigidbody.constraint_add()
                                        constraint = constraint_obj.rigid_body_constraint
                                        constraint.type = 'FIXED'
                                        constraint.object1 = obj_a
                                        constraint.object2 = obj_b
                                        if (props.breaking_threshold == -1):
                                            constraint.use_breaking = False
                                        else:
                                            constraint.use_breaking = True
                                            constraint.breaking_threshold = props.breaking_threshold
        return {'FINISHED'}

class PhysFXToolsPro_OT_DeleteGlue(Operator):
    bl_label = "Delete Glue"
    bl_idname = 'physfxtoolspro.deleteglue'
    bl_description = "Delete glue constraints inside the active collection."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        collection = context.collection
        self.traverse(collection)
        return {'FINISHED'}

    def traverse(self, collection):
        if len(collection.children) > 0:
            for col in collection.children:
                self.traverse(col)
        else:
            if collection.name.endswith("_glue"):
                for obj in collection.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
                bpy.data.collections.remove(collection)
        return {'FINISHED'}