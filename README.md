# Blender TRELLIS.2 Add-On
This Blender plug-in implements a stripped down version of Microsoft's TRELLIS.2 for local AI mesh generation on either Apple Silicon or Nvidia Cuda hardware. This plug-in uses the TRELLIS.2 pipeline to produce high density point clouds which are then furter processed by Blender's geometry nodes to produce dense quad meshes much like a high poly sculpt.

## Requirements

- Blender 5.1.0+
- Apple Silicon (M1 or later) or Nvidia Cuda compatable video card
- 24GB+ unified memory for Apple or 16GB+ video memory
- ~15GB disk space for model weights

## Quick Start

### Log into HuggingFace
Before installing the plug-in you will need to log into HuggingFace to setup an access token on your machine and to request access to Facebooks's DINOv3 model at the address bellow. This plug-in utilizes huggingface_hub to manage downloading of models and will fail to download this model if access is not setup correctly.
https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m

### Setup/Activate the Environment (Not needed for MacOS)
The plug-in requires an enviroment to installed aditional python modules such as torch, torchvision, and etc.. This enviroment appears to be automatic to Blender on MacOS but not so with on Linux, so the following console commands need to be run in the directory where the blender application is involked.
```bash
# Setup the inital python virtual environment
python -m venv .venv

# Activate each time before running Blender in the console
source .venv/bin/activate
```

### Plug-in installation
The easiest method of installation is done by downloading trellis2_bpy.zip from the root directory of the repository, then navigating to Edit->Prefrences in blender then at the top right on Add-ons select Install from Disk... Select the zip file to add the Trellis2 Blender Plugin.
An alternative mehtod would involve cloning this repository locally and adding the Addons directory to the Script Directories under Filepaths in Prefrences.

### Installing Required Python Modules
A number of python modules such as torch, torchvision, pillow, and huggingface_hub are needed to run mesh generation. Expanding the Trellis2 Blender Plugin should reveal an Install Dependencies button which when pressed will start installing the modules needed. This can take some time to complete.

### First Time Mesh Generation Run
First download the Suzanne.png image from the Example directory on this repository then find the Trellis2 section under the Scene Pannel. Under the Load Image from File, use the file dialog to locate the Suzanne.png file and press the Load Input Image button. This action will resize the selected image to 1024x1024 pixels and use a model to remove the background. When done the now internal image will be populated to Input Image in the next section bellow.
Next with the default settings, press the Generate Mesh button at the bottom of the Generate Mesh from Image section. On the first run, this will start downloading the models used by the Trellis2 pipeline which can take a considerable amount of time. If everything downloads, the image to mesh pipeline should load and generate a mesh for you. Additional runs should take much less time once the models are downloaded.

### Additional Mesh Generations
At this point this plug-in should be fully installed with the models used by the pipeline loaded to the respective hardware until quiting the Blender application. On subsequent first time mesh genrations the plug-in has to re-load the models and will keep them loaded for quicker mesh generations until quitting Blender. Be aware that keeping these models loaded holds up a lot of resources on your machine and quitting your blender session should clear them up.

## Example Project
Included in this respository is an example blender project with a generated suzanne mesh that can be viewed without installing this plug-in. Inside this project are geometry nodes used to convert the generated dense point cloud to quad meshes. These geometry nodes make use of the new SDF grid nodes in several methods to create quad meshes from points. These nodes could be quite useful on other applications in converting points to meshes outside of mesh generation using Trellis. 
