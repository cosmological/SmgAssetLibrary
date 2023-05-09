# SmgAssetLibrary
A simple repository with various scripts to automatically export SMG/SMG2 models and import them in Blender's asset library

Features:
- Automatically imports all .dae objects from a text file 
- Removes the skeleton root, and the modifiers
- Merges all of the component meshes with their UV Maps and Vertex Color data
- Scales and rotates the mesh for better use in Blender
- Fixes the materials to have proper opacity, and vertex coloring
- Adds the objects to the Asset Library and generates a preview image for them
- Removes duplicate materials from scene

Initial Setup:
- The scripts in this repo use relative filepaths and are looking for files that cannot be distributed
- ExtractArcs.ps1 expects various things to be copied into this repository
    - Install of WiiExplorer at the location: SmgAssetLibrary/WiiExplorer/WiiExplorer.exe 
        - Note: There is a new version of WiiExplorer that fixes a bug necessary for this script to work
    - Install of SuperBMD at the location SmgAssetLibrary/SuperBMD/SuperBMD.exe
    - The exported ObjectData from a Super Mario Galaxy 2 .iso located at SmgAssetLibrary/SMG2-Extracts/ObjectData
        - You can do this in Dolphin
    - If you already have these files/programs located elsewhere on your computer you can modify the variables within ExtractArcs.ps1
        - $arcExtractsFolderPath 
        - $wiiExplorerPath 
        - $superBmdPath 
- BlenderImportDae.py
    - If you modified the locations of any of the exported files in ExtractArcs.ps1 then you'll need to modify these variables
        - dae_file_path <- This must be the same as $arcExtractsFolderPath in ExtractArcs.ps1

Running the scripts:
- Open Powershell to this directory and run .\ExtractArcs.ps1
    - Depending on how powerful your machine is this might take a while
    - I (cosmological) have an R9 3900X and it took around 40 minutes
- Open SmgAssetLibrary.blend
    - This was tested in Blender 3.5.0
    - Open BlenderImportDae.py in the Scripting window and run the script
    - After a while you should have a .blend file with all of the Galaxy 2 assets sorted by course
        - One course will be created for each .txt file in the SMG2_Courses directory
    - Save the .blend in your 

Planned Features:
- Complete lists for SMG2 courses
- Common objects files
- SMG1 Support
- Add materials to asset library