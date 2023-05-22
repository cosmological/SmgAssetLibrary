import bpy
import os

#Change this name for each world
course_list_file = 'World1Stages'

course_text_file = 'Collectables'

# Get the current working directory of the script
cwd = bpy.path.abspath("//")
course_text_file_path = bpy.path.abspath("//SMG2_Courses")
#course_text_file_path = bpy.path.abspath("//CommonItems")


scene_collection = bpy.context.scene.collection

#If you want to import all assets at once you can uncomment lines 22-25 and comment out lines 27-31.
#NOTE: This will take a VERY LONG time to import especially on a low end computer
#Blender will use ~6GB of RAM to complete this operation
#The final .blend file you'll export will be ~1.2GB as well

#for filename in os.listdir(course_text_file_path):
#    if filename.endswith(".txt"):
#        #set the current course name to the filename
#        course_text_file = filename.split(".")[0]

with open(r'{0}.txt'.format(course_list_file), 'r') as course_list:
    for course in course_list:
        if course.strip() == "":
            continue
        course_text_file = course.strip()
        
        #modified from Blender.Stackexchange user Gorgioius 
        #Thread: https://blender.stackexchange.com/questions/249316/python-set-asset-library-tags-and-catalogs
        #open blender_assets.cats.txt to get the UUIDs of each catalog 
        uuid = None
        with open ('blender_assets.cats.txt') as asset_lib_file:
            for line in asset_lib_file:
                if line.startswith(("#", "VERSION", "\n")):
                    continue
                catalog_name = line.split(":")[2].split("\n")[0]
                if course_text_file in catalog_name:
                    uuid = line.split(":")[0]
                    

        #load each .txt file
        with open(r'{0}\{1}.txt'.format(course_text_file_path, course_text_file), 'r') as text_file:
            #create a new collection for imported objects from the text file
            new_collection = bpy.data.collections.new(course_text_file)
            scene_collection.children.link(new_collection)
            bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[course_text_file]
            
            #loop through each object defined in the .txt file
            for line in text_file:
                dae_file_name = line.strip()
                #check for empty line
                if dae_file_name == "":
                    continue

                # dae_file_name = 'Mario'
                dae_file_path = bpy.path.abspath(r'//SMG2-Extracts/ObjectData/{0}/{0}.dae'.format(dae_file_name))
                print(dae_file_path)
                

                bpy.ops.object.select_all(action='DESELECT')


                #create the new collection with name
                collection_name = dae_file_name
                collection = bpy.context.blend_data.collections.new(name=collection_name)
                bpy.context.collection.children.link(collection)

                #import the .dae mesh into a new collection
                bpy.ops.wm.collada_import(filepath=dae_file_path,
                                        auto_connect = True, 
                                        find_chains = True, 
                                        fix_orientation = True)

                for obj in bpy.context.selected_objects:
                    bpy.data.collections[collection_name].objects.link(obj)


                #delete the skeleton_root object from the armature
                for obj in collection.objects:
                    if 'skeleton_root' in obj.name:
                        bpy.data.objects.remove(obj, do_unlink=True)

                #now the collection is full of meshes from the .dae

                #clear the selection
                bpy.ops.object.select_all(action='DESELECT')


                for obj in collection.objects:
                    #Remove the armature modifier from each mesh    
                    obj.select_set(True)
                    for mod in obj.modifiers:
                        obj.modifiers.remove(mod)
                    #Set the name of the UV Map of each mesh to be the same for merging
                    for uvmap in obj.data.uv_layers:
                        uvmap.name = "UVMap"
                    for col in obj.data.vertex_colors:
                        col.name = "col0"
                        
                #join the meshes together
                bpy.ops.object.join()
                current_mesh = bpy.context.active_object

                #Rotate the mesh on the x-axis by 90, scale it to .01, reset transforms, and rename mesh
                current_mesh.rotation_euler[0] = 1.5708
                current_mesh.scale = (0.01, 0.01, 0.01)
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                current_mesh.name = dae_file_name
                
                #Modify the materials 
                for mat_slot in current_mesh.material_slots:
                    mat = mat_slot.material
                    mat.blend_method = 'CLIP'
                    mat.shadow_method = 'CLIP'
                    
                    if mat is None:
                        continue

                    nodes = mat.node_tree.nodes
                    links = mat.node_tree.links
                    
                    #Get the Principled BSDF Node            
                    bsdf = nodes.get("Principled BSDF")

                    # Create the new nodes for MixRGB and Attribute
                    mix_node = nodes.new('ShaderNodeMixRGB')
                    mix_node.blend_type = 'MULTIPLY'
                    mix_node.inputs['Fac'].default_value = 1.0

                    attr_node = nodes.new('ShaderNodeAttribute')
                    attr_node.attribute_name = 'col0'
                    
                    # Get the existing base color and link it to the mix node
                    base_color = None
                    for node in nodes:
                        if node.type == 'TEX_IMAGE':
                            base_color = node.outputs['Color']
                            alpha_channel = node.outputs['Alpha']
                            break
                    
                    if base_color is None:
                        print("No image texture found")
                        continue
                    
                    # Link the nodes together
                    links.new(attr_node.outputs['Color'], mix_node.inputs['Color1'])
                    
                    links.new(base_color, mix_node.inputs['Color2'])
                    links.new(alpha_channel, bsdf.inputs['Alpha'])
                    
                    links.new(base_color, mix_node.inputs['Color2'])
                    links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])
                
                #Add new mesh to asset library
                current_mesh.asset_mark()
                if uuid is not None:
                    asset_data = current_mesh.asset_data
                    asset_data.catalog_id = uuid
                
                #Set the preview image to a render of the object
                bpy.ops.ed.lib_id_generate_preview({"id": current_mesh})

 
#Remove all duplicate materials after import
#This code is modified from user "liero" on this thread: https://blenderartists.org/t/eliminate-duplicate-materials-001-002-003-after-append/373855/11
mats = bpy.data.materials

for obj in bpy.data.objects:
    #Loops through each material slot of the object
    for slt in obj.material_slots:
        #Get the current material in the slot
        orig_mat = bpy.data.materials.get(slt.name)
        #Split the material name by '.'
        part = slt.name.rpartition('.')
        #if the second half is a number (eg. 001) and first half is an existing material then its a duplicate
        if part[2].isnumeric() and part[0] in mats:
            #assign the slot material to the original material
            slt.material = mats.get(part[0])
            #remove the duplicate material
            bpy.data.materials.remove(orig_mat)
