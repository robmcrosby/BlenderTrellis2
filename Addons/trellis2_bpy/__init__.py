bl_info = {
    "name": "Trellis2 Blender Plugin",
    "blender": (5, 1, 0),
    "category": "Scene",
}

import bpy
from bpy.types import Operator
from bpy.props import PointerProperty

from .trellis2_modules import get_needed_modules, all_modules_installed, install_modules
from .trellis2_properties import Trellis2Properties
from .trellis2_bpy import loadInputImage, generate3dMeshFrom2dImage, cancelGeneration


class InstallTrellis2Modules(Operator):
  """ Install Modules used by Trellis """
  bl_idname = "scene.install_trellis2_modules"
  bl_label = "Install Modules"
  bl_options = {'REGISTER', 'INTERNAL'}
  
  @classmethod
  def poll(cls, context):
    return True
  
  def execute(self, context):
    install_modules()
    return {'FINISHED'}


class ImportTrellis2ImageOperator(Operator):
  """ Import image for use with Trellis """
  bl_idname = "scene.import_trellis2_image"
  bl_label = "Import Image"
  bl_options = {'REGISTER', 'INTERNAL'}
  
  @classmethod
  def poll(cls, context):
    props = context.scene.trellis2_properties
    return not props.image_file == ''
  
  def execute(self, context):
    props = context.scene.trellis2_properties
    props.image_input = loadInputImage(image_path = props.image_file)
    if not props.image_input == None:
      props.image_file = ''
    return {'FINISHED'}


class GenerateTrellis2MeshOperator(Operator):
  """ Invoke Trellis 2d image to 3d mesh generation """
  bl_idname = "scene.genrate_trellis2_mesh"
  bl_label = "2D Image to 3D Mesh"
  bl_options = {'REGISTER', 'INTERNAL'}
  
  @classmethod
  def poll(cls, context):
    props = context.scene.trellis2_properties
    return props.image_input is not None
  
  def execute(self, context):
    properties = context.scene.trellis2_properties
    generate3dMeshFrom2dImage(properties = properties)
    return {'FINISHED'}


class CancelTrellis2Operation(Operator):
  """ Cancel Trellis Operation """
  bl_idname = "scene.cancel_trellis2_operation"
  bl_label = "Cancel Generation"
  bl_options = {'REGISTER', 'INTERNAL'}
  
  @classmethod
  def poll(cls, context):
    return True
  
  def execute(self, context):
    properties = context.scene.trellis2_properties
    properties.gen_in_progress = False
    cancelGeneration()
    return {'FINISHED'}


class TRELLIS2_preferences(bpy.types.AddonPreferences):
  """ Adds Trellis2 Preferences """
  bl_idname = __name__
  
  def draw(self, context):
    layout = self.layout
    if not all_modules_installed():
      layout.operator(InstallTrellis2Modules.bl_idname, text="Install Dependencies")
    else:
      layout.operator(InstallTrellis2Modules.bl_idname, text="Update Dependencies")


class OBJECT_PT_trellis2_pannel(bpy.types.Panel):
  """ Creates Trellis2 Panel in the Object properties window """
  bl_label = "Trellis2"
  bl_idname = "SCENE_PT_trellis2_pannel"
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = "scene"

  def draw(self, context):
    scene = context.scene
    props = scene.trellis2_properties
    
    layout = self.layout
    if not all_modules_installed():
      layout.row().operator(InstallTrellis2Modules.bl_idname, text="Install Dependencies")
    else:
      layout.label(text="Load Image from File")
      box = layout.box()
      box.row().prop(props, 'image_file')
      box.row().operator(ImportTrellis2ImageOperator.bl_idname, text="Load Input Image")
      layout.separator()
      layout.label(text="Generate Mesh from Image")
      layout.row().prop(props, 'image_input')
      layout.row().prop(props, 'pipeline_type')
      layout.row().prop(props, 'sparse_steps')
      layout.row().prop(props, 'shape_steps')
      layout.row().prop(props, 'texture_steps')
      layout.row().prop(props, 'seed')
      layout.row().prop(props, 'gen_texture')
      layout.row().prop(props, 'centered')
      layout.row().prop(props, 'scale')
      layout.row().prop(props, 'count')
      if props.gen_in_progress:
        box = layout.box()
        box.label(text=props.gen_iteration)
        box.label(text=props.gen_stage)
        box.row().operator(CancelTrellis2Operation.bl_idname, text="Cancel Generation")
      else:
        layout.row().operator(GenerateTrellis2MeshOperator.bl_idname, text="Generate Mesh")


classes = [
  Trellis2Properties,
  InstallTrellis2Modules,
  GenerateTrellis2MeshOperator,
  ImportTrellis2ImageOperator,
  CancelTrellis2Operation,
  TRELLIS2_preferences,
  OBJECT_PT_trellis2_pannel,
]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)
  bpy.types.Scene.trellis2_properties = PointerProperty(type=Trellis2Properties)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)
  del bpy.types.Scene.trellis2_properties


if __name__ == "__main__":
  register()
