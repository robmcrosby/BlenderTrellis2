
import sys
import os

import threading
import queue

os.environ.setdefault("ATTN_BACKEND", "sdpa")
os.environ.setdefault("SPARSE_ATTN_BACKEND", "sdpa")
try:
    import flex_gemm  # noqa: F401
    os.environ.setdefault("SPARSE_CONV_BACKEND", "flex_gemm")
except ImportError:
    os.environ.setdefault("SPARSE_CONV_BACKEND", "none")
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import bpy
from pathlib import Path
from random import randint

from .trellis2_properties import Trellis2Properties
from .custom_nodes import get_sdf_points_to_mesh_node_group, get_vertex_bsdf_material

SESSION_CACHE = {}


def getDevice():
  import torch
  if torch.cuda.is_available():
    return torch.device("cuda")
  elif torch.backends.mps.is_available():
    return torch.device("mps")
  return 'cpu'


def getTrellis2ImageToBpyPipeline():
  import torch
  from .pipelines.trellis2_image_to_bpy import Trellis2ImageToBpyPipeline
  if not 'pipeline' in SESSION_CACHE:
    print("\nLoading pipeline...")
    pipeline = Trellis2ImageToBpyPipeline.from_pretrained("microsoft/TRELLIS.2-4B")
    
    device = getDevice()
    print("Load pipeline to device:", device)
    pipeline.to(device)
    
    #pipeline.to(torch.device("mps"))
    SESSION_CACHE['device'] = device
    SESSION_CACHE['pipeline'] = pipeline
    
  return SESSION_CACHE['pipeline']


def getTaskQueue():
  if not 'task_queue' in SESSION_CACHE:
    SESSION_CACHE['task_queue'] = queue.Queue()
  elif SESSION_CACHE['task_queue'] == None:
    SESSION_CACHE['task_queue'] = queue.Queue()
  return SESSION_CACHE['task_queue']


def loadBpyImage(image_path):
  try:
    return bpy.data.images.load(image_path, check_existing=True)
  except RuntimeError:
    print('Error Loading Image:', image_path)
  return None


def copyBpyImage(image, name):
  image = image.copy()
  image.name = name
  return image


def deleteBpyImage(image):
  if image.name in bpy.data.images:
    bpy.data.images.remove(image)


def bpyToPillowImage(image):
  pixels = [int(px * 255) for px in image.pixels[:]]
  bytes_data = bytes(pixels)
  size = (image.size[0], image.size[1])
  
  from PIL import Image as PILImage
  return PILImage.frombytes('RGBA', size, bytes_data).transpose(PILImage.FLIP_TOP_BOTTOM)

def writePillowToBpyImage(pil_image, bpy_image):
  from PIL import Image as PILImage
  pil_image = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)
  raw_pixels = list(pil_image.getdata())
  pixels = []
  for r, g, b, a in raw_pixels:
    pixels.extend([r / 255.0, g / 255.0, b / 255.0, a / 255.0])
  bpy_image.pixels.foreach_set(pixels)
  bpy_image.update()


def pillowToBpyImage(pil_image, name):
  width, height = pil_image.size
  bpy_image = bpy.data.images.new(
    name=name,
    width=width,
    height=height,
    alpha=True
  )
  writePillowToBpyImage(pil_image, bpy_image)
  return bpy_image
  

def imageHasBackground(pil_image):
  import numpy as np
  alpha = np.array(pil_image)[:, :, 3]
  return np.all(alpha == 255)


def removeBackground(pil_image):
  from rembg import remove
  return remove(pil_image)


def preprocessBpyImage(image, name):
  image.scale(1024, 1024)
  image.update()
  
  pil_image = bpyToPillowImage(image)
  if imageHasBackground(pil_image):
    pil_image = removeBackground(pil_image)
  
  bpy_image = pillowToBpyImage(pil_image, name)
  bpy_image.pack()
  return bpy_image


