
import sys
import subprocess
import importlib


def get_required_modules():
  return [
    ('Torch', 'torch', 'torch==2.11.0'),
    ('Torch Vision', 'torchvision', 'torchvision==0.26.0'),
    ('EasyDict', 'easydict', 'easydict'),
    ('Pillow', 'PIL', 'pillow'),
    ('Rembg', 'rembg', 'rembg[cpu]'),
    ('Transformers', 'transformers', 'transformers'),
    ('Hugging Face Hub', 'huggingface_hub', 'huggingface_hub')
  ]


def has_installed_module(module_name):
  try:
    importlib.import_module(module_name)
    return True
  except ImportError:
    return False


def get_needed_modules():
  needed_modules = []
  req_moduels = get_required_modules()
  for module in req_moduels:
    if not has_installed_module(module[1]):
      needed_modules.append(module)
  return needed_modules


def all_modules_installed():
  for module in get_required_modules():
    if not has_installed_module(module[1]):
      return False
  return True


def install_modules(modules = []):
  # Get Blender's internal Python executable path
  py_exe = sys.executable
  
  # Install/Update Pip
  subprocess.run([py_exe, '-m', 'ensurepip'], check=True)
  subprocess.run([py_exe, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
  
  # If modules is empty, assign reqired modules
  if not modules:
    modules = get_required_modules()
  
  # Install each module
  for module in modules:
    subprocess.run([py_exe, '-m', 'pip', 'install', '--upgrade', module[2]], check=True)
  print('Done Installing Modules')
