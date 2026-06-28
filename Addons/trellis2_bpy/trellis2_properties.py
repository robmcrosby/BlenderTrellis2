
import bpy
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty, EnumProperty, PointerProperty


def get_pipeline_types(self, context):
  return [
    ('512', '512', 'Generate Mesh from 512x512 Image'),
    ('1024', '1024', 'Generate Mesh from 1024x1024 Image'),
    ('1024_cascade', '1024 Cascade', 'Generate Mesh using both 512 and 1024 Images')
  ]


class Trellis2Properties(PropertyGroup):
  image_file: StringProperty(name='Image File', default='', subtype='FILE_PATH')
  image_input: PointerProperty(name='Image Input', type=bpy.types.Image, description='Input Image')
  pipeline_type: EnumProperty(name='Pipeline Type', items=get_pipeline_types, default=0)
  sparse_steps: IntProperty(name='Sparse Struture Steps', default=12, min=1)
  shape_steps: IntProperty(name='Shape Slat Steps', default=12, min=1)
  texture_steps: IntProperty(name='Texture Slat Steps', default=12, min=1)
  seed: IntProperty(name='Seed', default=42)
  centered: BoolProperty(name='Centered', default=True)
  scale: FloatProperty(name='Scale', default=1.0)
  count: IntProperty(name='Batch Size', default=1, min=1)
  gen_texture: BoolProperty(name='Generate Texture', default=True)
  
  gen_in_progress: BoolProperty(name='Generation in Progress', default=False)
  gen_iteration: StringProperty(name='Generation Iteration', default='')
  gen_stage: StringProperty(name='Generation Stage', default='')