def loadPreprocessedImage(image_path):
  # Return existing preprocessed image
  name = Path(image_path).stem
  if name in bpy.data.images:
    return bpyToPillowImage(bpy.data.images[output_name])
  
  # Load new image
  src_image = loadBpyImage(image_path)
  # Return None if failed to load
  if src_image == None:
    return None
  
  # Preprocess to copy and cleanup original
  image = preprocessBpyImage(src_image, name)
  deleteBpyImage(src_image)
  return bpyToPillowImage(image)
  

def getSocketIdentifier(name, node_group):
  for item in node_group.interface.items_tree:
    if item.item_type == 'SOCKET' and item.name == name:
      return item.identifier
  return None


def loadInputImage(image_path):
  # Load new image
  src_image = loadBpyImage(image_path)
  if src_image == None:
    return None
  
  # Remove older image if present
  name = Path(image_path).stem
  if name in bpy.data.images:
    deleteBpyImage(bpy.data.images[name])
  
  image = preprocessBpyImage(src_image, name)
  deleteBpyImage(src_image)
  return image


def runMeshGeneration():
  task_queue = getTaskQueue()
  count = SESSION_CACHE['count']
  index = SESSION_CACHE['index']
  
  image = SESSION_CACHE['image_input']
  seed = randint(0, 10000000) if count > 1 else SESSION_CACHE['seed']
  pipeline_type = SESSION_CACHE['pipeline_type']
  sparse_overrides = SESSION_CACHE['sparse_overrides']
  shape_overrides = SESSION_CACHE['shape_overrides']
  texture_overrides = SESSION_CACHE['texture_overrides']
  gen_texture = SESSION_CACHE['gen_texture']
  cancel_signal = SESSION_CACHE['cancel_signal']
  
  pipeline = getTrellis2ImageToBpyPipeline()
  outputs = pipeline.run(
    image,
    seed = seed,
    pipeline_type = pipeline_type,
    sparse_structure_sampler_params = sparse_overrides,
    shape_slat_sampler_params = shape_overrides,
    tex_slat_sampler_params = texture_overrides,
    gen_texture = gen_texture,
    task_queue = task_queue,
    cancel_signal = cancel_signal,
  )
  task_queue.put({'outputs':outputs, 'seed':seed, 'index':index})


def startMeshGenerationThread():
  thread = threading.Thread(target=runMeshGeneration)
  thread.daemon = True
  thread.start()


def redrawPanels():
  for screen in bpy.data.screens:
    for area in screen.areas:
      if area.type == 'PROPERTIES':
        area.tag_redraw()


