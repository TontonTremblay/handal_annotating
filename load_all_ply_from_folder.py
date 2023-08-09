# exec(compile(open("/home/jtremblay/code/handal_annotating/load_all_ply_from_folder.py").read(), "/home/jtremblay/code/handal_annotating/load_all_ply_from_folder.py", 'exec'))

import bpy
import os

def import_ply_files(folder_path):
    print(folder_path)
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".ply"):
                filepath = os.path.join(root, filename)
                print(filepath)
                bpy.ops.import_mesh.ply(filepath=filepath)
                object_name = filepath.replace(folder_path, "")
                
                # Rename the imported object
                if bpy.context.selected_objects:
                    imported_object = bpy.context.selected_objects[0]
                    imported_object.name = object_name.replace('.ply', '').replace("models_simplified", '')
                    imported_object.hide_viewport = True  # Hide in the viewport
                    imported_object.hide_render = False                     
                    # return
# Set the path to your folder containing PLY files
folder_path = "/home/jtremblay/code/handal_annotating/missing_part_meshes/"


# Import PLY files from subfolders
import_ply_files(folder_path)