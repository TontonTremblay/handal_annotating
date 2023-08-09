# exec(compile(open("/home/jtremblay/code/handal_annotating/menu.py").read(), "/home/jtremblay/code/handal_annotating/menu.py", 'exec'))

import bpy
import bmesh 

class OBJECT_PT_coloring(bpy.types.Panel):
    bl_label = "Handal Annotation"
    bl_idname = "OBJECT_PT_coloring"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.switch_to_edit_mode")
        layout.operator("object.color_save")

class OBJECT_OT_switch_to_edit_mode(bpy.types.Operator):
    bl_idname = "object.switch_to_edit_mode"
    bl_label = "Select Next Object"
    
    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                break
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        obj.hide_viewport = False  # Hide in the viewport
        obj.hide_render = False                     

        # Start vertex edit 
        bpy.ops.object.mode_set(mode='EDIT')
        
                
        return {'FINISHED'}

import os 

class OBJECT_OT_color_save(bpy.types.Operator):
    bl_idname = "object.color_save"
    bl_label = "Color and Save"
    
    

    def execute(self, context):
        def export(output_folder,obj):

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            try:
                base_path = os.path.splitext(output_folder+obj.name+'.ply')[0]
                base_path = '/'.join(base_path.split("/")[:-1])
                os.makedirs(base_path,exist_ok=True)
            except:
                pass
            bpy.ops.export_mesh.ply(filepath=output_folder+obj.name+'.ply', 
                use_selection=True
            )

        path = '/home/jtremblay/code/handal_annotating/output/'
        color=(0.0, 1.0, 0.0, 1.0)
        mesh = bpy.context.view_layer.objects.active
        old_name = mesh.name
        bpy.ops.mesh.separate(type='SELECTED')
        handle = bpy.context.view_layer.objects.active
        handle.name = handle.name.replace('.','')+'_n'
        not_handle = bpy.data.objects.get(old_name+".001")
        not_handle.name = old_name.replace('.','') +'_h'      

        bpy.ops.object.mode_set(mode='OBJECT')

        export(path,not_handle)
        export(path,handle)

        bpy.ops.object.select_all(action='DESELECT')
        not_handle.select_set(True)
        bpy.ops.object.delete()

        bpy.ops.object.select_all(action='DESELECT')
        handle.select_set(True)
        bpy.ops.object.delete()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_PT_coloring)
    bpy.utils.register_class(OBJECT_OT_switch_to_edit_mode)
    bpy.utils.register_class(OBJECT_OT_color_save)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_coloring)
    bpy.utils.unregister_class(OBJECT_OT_switch_to_edit_mode)
    bpy.utils.unregister_class(OBJECT_OT_color_save)

if __name__ == "__main__":
    register()