def checkMeshGeneration():
  task_queue = getTaskQueue()
  if not task_queue.empty():
    data = task_queue.get()
    properties = SESSION_CACHE['properties']
    
    if 'stage' in data:
      stage = data['stage']
      step = data['step']
      steps = data['steps']
      properties.gen_stage = f'stage {step} of {steps} : {stage}'
      #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
      redrawPanels()
    elif 'outputs' in data:
      outputs = data['outputs']
      seed = data['seed']
      index = data['index']
      
      if not outputs:
        return None
      
      output_name = SESSION_CACHE['output_name']
      batch_count = SESSION_CACHE['count']
      centered = SESSION_CACHE['centered']
      scale = SESSION_CACHE['scale']
      
      obj_name = f'{output_name}_{seed}' if batch_count > 1 else output_name
      
      properties.gen_stage = 'Loading Mesh to Blender'
      
      verts = outputs[0]
      mesh_data = bpy.data.meshes.new(obj_name+'_mesh')
      mesh_data.from_pydata(verts, [], [])
      
      if len(outputs) > 1:
        attrs = outputs[1]
        
        vertex_colors = attrs[:,:4].tolist()
        color_attr = mesh_data.color_attributes.new(name="Color", type='FLOAT_COLOR', domain='POINT')
        for i, datum in enumerate(color_attr.data):
          datum.color = vertex_colors[i]
        
        vertex_metallic = attrs[:,3].tolist()
        attr_metallic = mesh_data.attributes.new(name='Metallic', type='FLOAT', domain='POINT')
        for i, datum in enumerate(attr_metallic.data):
          datum.value = vertex_metallic[i]
        
        vertex_roughness = attrs[:,4].tolist()
        attr_roughness = mesh_data.attributes.new(name='Roughness', type='FLOAT', domain='POINT')
        for i, datum in enumerate(attr_roughness.data):
          datum.value = vertex_roughness[i]
        
        vertex_opacity = attrs[:,5].tolist()
        attr_opacity = mesh_data.attributes.new(name='Opacity', type='FLOAT', domain='POINT')
        for i, datum in enumerate(attr_opacity.data):
          datum.value = vertex_opacity[i]
      
      mesh_data.update()
      
      # Create new object for mesh
      new_object = bpy.data.objects.new(obj_name, mesh_data)
      bpy.context.collection.objects.link(new_object)
      
      # Add points to mesh geometry nodes modifiter
      modifier = new_object.modifiers.new(name="PointsToMesh", type='NODES')
      modifier.node_group = get_sdf_points_to_mesh_node_group()
      
      material_socket = getSocketIdentifier('Material', modifier.node_group)
      modifier[material_socket] = get_vertex_bsdf_material()
      
      centered_socket = getSocketIdentifier('Centered', modifier.node_group)
      modifier[centered_socket] = centered
      
      scale_socket = getSocketIdentifier('Scale', modifier.node_group)
      modifier[scale_socket] = scale
      
      mesh_data.update()
      
      if batch_count > 1:
        new_object.location.x = (index - (batch_count-1.0)*0.5)*scale
      
      index += 1
      if index < batch_count:
        # Start new mesh generation thread
        SESSION_CACHE['index'] = index
        properties.gen_iteration = f'Generating Mesh {1+index} of {batch_count}' if batch_count > 1 else 'Generating Mesh'
        properties.gen_stage = ''
        startMeshGenerationThread()
        return 1.0
      properties.gen_iteration = 'Mesh Generation Done'
      properties.gen_stage = ''
      properties.gen_in_progress = False
      SESSION_CACHE['properties'] = None
      print('Mesh Generation Done')
      return None
  return 1.0


def cancelGeneration():
  if 'cancel_signal' in SESSION_CACHE:
    cancel_signal = SESSION_CACHE['cancel_signal']
    if cancel_signal != None:
      cancel_signal.set()
    SESSION_CACHE['cancel_signal'] = None


def generate3dMeshFrom2dImage(properties):
  image_input = properties.image_input
  if properties.image_input == None:
    return
  output_name = image_input.name
  image = bpyToPillowImage(image_input)
  
  SESSION_CACHE['properties'] = properties
  SESSION_CACHE['image_input'] = bpyToPillowImage(properties.image_input)
  SESSION_CACHE['output_name'] = properties.image_input.name
  SESSION_CACHE['pipeline_type'] = properties.pipeline_type
  SESSION_CACHE['seed'] = int(properties.seed)
  SESSION_CACHE['centered'] = bool(properties.centered)
  SESSION_CACHE['scale'] = float(properties.scale)
  SESSION_CACHE['gen_texture'] = bool(properties.gen_texture)
  
  SESSION_CACHE['sparse_overrides'] = {'steps': int(properties.sparse_steps)}
  SESSION_CACHE['shape_overrides'] = {'steps': int(properties.shape_steps)}
  SESSION_CACHE['texture_overrides'] = {'steps': int(properties.texture_steps)}
  
  SESSION_CACHE['count'] = int(properties.count)
  SESSION_CACHE['index'] = 0
  SESSION_CACHE['cancel_signal'] = threading.Event()
  
  # Start the mesh generation thread
  properties.gen_iteration = f'Generating Mesh 1 of {properties.count}' if properties.count > 1 else 'Generating Mesh'
  properties.gen_stage = 'Loading Pipeline Models'
  properties.gen_in_progress = True
  startMeshGenerationThread()
  
  # Start check mesh genration timer
  bpy.app.timers.register(checkMeshGeneration)
