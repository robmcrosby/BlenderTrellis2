import bpy
import mathutils
import os
import typing


def get_smooth_geometry_node_group():
  node_name = "Smooth Geometry"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]
  
  """Initialize Smooth Geometry node group"""
  smooth_geometry_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  smooth_geometry_1.color_tag = 'GEOMETRY'
  smooth_geometry_1.description = ""
  smooth_geometry_1.default_group_node_width = 140
  smooth_geometry_1.show_modifier_manage_panel = True

  # smooth_geometry_1 interface

  # Socket Geometry
  geometry_socket = smooth_geometry_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
  geometry_socket.attribute_domain = 'POINT'
  geometry_socket.default_input = 'VALUE'
  geometry_socket.structure_type = 'AUTO'

  # Socket Geometry
  geometry_socket_1 = smooth_geometry_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
  geometry_socket_1.attribute_domain = 'POINT'
  geometry_socket_1.description = "Points to smooth based on their neighbors"
  geometry_socket_1.default_input = 'VALUE'
  geometry_socket_1.structure_type = 'AUTO'

  # Socket Selection
  selection_socket = smooth_geometry_1.interface.new_socket(name="Selection", in_out='INPUT', socket_type='NodeSocketBool')
  selection_socket.default_value = True
  selection_socket.attribute_domain = 'POINT'
  selection_socket.hide_value = True
  selection_socket.default_input = 'VALUE'
  selection_socket.structure_type = 'AUTO'

  # Socket Iterations
  iterations_socket = smooth_geometry_1.interface.new_socket(name="Iterations", in_out='INPUT', socket_type='NodeSocketInt')
  iterations_socket.default_value = 5
  iterations_socket.min_value = 0
  iterations_socket.max_value = 2147483647
  iterations_socket.subtype = 'NONE'
  iterations_socket.attribute_domain = 'POINT'
  iterations_socket.description = "How many times to repeat the smoothing step"
  iterations_socket.default_input = 'VALUE'
  iterations_socket.structure_type = 'AUTO'

  # Socket Weight
  weight_socket = smooth_geometry_1.interface.new_socket(name="Weight", in_out='INPUT', socket_type='NodeSocketFloat')
  weight_socket.default_value = 0.5
  weight_socket.min_value = 0.0
  weight_socket.max_value = 1.0
  weight_socket.subtype = 'FACTOR'
  weight_socket.attribute_domain = 'POINT'
  weight_socket.description = "Relative mix weight of neighboring elements"
  weight_socket.default_input = 'VALUE'
  weight_socket.structure_type = 'AUTO'

  # Initialize smooth_geometry_1 nodes

  # Node Group Output
  group_output = smooth_geometry_1.nodes.new("NodeGroupOutput")
  group_output.name = "Group Output"
  group_output.show_options = True
  group_output.is_active_output = True

  # Node Group Input
  group_input = smooth_geometry_1.nodes.new("NodeGroupInput")
  group_input.name = "Group Input"
  group_input.use_custom_color = True
  group_input.color = (0.5098000168800354, 0.20784400403499603, 0.2980409860610962)
  group_input.show_options = True

  # Node Set Position
  set_position = smooth_geometry_1.nodes.new("GeometryNodeSetPosition")
  set_position.name = "Set Position"
  set_position.show_options = True
  # Offset
  set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

  # Node Position
  position = smooth_geometry_1.nodes.new("GeometryNodeInputPosition")
  position.name = "Position"
  position.show_options = True

  # Node Blur Attribute
  blur_attribute = smooth_geometry_1.nodes.new("GeometryNodeBlurAttribute")
  blur_attribute.name = "Blur Attribute"
  blur_attribute.show_options = True
  blur_attribute.data_type = 'FLOAT_VECTOR'

  # Set locations
  smooth_geometry_1.nodes["Group Output"].location = (370.4945068359375, 0.0)
  smooth_geometry_1.nodes["Group Input"].location = (-459.9999694824219, 0.0)
  smooth_geometry_1.nodes["Set Position"].location = (100.00000762939453, 40.0)
  smooth_geometry_1.nodes["Position"].location = (-260.0, -40.0)
  smooth_geometry_1.nodes["Blur Attribute"].location = (-80.0, -20.0)

  # Set dimensions
  smooth_geometry_1.nodes["Group Output"].width  = 140.0
  smooth_geometry_1.nodes["Group Output"].height = 100.0

  smooth_geometry_1.nodes["Group Input"].width  = 140.0
  smooth_geometry_1.nodes["Group Input"].height = 100.0

  smooth_geometry_1.nodes["Set Position"].width  = 140.0
  smooth_geometry_1.nodes["Set Position"].height = 100.0

  smooth_geometry_1.nodes["Position"].width  = 140.0
  smooth_geometry_1.nodes["Position"].height = 100.0

  smooth_geometry_1.nodes["Blur Attribute"].width  = 140.0
  smooth_geometry_1.nodes["Blur Attribute"].height = 100.0


  # Initialize smooth_geometry_1 links

  # position.Position -> blur_attribute.Value
  smooth_geometry_1.links.new(
    smooth_geometry_1.nodes["Position"].outputs[0],
    smooth_geometry_1.nodes["Blur Attribute"].inputs[0]
  )
  # blur_attribute.Value -> set_position.Position
  smooth_geometry_1.links.new(
    smooth_geometry_1.nodes["Blur Attribute"].outputs[0],
    smooth_geometry_1.nodes["Set Position"].inputs[2]
  )
  # group_input.Geometry -> set_position.Geometry
  smooth_geometry_1.links.new(
    smooth_geometry_1.nodes["Group Input"].outputs[0],
    smooth_geometry_1.nodes["Set Position"].inputs[0]
  )
  # set_position.Geometry -> group_output.Geometry
  smooth_geometry_1.links.new(
    smooth_geometry_1.nodes["Set Position"].outputs[0],
    smooth_geometry_1.nodes["Group Output"].inputs[0]
  )
  # group_input.Selection -> set_position.Selection
  smooth_geometry_1.links.new(
    smooth_geometry_1.nodes["Group Input"].outputs[1],
    smooth_geometry_1.nodes["Set Position"].inputs[1]
  )
  # group_input.Weight -> blur_attribute.Weight
  smooth_geometry_1.links.new(
    smooth_geometry_1.nodes["Group Input"].outputs[3],
    smooth_geometry_1.nodes["Blur Attribute"].inputs[2]
  )
  # group_input.Iterations -> blur_attribute.Iterations
  smooth_geometry_1.links.new(
    smooth_geometry_1.nodes["Group Input"].outputs[2],
    smooth_geometry_1.nodes["Blur Attribute"].inputs[1]
  )

  return smooth_geometry_1


def get_nearest_position_group():
  node_name = "Nearest Position"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]
  
  """Initialize Nearest Position node group"""
  nearest_position_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  nearest_position_1.color_tag = 'NONE'
  nearest_position_1.description = ""
  nearest_position_1.default_group_node_width = 140
  nearest_position_1.show_modifier_manage_panel = True

  # nearest_position_1 interface

  # Socket Position
  position_socket = nearest_position_1.interface.new_socket(name="Position", in_out='OUTPUT', socket_type='NodeSocketVector')
  position_socket.default_value = (0.0, 0.0, 0.0)
  position_socket.min_value = -3.4028234663852886e+38
  position_socket.max_value = 3.4028234663852886e+38
  position_socket.subtype = 'NONE'
  position_socket.attribute_domain = 'POINT'
  position_socket.default_input = 'VALUE'
  position_socket.structure_type = 'AUTO'

  # Socket Geometry
  geometry_socket = nearest_position_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
  geometry_socket.attribute_domain = 'POINT'
  geometry_socket.default_input = 'VALUE'
  geometry_socket.structure_type = 'AUTO'

  # Initialize nearest_position_1 nodes

  # Node Position
  position = nearest_position_1.nodes.new("GeometryNodeInputPosition")
  position.name = "Position"
  position.hide = True
  position.show_options = True

  # Node Sample Nearest
  sample_nearest = nearest_position_1.nodes.new("GeometryNodeSampleNearest")
  sample_nearest.name = "Sample Nearest"
  sample_nearest.show_options = True
  sample_nearest.domain = 'POINT'

  # Node Sample Index
  sample_index = nearest_position_1.nodes.new("GeometryNodeSampleIndex")
  sample_index.name = "Sample Index"
  sample_index.show_options = True
  sample_index.clamp = False
  sample_index.data_type = 'FLOAT_VECTOR'
  sample_index.domain = 'POINT'

  # Node Group Output
  group_output = nearest_position_1.nodes.new("NodeGroupOutput")
  group_output.label = "Position Out"
  group_output.name = "Group Output"
  group_output.hide = True
  group_output.show_options = True
  group_output.is_active_output = True
  group_output.inputs[1].hide = True

  # Node Group Input
  group_input = nearest_position_1.nodes.new("NodeGroupInput")
  group_input.label = "Geometry"
  group_input.name = "Group Input"
  group_input.hide = True
  group_input.show_options = True
  group_input.outputs[1].hide = True

  # Node Position.001
  position_001 = nearest_position_1.nodes.new("GeometryNodeInputPosition")
  position_001.name = "Position.001"
  position_001.hide = True
  position_001.show_options = True

  # Node Group Input.001
  group_input_001 = nearest_position_1.nodes.new("NodeGroupInput")
  group_input_001.label = "Geometry"
  group_input_001.name = "Group Input.001"
  group_input_001.hide = True
  group_input_001.show_options = True
  group_input_001.outputs[1].hide = True

  # Set locations
  nearest_position_1.nodes["Position"].location = (-93.37069702148438, 38.232078552246094)
  nearest_position_1.nodes["Sample Nearest"].location = (-132.29437255859375, 1.9682176113128662)
  nearest_position_1.nodes["Sample Index"].location = (37.825069427490234, 165.91693115234375)
  nearest_position_1.nodes["Group Output"].location = (175.74623107910156, 139.36181640625)
  nearest_position_1.nodes["Group Input"].location = (-93.74468994140625, 76.96391296386719)
  nearest_position_1.nodes["Position.001"].location = (-253.46517944335938, -93.86023712158203)
  nearest_position_1.nodes["Group Input.001"].location = (-253.83917236328125, -55.128395080566406)

  # Set dimensions
  nearest_position_1.nodes["Position"].width  = 100.0
  nearest_position_1.nodes["Position"].height = 100.0

  nearest_position_1.nodes["Sample Nearest"].width  = 140.0
  nearest_position_1.nodes["Sample Nearest"].height = 100.0

  nearest_position_1.nodes["Sample Index"].width  = 111.8983154296875
  nearest_position_1.nodes["Sample Index"].height = 100.0

  nearest_position_1.nodes["Group Output"].width  = 105.6129150390625
  nearest_position_1.nodes["Group Output"].height = 100.0

  nearest_position_1.nodes["Group Input"].width  = 99.12481689453125
  nearest_position_1.nodes["Group Input"].height = 100.0

  nearest_position_1.nodes["Position.001"].width  = 100.0
  nearest_position_1.nodes["Position.001"].height = 100.0

  nearest_position_1.nodes["Group Input.001"].width  = 99.12481689453125
  nearest_position_1.nodes["Group Input.001"].height = 100.0


  # Initialize nearest_position_1 links

  # position.Position -> sample_index.Value
  nearest_position_1.links.new(
    nearest_position_1.nodes["Position"].outputs[0],
    nearest_position_1.nodes["Sample Index"].inputs[1]
  )
  # group_input.Geometry -> sample_index.Geometry
  nearest_position_1.links.new(
    nearest_position_1.nodes["Group Input"].outputs[0],
    nearest_position_1.nodes["Sample Index"].inputs[0]
  )
  # sample_nearest.Index -> sample_index.Index
  nearest_position_1.links.new(
    nearest_position_1.nodes["Sample Nearest"].outputs[0],
    nearest_position_1.nodes["Sample Index"].inputs[2]
  )
  # sample_index.Value -> group_output.Position
  nearest_position_1.links.new(
    nearest_position_1.nodes["Sample Index"].outputs[0],
    nearest_position_1.nodes["Group Output"].inputs[0]
  )
  # group_input_001.Geometry -> sample_nearest.Geometry
  nearest_position_1.links.new(
    nearest_position_1.nodes["Group Input.001"].outputs[0],
    nearest_position_1.nodes["Sample Nearest"].inputs[0]
  )
  # position_001.Position -> sample_nearest.Sample Position
  nearest_position_1.links.new(
    nearest_position_1.nodes["Position.001"].outputs[0],
    nearest_position_1.nodes["Sample Nearest"].inputs[1]
  )

  return nearest_position_1


def get_carve_sdf_node_group():
  node_name = "Carve SDF"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]
  
  """Initialize Carve SDF node group"""
  carve_sdf_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  carve_sdf_1.color_tag = 'NONE'
  carve_sdf_1.description = ""
  carve_sdf_1.default_group_node_width = 140
  carve_sdf_1.show_modifier_manage_panel = True

  # carve_sdf_1 interface

  # Socket Mesh
  mesh_socket = carve_sdf_1.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')
  mesh_socket.attribute_domain = 'POINT'
  mesh_socket.default_input = 'VALUE'
  mesh_socket.structure_type = 'AUTO'

  # Socket Mesh
  mesh_socket_1 = carve_sdf_1.interface.new_socket(name="Mesh", in_out='INPUT', socket_type='NodeSocketGeometry')
  mesh_socket_1.attribute_domain = 'POINT'
  mesh_socket_1.description = "Mesh whose inner volume is converted to a signed distance field grid"
  mesh_socket_1.default_input = 'VALUE'
  mesh_socket_1.structure_type = 'AUTO'

  # Socket Points
  points_socket = carve_sdf_1.interface.new_socket(name="Points", in_out='INPUT', socket_type='NodeSocketGeometry')
  points_socket.attribute_domain = 'POINT'
  points_socket.default_input = 'VALUE'
  points_socket.structure_type = 'AUTO'

  # Socket Voxel Size
  voxel_size_socket = carve_sdf_1.interface.new_socket(name="Voxel Size", in_out='INPUT', socket_type='NodeSocketFloat')
  voxel_size_socket.default_value = 0.019999999552965164
  voxel_size_socket.min_value = 0.009999999776482582
  voxel_size_socket.max_value = 3.4028234663852886e+38
  voxel_size_socket.subtype = 'DISTANCE'
  voxel_size_socket.attribute_domain = 'POINT'
  voxel_size_socket.default_input = 'VALUE'
  voxel_size_socket.structure_type = 'AUTO'

  # Socket Iterations
  iterations_socket = carve_sdf_1.interface.new_socket(name="Iterations", in_out='INPUT', socket_type='NodeSocketInt')
  iterations_socket.default_value = 4
  iterations_socket.min_value = 0
  iterations_socket.max_value = 2147483647
  iterations_socket.subtype = 'NONE'
  iterations_socket.attribute_domain = 'POINT'
  iterations_socket.default_input = 'VALUE'
  iterations_socket.structure_type = 'AUTO'

  # Initialize carve_sdf_1 nodes

  # Node Mesh to SDF Grid.004
  mesh_to_sdf_grid_004 = carve_sdf_1.nodes.new("GeometryNodeMeshToSDFGrid")
  mesh_to_sdf_grid_004.name = "Mesh to SDF Grid.004"
  mesh_to_sdf_grid_004.show_options = True
  # Band Width
  mesh_to_sdf_grid_004.inputs[2].default_value = 3

  # Node Grid to Mesh.006
  grid_to_mesh_006 = carve_sdf_1.nodes.new("GeometryNodeGridToMesh")
  grid_to_mesh_006.name = "Grid to Mesh.006"
  grid_to_mesh_006.show_options = True
  # Threshold
  grid_to_mesh_006.inputs[1].default_value = 0.009999999776482582
  # Adaptivity
  grid_to_mesh_006.inputs[2].default_value = 0.0

  # Node Repeat Input.005
  repeat_input_005 = carve_sdf_1.nodes.new("GeometryNodeRepeatInput")
  repeat_input_005.name = "Repeat Input.005"
  repeat_input_005.show_options = True
  # Node Repeat Output.005
  repeat_output_005 = carve_sdf_1.nodes.new("GeometryNodeRepeatOutput")
  repeat_output_005.name = "Repeat Output.005"
  repeat_output_005.show_options = True
  repeat_output_005.active_index = 0
  repeat_output_005.inspection_index = 0
  repeat_output_005.repeat_items.clear()
  # Create item "SDF Grid"
  repeat_output_005.repeat_items.new('FLOAT', "SDF Grid")
  repeat_output_005.inputs[1].hide = True
  repeat_output_005.outputs[1].hide = True

  # Node Grid to Mesh.007
  grid_to_mesh_007 = carve_sdf_1.nodes.new("GeometryNodeGridToMesh")
  grid_to_mesh_007.name = "Grid to Mesh.007"
  grid_to_mesh_007.show_options = True
  # Threshold
  grid_to_mesh_007.inputs[1].default_value = 0.009999999776482582
  # Adaptivity
  grid_to_mesh_007.inputs[2].default_value = 0.0

  # Node Nearest Position.003
  nearest_position_003 = carve_sdf_1.nodes.new("GeometryNodeGroup")
  nearest_position_003.name = "Nearest Position.003"
  nearest_position_003.hide = True
  nearest_position_003.node_tree = get_nearest_position_group()

  # Node Vector Math.007
  vector_math_007 = carve_sdf_1.nodes.new("ShaderNodeVectorMath")
  vector_math_007.name = "Vector Math.007"
  vector_math_007.hide = True
  vector_math_007.show_options = True
  vector_math_007.operation = 'DISTANCE'

  # Node Position.006
  position_006 = carve_sdf_1.nodes.new("GeometryNodeInputPosition")
  position_006.name = "Position.006"
  position_006.hide = True
  position_006.show_options = True

  # Node Compare.006
  compare_006 = carve_sdf_1.nodes.new("FunctionNodeCompare")
  compare_006.name = "Compare.006"
  compare_006.show_options = True
  compare_006.data_type = 'FLOAT'
  compare_006.mode = 'ELEMENT'
  compare_006.operation = 'LESS_THAN'

  # Node Delete Geometry.002
  delete_geometry_002 = carve_sdf_1.nodes.new("GeometryNodeDeleteGeometry")
  delete_geometry_002.name = "Delete Geometry.002"
  delete_geometry_002.show_options = True
  delete_geometry_002.domain = 'POINT'
  delete_geometry_002.mode = 'ALL'

  # Node Mesh to Points.005
  mesh_to_points_005 = carve_sdf_1.nodes.new("GeometryNodeMeshToPoints")
  mesh_to_points_005.name = "Mesh to Points.005"
  mesh_to_points_005.show_options = True
  mesh_to_points_005.mode = 'FACES'
  # Selection
  mesh_to_points_005.inputs[1].default_value = True
  # Position
  mesh_to_points_005.inputs[2].default_value = (0.0, 0.0, 0.0)
  # Radius
  mesh_to_points_005.inputs[3].default_value = 0.004999999888241291

  # Node Points to SDF Grid.002
  points_to_sdf_grid_002 = carve_sdf_1.nodes.new("GeometryNodePointsToSDFGrid")
  points_to_sdf_grid_002.name = "Points to SDF Grid.002"
  points_to_sdf_grid_002.show_options = True

  # Node SDF Grid Boolean.002
  sdf_grid_boolean_002 = carve_sdf_1.nodes.new("GeometryNodeSDFGridBoolean")
  sdf_grid_boolean_002.name = "SDF Grid Boolean.002"
  sdf_grid_boolean_002.show_options = True
  sdf_grid_boolean_002.operation = 'DIFFERENCE'

  # Node Domain Size.002
  domain_size_002 = carve_sdf_1.nodes.new("GeometryNodeAttributeDomainSize")
  domain_size_002.name = "Domain Size.002"
  domain_size_002.show_options = True
  domain_size_002.component = 'POINTCLOUD'

  # Node Compare.007
  compare_007 = carve_sdf_1.nodes.new("FunctionNodeCompare")
  compare_007.name = "Compare.007"
  compare_007.show_options = True
  compare_007.data_type = 'INT'
  compare_007.mode = 'ELEMENT'
  compare_007.operation = 'GREATER_THAN'
  # B_INT
  compare_007.inputs[3].default_value = 0

  # Node Switch.005
  switch_005 = carve_sdf_1.nodes.new("GeometryNodeSwitch")
  switch_005.name = "Switch.005"
  switch_005.show_options = True
  switch_005.input_type = 'FLOAT'

  # Node Reroute.006
  reroute_006 = carve_sdf_1.nodes.new("NodeReroute")
  reroute_006.name = "Reroute.006"
  reroute_006.show_options = True
  reroute_006.socket_idname = "NodeSocketFloat"
  # Node Mesh to Points.006
  mesh_to_points_006 = carve_sdf_1.nodes.new("GeometryNodeMeshToPoints")
  mesh_to_points_006.name = "Mesh to Points.006"
  mesh_to_points_006.show_options = True
  mesh_to_points_006.mode = 'VERTICES'
  # Selection
  mesh_to_points_006.inputs[1].default_value = True
  # Position
  mesh_to_points_006.inputs[2].default_value = (0.0, 0.0, 0.0)
  # Radius
  mesh_to_points_006.inputs[3].default_value = 0.004999999888241291

  # Node Join Geometry.003
  join_geometry_003 = carve_sdf_1.nodes.new("GeometryNodeJoinGeometry")
  join_geometry_003.name = "Join Geometry.003"
  join_geometry_003.show_options = True

  # Node Math.001
  math_001 = carve_sdf_1.nodes.new("ShaderNodeMath")
  math_001.name = "Math.001"
  math_001.show_options = True
  math_001.operation = 'SUBTRACT'
  math_001.use_clamp = False

  # Node Group Output
  group_output = carve_sdf_1.nodes.new("NodeGroupOutput")
  group_output.name = "Group Output"
  group_output.show_options = True
  group_output.is_active_output = True

  # Node Group Input
  group_input = carve_sdf_1.nodes.new("NodeGroupInput")
  group_input.name = "Group Input"
  group_input.show_options = True
  group_input.outputs[1].hide = True
  group_input.outputs[3].hide = True
  group_input.outputs[4].hide = True

  # Node Group Input.001
  group_input_001 = carve_sdf_1.nodes.new("NodeGroupInput")
  group_input_001.name = "Group Input.001"
  group_input_001.show_options = True
  group_input_001.outputs[0].hide = True
  group_input_001.outputs[2].hide = True
  group_input_001.outputs[3].hide = True
  group_input_001.outputs[4].hide = True

  # Node Group Input.002
  group_input_002 = carve_sdf_1.nodes.new("NodeGroupInput")
  group_input_002.name = "Group Input.002"
  group_input_002.show_options = True
  group_input_002.outputs[0].hide = True
  group_input_002.outputs[1].hide = True
  group_input_002.outputs[3].hide = True
  group_input_002.outputs[4].hide = True

  # Node Group Input.003
  group_input_003 = carve_sdf_1.nodes.new("NodeGroupInput")
  group_input_003.name = "Group Input.003"
  group_input_003.show_options = True
  group_input_003.outputs[0].hide = True
  group_input_003.outputs[1].hide = True
  group_input_003.outputs[3].hide = True
  group_input_003.outputs[4].hide = True

  # Node Group Input.004
  group_input_004 = carve_sdf_1.nodes.new("NodeGroupInput")
  group_input_004.label = "Iterations"
  group_input_004.name = "Group Input.004"
  group_input_004.hide = True
  group_input_004.show_options = True
  group_input_004.outputs[0].hide = True
  group_input_004.outputs[1].hide = True
  group_input_004.outputs[2].hide = True
  group_input_004.outputs[4].hide = True

  # Process zone input Repeat Input.005
  repeat_input_005.pair_with_output(repeat_output_005)



  # Set locations
  carve_sdf_1.nodes["Mesh to SDF Grid.004"].location = (-893.1796264648438, 88.2847900390625)
  carve_sdf_1.nodes["Grid to Mesh.006"].location = (-529.052490234375, 24.1229248046875)
  carve_sdf_1.nodes["Repeat Input.005"].location = (-708.406494140625, 164.139404296875)
  carve_sdf_1.nodes["Repeat Output.005"].location = (685.41796875, 181.69244384765625)
  carve_sdf_1.nodes["Grid to Mesh.007"].location = (827.1908569335938, 176.96237182617188)
  carve_sdf_1.nodes["Nearest Position.003"].location = (-521.0652465820312, -146.3201904296875)
  carve_sdf_1.nodes["Vector Math.007"].location = (-370.5401611328125, -165.32220458984375)
  carve_sdf_1.nodes["Position.006"].location = (-522.9541015625, -185.32220458984375)
  carve_sdf_1.nodes["Compare.006"].location = (-204.0587158203125, -114.40109252929688)
  carve_sdf_1.nodes["Delete Geometry.002"].location = (-203.9537353515625, 22.913421630859375)
  carve_sdf_1.nodes["Mesh to Points.005"].location = (-368.74273681640625, 24.266265869140625)
  carve_sdf_1.nodes["Points to SDF Grid.002"].location = (108.63067626953125, 33.009521484375)
  carve_sdf_1.nodes["SDF Grid Boolean.002"].location = (308.256591796875, 51.51800537109375)
  carve_sdf_1.nodes["Domain Size.002"].location = (-11.01190185546875, 226.3948974609375)
  carve_sdf_1.nodes["Compare.007"].location = (161.57373046875, 274.72265625)
  carve_sdf_1.nodes["Switch.005"].location = (494.910400390625, 184.33013916015625)
  carve_sdf_1.nodes["Reroute.006"].location = (243.27838134765625, 77.62060546875)
  carve_sdf_1.nodes["Mesh to Points.006"].location = (-364.6607360839844, 200.74786376953125)
  carve_sdf_1.nodes["Join Geometry.003"].location = (-199.75390625, 82.32177734375)
  carve_sdf_1.nodes["Math.001"].location = (-203.748046875, -274.72265625)
  carve_sdf_1.nodes["Group Output"].location = (1002.779541015625, 179.1442413330078)
  carve_sdf_1.nodes["Group Input"].location = (-1018.6004028320312, 64.10063171386719)
  carve_sdf_1.nodes["Group Input.001"].location = (-648.33642578125, -143.12879943847656)
  carve_sdf_1.nodes["Group Input.002"].location = (-366.85040283203125, -276.7236633300781)
  carve_sdf_1.nodes["Group Input.003"].location = (108.72254943847656, -99.85699462890625)
  carve_sdf_1.nodes["Group Input.004"].location = (-845.061767578125, 125.2640380859375)

  # Set dimensions
  carve_sdf_1.nodes["Mesh to SDF Grid.004"].width  = 140.0
  carve_sdf_1.nodes["Mesh to SDF Grid.004"].height = 100.0

  carve_sdf_1.nodes["Grid to Mesh.006"].width  = 140.0
  carve_sdf_1.nodes["Grid to Mesh.006"].height = 100.0

  carve_sdf_1.nodes["Repeat Input.005"].width  = 140.0
  carve_sdf_1.nodes["Repeat Input.005"].height = 100.0

  carve_sdf_1.nodes["Repeat Output.005"].width  = 100.0
  carve_sdf_1.nodes["Repeat Output.005"].height = 100.0

  carve_sdf_1.nodes["Grid to Mesh.007"].width  = 140.0
  carve_sdf_1.nodes["Grid to Mesh.007"].height = 100.0

  carve_sdf_1.nodes["Nearest Position.003"].width  = 125.34478759765625
  carve_sdf_1.nodes["Nearest Position.003"].height = 100.0

  carve_sdf_1.nodes["Vector Math.007"].width  = 100.0
  carve_sdf_1.nodes["Vector Math.007"].height = 100.0

  carve_sdf_1.nodes["Position.006"].width  = 125.34490966796875
  carve_sdf_1.nodes["Position.006"].height = 100.0

  carve_sdf_1.nodes["Compare.006"].width  = 140.0
  carve_sdf_1.nodes["Compare.006"].height = 100.0

  carve_sdf_1.nodes["Delete Geometry.002"].width  = 140.0
  carve_sdf_1.nodes["Delete Geometry.002"].height = 100.0

  carve_sdf_1.nodes["Mesh to Points.005"].width  = 136.0919189453125
  carve_sdf_1.nodes["Mesh to Points.005"].height = 100.0

  carve_sdf_1.nodes["Points to SDF Grid.002"].width  = 140.0
  carve_sdf_1.nodes["Points to SDF Grid.002"].height = 100.0

  carve_sdf_1.nodes["SDF Grid Boolean.002"].width  = 140.0
  carve_sdf_1.nodes["SDF Grid Boolean.002"].height = 100.0

  carve_sdf_1.nodes["Domain Size.002"].width  = 140.0
  carve_sdf_1.nodes["Domain Size.002"].height = 100.0

  carve_sdf_1.nodes["Compare.007"].width  = 140.0
  carve_sdf_1.nodes["Compare.007"].height = 100.0

  carve_sdf_1.nodes["Switch.005"].width  = 140.0
  carve_sdf_1.nodes["Switch.005"].height = 100.0

  carve_sdf_1.nodes["Reroute.006"].width  = 20.0
  carve_sdf_1.nodes["Reroute.006"].height = 100.0

  carve_sdf_1.nodes["Mesh to Points.006"].width  = 136.0919189453125
  carve_sdf_1.nodes["Mesh to Points.006"].height = 100.0

  carve_sdf_1.nodes["Join Geometry.003"].width  = 140.0
  carve_sdf_1.nodes["Join Geometry.003"].height = 100.0

  carve_sdf_1.nodes["Math.001"].width  = 140.0
  carve_sdf_1.nodes["Math.001"].height = 100.0

  carve_sdf_1.nodes["Group Output"].width  = 140.0
  carve_sdf_1.nodes["Group Output"].height = 100.0

  carve_sdf_1.nodes["Group Input"].width  = 97.8846435546875
  carve_sdf_1.nodes["Group Input"].height = 100.0

  carve_sdf_1.nodes["Group Input.001"].width  = 99.63946533203125
  carve_sdf_1.nodes["Group Input.001"].height = 100.0

  carve_sdf_1.nodes["Group Input.002"].width  = 100.9185791015625
  carve_sdf_1.nodes["Group Input.002"].height = 100.0

  carve_sdf_1.nodes["Group Input.003"].width  = 100.9185791015625
  carve_sdf_1.nodes["Group Input.003"].height = 100.0

  carve_sdf_1.nodes["Group Input.004"].width  = 94.25653076171875
  carve_sdf_1.nodes["Group Input.004"].height = 100.0


  # Initialize carve_sdf_1 links

  # mesh_to_sdf_grid_004.SDF Grid -> repeat_input_005.SDF Grid
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Mesh to SDF Grid.004"].outputs[0],
    carve_sdf_1.nodes["Repeat Input.005"].inputs[1]
  )
  # nearest_position_003.Position -> vector_math_007.Vector
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Nearest Position.003"].outputs[0],
    carve_sdf_1.nodes["Vector Math.007"].inputs[0]
  )
  # position_006.Position -> vector_math_007.Vector
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Position.006"].outputs[0],
    carve_sdf_1.nodes["Vector Math.007"].inputs[1]
  )
  # vector_math_007.Value -> compare_006.A
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Vector Math.007"].outputs[1],
    carve_sdf_1.nodes["Compare.006"].inputs[0]
  )
  # grid_to_mesh_006.Mesh -> mesh_to_points_005.Mesh
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Grid to Mesh.006"].outputs[0],
    carve_sdf_1.nodes["Mesh to Points.005"].inputs[0]
  )
  # compare_006.Result -> delete_geometry_002.Selection
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Compare.006"].outputs[0],
    carve_sdf_1.nodes["Delete Geometry.002"].inputs[1]
  )
  # delete_geometry_002.Geometry -> points_to_sdf_grid_002.Points
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Delete Geometry.002"].outputs[0],
    carve_sdf_1.nodes["Points to SDF Grid.002"].inputs[0]
  )
  # points_to_sdf_grid_002.SDF Grid -> sdf_grid_boolean_002.Grid 2
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Points to SDF Grid.002"].outputs[0],
    carve_sdf_1.nodes["SDF Grid Boolean.002"].inputs[1]
  )
  # repeat_output_005.SDF Grid -> grid_to_mesh_007.Grid
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Repeat Output.005"].outputs[0],
    carve_sdf_1.nodes["Grid to Mesh.007"].inputs[0]
  )
  # repeat_input_005.SDF Grid -> grid_to_mesh_006.Grid
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Repeat Input.005"].outputs[1],
    carve_sdf_1.nodes["Grid to Mesh.006"].inputs[0]
  )
  # reroute_006.Output -> sdf_grid_boolean_002.Grid 1
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Reroute.006"].outputs[0],
    carve_sdf_1.nodes["SDF Grid Boolean.002"].inputs[0]
  )
  # switch_005.Output -> repeat_output_005.SDF Grid
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Switch.005"].outputs[0],
    carve_sdf_1.nodes["Repeat Output.005"].inputs[0]
  )
  # delete_geometry_002.Geometry -> domain_size_002.Geometry
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Delete Geometry.002"].outputs[0],
    carve_sdf_1.nodes["Domain Size.002"].inputs[0]
  )
  # domain_size_002.Point Count -> compare_007.A
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Domain Size.002"].outputs[0],
    carve_sdf_1.nodes["Compare.007"].inputs[2]
  )
  # sdf_grid_boolean_002.Grid -> switch_005.True
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["SDF Grid Boolean.002"].outputs[0],
    carve_sdf_1.nodes["Switch.005"].inputs[2]
  )
  # compare_007.Result -> switch_005.Switch
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Compare.007"].outputs[0],
    carve_sdf_1.nodes["Switch.005"].inputs[0]
  )
  # repeat_input_005.SDF Grid -> reroute_006.Input
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Repeat Input.005"].outputs[1],
    carve_sdf_1.nodes["Reroute.006"].inputs[0]
  )
  # reroute_006.Output -> switch_005.False
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Reroute.006"].outputs[0],
    carve_sdf_1.nodes["Switch.005"].inputs[1]
  )
  # grid_to_mesh_006.Mesh -> mesh_to_points_006.Mesh
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Grid to Mesh.006"].outputs[0],
    carve_sdf_1.nodes["Mesh to Points.006"].inputs[0]
  )
  # mesh_to_points_006.Points -> join_geometry_003.Geometry
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Mesh to Points.006"].outputs[0],
    carve_sdf_1.nodes["Join Geometry.003"].inputs[0]
  )
  # vector_math_007.Value -> math_001.Value
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Vector Math.007"].outputs[1],
    carve_sdf_1.nodes["Math.001"].inputs[0]
  )
  # math_001.Value -> points_to_sdf_grid_002.Radius
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Math.001"].outputs[0],
    carve_sdf_1.nodes["Points to SDF Grid.002"].inputs[1]
  )
  # join_geometry_003.Geometry -> delete_geometry_002.Geometry
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Join Geometry.003"].outputs[0],
    carve_sdf_1.nodes["Delete Geometry.002"].inputs[0]
  )
  # group_input.Mesh -> mesh_to_sdf_grid_004.Mesh
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Group Input"].outputs[0],
    carve_sdf_1.nodes["Mesh to SDF Grid.004"].inputs[0]
  )
  # grid_to_mesh_007.Mesh -> group_output.Mesh
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Grid to Mesh.007"].outputs[0],
    carve_sdf_1.nodes["Group Output"].inputs[0]
  )
  # group_input.Voxel Size -> mesh_to_sdf_grid_004.Voxel Size
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Group Input"].outputs[2],
    carve_sdf_1.nodes["Mesh to SDF Grid.004"].inputs[1]
  )
  # group_input_001.Points -> nearest_position_003.Geometry
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Group Input.001"].outputs[1],
    carve_sdf_1.nodes["Nearest Position.003"].inputs[0]
  )
  # group_input_002.Voxel Size -> compare_006.B
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Group Input.002"].outputs[2],
    carve_sdf_1.nodes["Compare.006"].inputs[1]
  )
  # group_input_002.Voxel Size -> math_001.Value
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Group Input.002"].outputs[2],
    carve_sdf_1.nodes["Math.001"].inputs[1]
  )
  # group_input_003.Voxel Size -> points_to_sdf_grid_002.Voxel Size
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Group Input.003"].outputs[2],
    carve_sdf_1.nodes["Points to SDF Grid.002"].inputs[2]
  )
  # group_input_004.Iterations -> repeat_input_005.Iterations
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Group Input.004"].outputs[3],
    carve_sdf_1.nodes["Repeat Input.005"].inputs[0]
  )
  # mesh_to_points_005.Points -> join_geometry_003.Geometry
  carve_sdf_1.links.new(
    carve_sdf_1.nodes["Mesh to Points.005"].outputs[0],
    carve_sdf_1.nodes["Join Geometry.003"].inputs[0]
  )

  return carve_sdf_1


def get_nearest_point_node_group():
  node_name = "Nearest Point"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]
  
  """Initialize Nearest Point node group"""
  nearest_point_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  nearest_point_1.color_tag = 'NONE'
  nearest_point_1.description = ""
  nearest_point_1.default_group_node_width = 140
  nearest_point_1.show_modifier_manage_panel = True

  # nearest_point_1 interface

  # Socket Position
  position_socket = nearest_point_1.interface.new_socket(name="Position", in_out='OUTPUT', socket_type='NodeSocketVector')
  position_socket.default_value = (0.0, 0.0, 0.0)
  position_socket.min_value = -3.4028234663852886e+38
  position_socket.max_value = 3.4028234663852886e+38
  position_socket.subtype = 'NONE'
  position_socket.attribute_domain = 'POINT'
  position_socket.default_input = 'VALUE'
  position_socket.structure_type = 'AUTO'

  # Socket Distance
  distance_socket = nearest_point_1.interface.new_socket(name="Distance", in_out='OUTPUT', socket_type='NodeSocketFloat')
  distance_socket.default_value = 0.0
  distance_socket.min_value = -3.4028234663852886e+38
  distance_socket.max_value = 3.4028234663852886e+38
  distance_socket.subtype = 'NONE'
  distance_socket.attribute_domain = 'POINT'
  distance_socket.default_input = 'VALUE'
  distance_socket.structure_type = 'AUTO'

  # Socket Geometry
  geometry_socket = nearest_point_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
  geometry_socket.attribute_domain = 'POINT'
  geometry_socket.default_input = 'VALUE'
  geometry_socket.structure_type = 'AUTO'

  # Socket Position
  position_socket_1 = nearest_point_1.interface.new_socket(name="Position", in_out='INPUT', socket_type='NodeSocketVector')
  position_socket_1.default_value = (0.0, 0.0, 0.0)
  position_socket_1.min_value = -3.4028234663852886e+38
  position_socket_1.max_value = 3.4028234663852886e+38
  position_socket_1.subtype = 'NONE'
  position_socket_1.attribute_domain = 'POINT'
  position_socket_1.hide_value = True
  position_socket_1.default_input = 'VALUE'
  position_socket_1.structure_type = 'AUTO'

  # Initialize nearest_point_1 nodes

  # Node Sample Nearest
  sample_nearest = nearest_point_1.nodes.new("GeometryNodeSampleNearest")
  sample_nearest.name = "Sample Nearest"
  sample_nearest.show_options = True
  sample_nearest.domain = 'POINT'

  # Node Sample Index
  sample_index = nearest_point_1.nodes.new("GeometryNodeSampleIndex")
  sample_index.name = "Sample Index"
  sample_index.show_options = True
  sample_index.clamp = False
  sample_index.data_type = 'FLOAT_VECTOR'
  sample_index.domain = 'POINT'

  # Node Group Output
  group_output = nearest_point_1.nodes.new("NodeGroupOutput")
  group_output.name = "Group Output"
  group_output.show_options = True
  group_output.is_active_output = True
  group_output.inputs[2].hide = True

  # Node Group Input
  group_input = nearest_point_1.nodes.new("NodeGroupInput")
  group_input.name = "Group Input"
  group_input.show_options = True
  group_input.outputs[2].hide = True

  # Node Vector Math
  vector_math = nearest_point_1.nodes.new("ShaderNodeVectorMath")
  vector_math.name = "Vector Math"
  vector_math.hide = True
  vector_math.show_options = True
  vector_math.operation = 'DISTANCE'

  # Node Group Input.001
  group_input_001 = nearest_point_1.nodes.new("NodeGroupInput")
  group_input_001.label = "Position"
  group_input_001.name = "Group Input.001"
  group_input_001.hide = True
  group_input_001.show_options = True
  group_input_001.outputs[0].hide = True
  group_input_001.outputs[2].hide = True

  # Set locations
  nearest_point_1.nodes["Sample Nearest"].location = (49.962913513183594, -84.510498046875)
  nearest_point_1.nodes["Sample Index"].location = (51.33625030517578, 117.34970092773438)
  nearest_point_1.nodes["Group Output"].location = (328.24993896484375, 116.326904296875)
  nearest_point_1.nodes["Group Input"].location = (-100.41714477539062, -45.57501983642578)
  nearest_point_1.nodes["Vector Math"].location = (210.3355712890625, 70.0045166015625)
  nearest_point_1.nodes["Group Input.001"].location = (210.8857421875, 32.8099365234375)

  # Set dimensions
  nearest_point_1.nodes["Sample Nearest"].width  = 140.0
  nearest_point_1.nodes["Sample Nearest"].height = 100.0

  nearest_point_1.nodes["Sample Index"].width  = 137.67919921875
  nearest_point_1.nodes["Sample Index"].height = 100.0

  nearest_point_1.nodes["Group Output"].width  = 104.1322021484375
  nearest_point_1.nodes["Group Output"].height = 100.0

  nearest_point_1.nodes["Group Input"].width  = 96.50079345703125
  nearest_point_1.nodes["Group Input"].height = 100.0

  nearest_point_1.nodes["Vector Math"].width  = 100.0
  nearest_point_1.nodes["Vector Math"].height = 100.0

  nearest_point_1.nodes["Group Input.001"].width  = 99.24896240234375
  nearest_point_1.nodes["Group Input.001"].height = 100.0


  # Initialize nearest_point_1 links

  # sample_nearest.Index -> sample_index.Index
  nearest_point_1.links.new(
    nearest_point_1.nodes["Sample Nearest"].outputs[0],
    nearest_point_1.nodes["Sample Index"].inputs[2]
  )
  # group_input.Geometry -> sample_nearest.Geometry
  nearest_point_1.links.new(
    nearest_point_1.nodes["Group Input"].outputs[0],
    nearest_point_1.nodes["Sample Nearest"].inputs[0]
  )
  # group_input.Position -> sample_nearest.Sample Position
  nearest_point_1.links.new(
    nearest_point_1.nodes["Group Input"].outputs[1],
    nearest_point_1.nodes["Sample Nearest"].inputs[1]
  )
  # group_input.Position -> sample_index.Value
  nearest_point_1.links.new(
    nearest_point_1.nodes["Group Input"].outputs[1],
    nearest_point_1.nodes["Sample Index"].inputs[1]
  )
  # group_input.Geometry -> sample_index.Geometry
  nearest_point_1.links.new(
    nearest_point_1.nodes["Group Input"].outputs[0],
    nearest_point_1.nodes["Sample Index"].inputs[0]
  )
  # sample_index.Value -> group_output.Position
  nearest_point_1.links.new(
    nearest_point_1.nodes["Sample Index"].outputs[0],
    nearest_point_1.nodes["Group Output"].inputs[0]
  )
  # sample_index.Value -> vector_math.Vector
  nearest_point_1.links.new(
    nearest_point_1.nodes["Sample Index"].outputs[0],
    nearest_point_1.nodes["Vector Math"].inputs[0]
  )
  # group_input_001.Position -> vector_math.Vector
  nearest_point_1.links.new(
    nearest_point_1.nodes["Group Input.001"].outputs[1],
    nearest_point_1.nodes["Vector Math"].inputs[1]
  )
  # vector_math.Value -> group_output.Distance
  nearest_point_1.links.new(
    nearest_point_1.nodes["Vector Math"].outputs[1],
    nearest_point_1.nodes["Group Output"].inputs[1]
  )

  return nearest_point_1


def get_normal_offset_node_group():
  node_name = "Normal Offset"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]
  
  """Initialize Normal Offset node group"""
  normal_offset_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  normal_offset_1.color_tag = 'NONE'
  normal_offset_1.description = ""
  normal_offset_1.default_group_node_width = 140
  normal_offset_1.show_modifier_manage_panel = True

  # normal_offset_1 interface

  # Socket Position
  position_socket = normal_offset_1.interface.new_socket(name="Position", in_out='OUTPUT', socket_type='NodeSocketVector')
  position_socket.default_value = (0.0, 0.0, 0.0)
  position_socket.min_value = -3.4028234663852886e+38
  position_socket.max_value = 3.4028234663852886e+38
  position_socket.subtype = 'NONE'
  position_socket.attribute_domain = 'POINT'
  position_socket.default_input = 'VALUE'
  position_socket.structure_type = 'AUTO'

  # Socket Target
  target_socket = normal_offset_1.interface.new_socket(name="Target", in_out='INPUT', socket_type='NodeSocketVector')
  target_socket.default_value = (0.0, 0.0, 0.0)
  target_socket.min_value = -10000.0
  target_socket.max_value = 10000.0
  target_socket.subtype = 'NONE'
  target_socket.attribute_domain = 'POINT'
  target_socket.hide_value = True
  target_socket.default_input = 'VALUE'
  target_socket.structure_type = 'AUTO'

  # Initialize normal_offset_1 nodes

  # Node Position.003
  position_003 = normal_offset_1.nodes.new("GeometryNodeInputPosition")
  position_003.name = "Position.003"
  position_003.hide = True
  position_003.show_options = True

  # Node Normal.001
  normal_001 = normal_offset_1.nodes.new("GeometryNodeInputNormal")
  normal_001.name = "Normal.001"
  normal_001.hide = True
  normal_001.show_options = True
  normal_001.legacy_corner_normals = False
  normal_001.outputs[1].hide = True

  # Node Vector Math
  vector_math = normal_offset_1.nodes.new("ShaderNodeVectorMath")
  vector_math.name = "Vector Math"
  vector_math.hide = True
  vector_math.show_options = True
  vector_math.operation = 'DOT_PRODUCT'

  # Node Vector Math.004
  vector_math_004 = normal_offset_1.nodes.new("ShaderNodeVectorMath")
  vector_math_004.name = "Vector Math.004"
  vector_math_004.hide = True
  vector_math_004.show_options = True
  vector_math_004.operation = 'DOT_PRODUCT'

  # Node Math.002
  math_002 = normal_offset_1.nodes.new("ShaderNodeMath")
  math_002.name = "Math.002"
  math_002.hide = True
  math_002.show_options = True
  math_002.operation = 'SUBTRACT'
  math_002.use_clamp = False

  # Node Vector Math.005
  vector_math_005 = normal_offset_1.nodes.new("ShaderNodeVectorMath")
  vector_math_005.name = "Vector Math.005"
  vector_math_005.hide = True
  vector_math_005.show_options = True
  vector_math_005.operation = 'SCALE'

  # Node Vector Math.006
  vector_math_006 = normal_offset_1.nodes.new("ShaderNodeVectorMath")
  vector_math_006.name = "Vector Math.006"
  vector_math_006.hide = True
  vector_math_006.show_options = True
  vector_math_006.operation = 'ADD'

  # Node Group Output
  group_output = normal_offset_1.nodes.new("NodeGroupOutput")
  group_output.label = "Position Out"
  group_output.name = "Group Output"
  group_output.hide = True
  group_output.show_options = True
  group_output.is_active_output = True
  group_output.inputs[1].hide = True

  # Node Group Input
  group_input = normal_offset_1.nodes.new("NodeGroupInput")
  group_input.label = "Target"
  group_input.name = "Group Input"
  group_input.hide = True
  group_input.show_options = True
  group_input.outputs[1].hide = True

  # Node Reroute
  reroute = normal_offset_1.nodes.new("NodeReroute")
  reroute.name = "Reroute"
  reroute.show_options = True
  reroute.socket_idname = "NodeSocketVector"
  # Node Reroute.001
  reroute_001 = normal_offset_1.nodes.new("NodeReroute")
  reroute_001.name = "Reroute.001"
  reroute_001.show_options = True
  reroute_001.socket_idname = "NodeSocketVector"
  # Set locations
  normal_offset_1.nodes["Position.003"].location = (-259.773193359375, -36.72711944580078)
  normal_offset_1.nodes["Normal.001"].location = (-259.3927001953125, 2.4444260597229004)
  normal_offset_1.nodes["Vector Math"].location = (-131.80618286132812, 40.369178771972656)
  normal_offset_1.nodes["Vector Math.004"].location = (-131.80618286132812, 2.2091081142425537)
  normal_offset_1.nodes["Math.002"].location = (-12.845857620239258, 23.469697952270508)
  normal_offset_1.nodes["Vector Math.005"].location = (118.69123077392578, 2.254807472229004)
  normal_offset_1.nodes["Vector Math.006"].location = (119.40107727050781, -32.85173797607422)
  normal_offset_1.nodes["Group Output"].location = (240.68240356445312, -33.660926818847656)
  normal_offset_1.nodes["Group Input"].location = (-261.30322265625, 41.14594650268555)
  normal_offset_1.nodes["Reroute"].location = (-130.6710968017578, -32.93149948120117)
  normal_offset_1.nodes["Reroute.001"].location = (88.57219696044922, -33.98442459106445)

  # Set dimensions
  normal_offset_1.nodes["Position.003"].width  = 100.0
  normal_offset_1.nodes["Position.003"].height = 100.0

  normal_offset_1.nodes["Normal.001"].width  = 100.0
  normal_offset_1.nodes["Normal.001"].height = 100.0

  normal_offset_1.nodes["Vector Math"].width  = 100.0
  normal_offset_1.nodes["Vector Math"].height = 100.0

  normal_offset_1.nodes["Vector Math.004"].width  = 100.0
  normal_offset_1.nodes["Vector Math.004"].height = 100.0

  normal_offset_1.nodes["Math.002"].width  = 100.0
  normal_offset_1.nodes["Math.002"].height = 100.0

  normal_offset_1.nodes["Vector Math.005"].width  = 100.0
  normal_offset_1.nodes["Vector Math.005"].height = 100.0

  normal_offset_1.nodes["Vector Math.006"].width  = 100.0
  normal_offset_1.nodes["Vector Math.006"].height = 100.0

  normal_offset_1.nodes["Group Output"].width  = 108.78839111328125
  normal_offset_1.nodes["Group Output"].height = 100.0

  normal_offset_1.nodes["Group Input"].width  = 100.33514404296875
  normal_offset_1.nodes["Group Input"].height = 100.0

  normal_offset_1.nodes["Reroute"].width  = 20.0
  normal_offset_1.nodes["Reroute"].height = 100.0

  normal_offset_1.nodes["Reroute.001"].width  = 20.0
  normal_offset_1.nodes["Reroute.001"].height = 100.0


  # Initialize normal_offset_1 links

  # normal_001.Normal -> vector_math.Vector
  normal_offset_1.links.new(
    normal_offset_1.nodes["Normal.001"].outputs[0],
    normal_offset_1.nodes["Vector Math"].inputs[1]
  )
  # normal_001.Normal -> vector_math_004.Vector
  normal_offset_1.links.new(
    normal_offset_1.nodes["Normal.001"].outputs[0],
    normal_offset_1.nodes["Vector Math.004"].inputs[1]
  )
  # position_003.Position -> vector_math_004.Vector
  normal_offset_1.links.new(
    normal_offset_1.nodes["Position.003"].outputs[0],
    normal_offset_1.nodes["Vector Math.004"].inputs[0]
  )
  # vector_math.Value -> math_002.Value
  normal_offset_1.links.new(
    normal_offset_1.nodes["Vector Math"].outputs[1],
    normal_offset_1.nodes["Math.002"].inputs[0]
  )
  # vector_math_004.Value -> math_002.Value
  normal_offset_1.links.new(
    normal_offset_1.nodes["Vector Math.004"].outputs[1],
    normal_offset_1.nodes["Math.002"].inputs[1]
  )
  # reroute_001.Output -> vector_math_005.Vector
  normal_offset_1.links.new(
    normal_offset_1.nodes["Reroute.001"].outputs[0],
    normal_offset_1.nodes["Vector Math.005"].inputs[0]
  )
  # math_002.Value -> vector_math_005.Scale
  normal_offset_1.links.new(
    normal_offset_1.nodes["Math.002"].outputs[0],
    normal_offset_1.nodes["Vector Math.005"].inputs[3]
  )
  # group_input.Target -> vector_math.Vector
  normal_offset_1.links.new(
    normal_offset_1.nodes["Group Input"].outputs[0],
    normal_offset_1.nodes["Vector Math"].inputs[0]
  )
  # vector_math_006.Vector -> group_output.Position
  normal_offset_1.links.new(
    normal_offset_1.nodes["Vector Math.006"].outputs[0],
    normal_offset_1.nodes["Group Output"].inputs[0]
  )
  # normal_001.Normal -> reroute.Input
  normal_offset_1.links.new(
    normal_offset_1.nodes["Normal.001"].outputs[0],
    normal_offset_1.nodes["Reroute"].inputs[0]
  )
  # reroute.Output -> reroute_001.Input
  normal_offset_1.links.new(
    normal_offset_1.nodes["Reroute"].outputs[0],
    normal_offset_1.nodes["Reroute.001"].inputs[0]
  )
  # position_003.Position -> vector_math_006.Vector
  normal_offset_1.links.new(
    normal_offset_1.nodes["Position.003"].outputs[0],
    normal_offset_1.nodes["Vector Math.006"].inputs[1]
  )
  # vector_math_005.Vector -> vector_math_006.Vector
  normal_offset_1.links.new(
    normal_offset_1.nodes["Vector Math.005"].outputs[0],
    normal_offset_1.nodes["Vector Math.006"].inputs[0]
  )

  return normal_offset_1


def get_offset_nearst_node_group():
  node_name = "Offset Nearst"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]
  
  """Initialize Offset Nearst node group"""
  offset_nearst_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  offset_nearst_1.color_tag = 'NONE'
  offset_nearst_1.description = ""
  offset_nearst_1.default_group_node_width = 140
  offset_nearst_1.show_modifier_manage_panel = True

  # offset_nearst_1 interface

  # Socket Geometry
  geometry_socket = offset_nearst_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
  geometry_socket.attribute_domain = 'POINT'
  geometry_socket.default_input = 'VALUE'
  geometry_socket.structure_type = 'AUTO'

  # Socket Geometry
  geometry_socket_1 = offset_nearst_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
  geometry_socket_1.attribute_domain = 'POINT'
  geometry_socket_1.default_input = 'VALUE'
  geometry_socket_1.structure_type = 'AUTO'

  # Socket Point Cloud
  point_cloud_socket = offset_nearst_1.interface.new_socket(name="Point Cloud", in_out='INPUT', socket_type='NodeSocketGeometry')
  point_cloud_socket.attribute_domain = 'POINT'
  point_cloud_socket.default_input = 'VALUE'
  point_cloud_socket.structure_type = 'AUTO'

  # Socket Iterations
  iterations_socket = offset_nearst_1.interface.new_socket(name="Iterations", in_out='INPUT', socket_type='NodeSocketInt')
  iterations_socket.default_value = 4
  iterations_socket.min_value = 0
  iterations_socket.max_value = 2147483647
  iterations_socket.subtype = 'NONE'
  iterations_socket.attribute_domain = 'POINT'
  iterations_socket.default_input = 'VALUE'
  iterations_socket.structure_type = 'AUTO'

  # Socket Snap Last
  snap_last_socket = offset_nearst_1.interface.new_socket(name="Snap Last", in_out='INPUT', socket_type='NodeSocketBool')
  snap_last_socket.default_value = False
  snap_last_socket.attribute_domain = 'POINT'
  snap_last_socket.default_input = 'VALUE'
  snap_last_socket.structure_type = 'AUTO'

  # Initialize offset_nearst_1 nodes

  # Node Set Position.004
  set_position_004 = offset_nearst_1.nodes.new("GeometryNodeSetPosition")
  set_position_004.name = "Set Position.004"
  set_position_004.hide = True
  set_position_004.show_options = True
  set_position_004.inputs[1].hide = True
  set_position_004.inputs[3].hide = True
  # Selection
  set_position_004.inputs[1].default_value = True
  # Offset
  set_position_004.inputs[3].default_value = (0.0, 0.0, 0.0)

  # Node Group.008
  group_008 = offset_nearst_1.nodes.new("GeometryNodeGroup")
  group_008.name = "Group.008"
  group_008.hide = True
  group_008.node_tree = get_nearest_point_node_group()
  group_008.outputs[1].hide = True

  # Node Group.009
  group_009 = offset_nearst_1.nodes.new("GeometryNodeGroup")
  group_009.name = "Group.009"
  group_009.hide = True
  group_009.node_tree = get_normal_offset_node_group()

  # Node Position
  position = offset_nearst_1.nodes.new("GeometryNodeInputPosition")
  position.name = "Position"
  position.hide = True
  position.show_options = True

  # Node Repeat Input
  repeat_input = offset_nearst_1.nodes.new("GeometryNodeRepeatInput")
  repeat_input.name = "Repeat Input"
  repeat_input.hide = True
  repeat_input.show_options = True
  repeat_input.outputs[0].hide = True
  # Node Repeat Output
  repeat_output = offset_nearst_1.nodes.new("GeometryNodeRepeatOutput")
  repeat_output.name = "Repeat Output"
  repeat_output.hide = True
  repeat_output.show_options = True
  repeat_output.active_index = 0
  repeat_output.inspection_index = 0
  repeat_output.repeat_items.clear()
  # Create item "Geometry"
  repeat_output.repeat_items.new('GEOMETRY', "Geometry")
  repeat_output.inputs[1].hide = True
  repeat_output.outputs[1].hide = True

  # Node Group Output
  group_output = offset_nearst_1.nodes.new("NodeGroupOutput")
  group_output.label = "Geometry Out"
  group_output.name = "Group Output"
  group_output.hide = True
  group_output.show_options = True
  group_output.is_active_output = True
  group_output.inputs[1].hide = True

  # Node Group Input
  group_input = offset_nearst_1.nodes.new("NodeGroupInput")
  group_input.label = "Geometry"
  group_input.name = "Group Input"
  group_input.hide = True
  group_input.show_options = True
  group_input.outputs[1].hide = True
  group_input.outputs[2].hide = True
  group_input.outputs[3].hide = True
  group_input.outputs[4].hide = True

  # Node Group Input.001
  group_input_001 = offset_nearst_1.nodes.new("NodeGroupInput")
  group_input_001.label = "Point Cloud"
  group_input_001.name = "Group Input.001"
  group_input_001.hide = True
  group_input_001.show_options = True
  group_input_001.outputs[0].hide = True
  group_input_001.outputs[2].hide = True
  group_input_001.outputs[3].hide = True
  group_input_001.outputs[4].hide = True

  # Node Set Position.005
  set_position_005 = offset_nearst_1.nodes.new("GeometryNodeSetPosition")
  set_position_005.name = "Set Position.005"
  set_position_005.hide = True
  set_position_005.show_options = True
  set_position_005.inputs[1].hide = True
  set_position_005.inputs[3].hide = True
  # Selection
  set_position_005.inputs[1].default_value = True
  # Offset
  set_position_005.inputs[3].default_value = (0.0, 0.0, 0.0)

  # Node Group.010
  group_010 = offset_nearst_1.nodes.new("GeometryNodeGroup")
  group_010.name = "Group.010"
  group_010.hide = True
  group_010.node_tree = get_nearest_point_node_group()
  group_010.outputs[1].hide = True

  # Node Position.001
  position_001 = offset_nearst_1.nodes.new("GeometryNodeInputPosition")
  position_001.name = "Position.001"
  position_001.hide = True
  position_001.show_options = True

  # Node Group Input.002
  group_input_002 = offset_nearst_1.nodes.new("NodeGroupInput")
  group_input_002.label = "Point Cloud"
  group_input_002.name = "Group Input.002"
  group_input_002.hide = True
  group_input_002.show_options = True
  group_input_002.outputs[0].hide = True
  group_input_002.outputs[2].hide = True
  group_input_002.outputs[3].hide = True
  group_input_002.outputs[4].hide = True

  # Node Switch
  switch = offset_nearst_1.nodes.new("GeometryNodeSwitch")
  switch.name = "Switch"
  switch.hide = True
  switch.show_options = True
  switch.input_type = 'GEOMETRY'

  # Node Group Input.003
  group_input_003 = offset_nearst_1.nodes.new("NodeGroupInput")
  group_input_003.label = "Snap Last"
  group_input_003.name = "Group Input.003"
  group_input_003.hide = True
  group_input_003.show_options = True
  group_input_003.outputs[0].hide = True
  group_input_003.outputs[1].hide = True
  group_input_003.outputs[2].hide = True
  group_input_003.outputs[4].hide = True

  # Node Reroute
  reroute = offset_nearst_1.nodes.new("NodeReroute")
  reroute.name = "Reroute"
  reroute.show_options = True
  reroute.socket_idname = "NodeSocketGeometry"
  # Node Reroute.001
  reroute_001 = offset_nearst_1.nodes.new("NodeReroute")
  reroute_001.name = "Reroute.001"
  reroute_001.show_options = True
  reroute_001.socket_idname = "NodeSocketGeometry"
  # Node Frame
  frame = offset_nearst_1.nodes.new("NodeFrame")
  frame.label = "Snap to Closest Point"
  frame.name = "Frame"
  frame.show_options = True
  frame.label_size = 20
  frame.shrink = True

  # Node Group Input.004
  group_input_004 = offset_nearst_1.nodes.new("NodeGroupInput")
  group_input_004.label = "Iterations"
  group_input_004.name = "Group Input.004"
  group_input_004.hide = True
  group_input_004.show_options = True
  group_input_004.outputs[0].hide = True
  group_input_004.outputs[1].hide = True
  group_input_004.outputs[3].hide = True
  group_input_004.outputs[4].hide = True

  # Node Frame.001
  frame_001 = offset_nearst_1.nodes.new("NodeFrame")
  frame_001.label = "Iterate Toward Closest Point"
  frame_001.name = "Frame.001"
  frame_001.show_options = True
  frame_001.label_size = 20
  frame_001.shrink = True

  # Process zone input Repeat Input
  repeat_input.pair_with_output(repeat_output)



  # Set parents
  offset_nearst_1.nodes["Set Position.004"].parent = offset_nearst_1.nodes["Frame.001"]
  offset_nearst_1.nodes["Group.008"].parent = offset_nearst_1.nodes["Frame.001"]
  offset_nearst_1.nodes["Group.009"].parent = offset_nearst_1.nodes["Frame.001"]
  offset_nearst_1.nodes["Position"].parent = offset_nearst_1.nodes["Frame.001"]
  offset_nearst_1.nodes["Repeat Input"].parent = offset_nearst_1.nodes["Frame.001"]
  offset_nearst_1.nodes["Repeat Output"].parent = offset_nearst_1.nodes["Frame.001"]
  offset_nearst_1.nodes["Group Input"].parent = offset_nearst_1.nodes["Frame.001"]
  offset_nearst_1.nodes["Group Input.001"].parent = offset_nearst_1.nodes["Frame.001"]
  offset_nearst_1.nodes["Set Position.005"].parent = offset_nearst_1.nodes["Frame"]
  offset_nearst_1.nodes["Group.010"].parent = offset_nearst_1.nodes["Frame"]
  offset_nearst_1.nodes["Position.001"].parent = offset_nearst_1.nodes["Frame"]
  offset_nearst_1.nodes["Group Input.002"].parent = offset_nearst_1.nodes["Frame"]
  offset_nearst_1.nodes["Switch"].parent = offset_nearst_1.nodes["Frame"]
  offset_nearst_1.nodes["Group Input.003"].parent = offset_nearst_1.nodes["Frame"]
  offset_nearst_1.nodes["Reroute"].parent = offset_nearst_1.nodes["Frame"]
  offset_nearst_1.nodes["Reroute.001"].parent = offset_nearst_1.nodes["Frame"]
  offset_nearst_1.nodes["Group Input.004"].parent = offset_nearst_1.nodes["Frame.001"]

  # Set locations
  offset_nearst_1.nodes["Set Position.004"].location = (268.4007568359375, -60.60466003417969)
  offset_nearst_1.nodes["Group.008"].location = (270.2705993652344, -133.89791870117188)
  offset_nearst_1.nodes["Group.009"].location = (267.8958740234375, -96.12541198730469)
  offset_nearst_1.nodes["Position"].location = (146.48406982421875, -151.76663208007812)
  offset_nearst_1.nodes["Repeat Input"].location = (144.32069396972656, -79.52198791503906)
  offset_nearst_1.nodes["Repeat Output"].location = (402.03143310546875, -59.91487121582031)
  offset_nearst_1.nodes["Group Output"].location = (584.2669677734375, 85.59648132324219)
  offset_nearst_1.nodes["Group Input"].location = (29.974273681640625, -84.94363403320312)
  offset_nearst_1.nodes["Group Input.001"].location = (146.00747680664062, -115.39196014404297)
  offset_nearst_1.nodes["Set Position.005"].location = (152.1510009765625, -86.62313079833984)
  offset_nearst_1.nodes["Group.010"].location = (151.8896484375, -126.32303619384766)
  offset_nearst_1.nodes["Position.001"].location = (31.067138671875, -129.35986328125)
  offset_nearst_1.nodes["Group Input.002"].location = (31.183380126953125, -94.17173767089844)
  offset_nearst_1.nodes["Switch"].location = (151.57745361328125, -45.12620544433594)
  offset_nearst_1.nodes["Group Input.003"].location = (30.240509033203125, -44.306396484375)
  offset_nearst_1.nodes["Reroute"].location = (39.285797119140625, -77.84278106689453)
  offset_nearst_1.nodes["Reroute.001"].location = (122.17684936523438, -78.14617919921875)
  offset_nearst_1.nodes["Frame"].location = (271.5, 131.0)
  offset_nearst_1.nodes["Group Input.004"].location = (144.76559448242188, -45.68585205078125)
  offset_nearst_1.nodes["Frame.001"].location = (-286.5, 125.5)

  # Set dimensions
  offset_nearst_1.nodes["Set Position.004"].width  = 109.50076293945312
  offset_nearst_1.nodes["Set Position.004"].height = 100.0

  offset_nearst_1.nodes["Group.008"].width  = 109.70138549804688
  offset_nearst_1.nodes["Group.008"].height = 100.0

  offset_nearst_1.nodes["Group.009"].width  = 111.82037353515625
  offset_nearst_1.nodes["Group.009"].height = 100.0

  offset_nearst_1.nodes["Position"].width  = 100.0
  offset_nearst_1.nodes["Position"].height = 100.0

  offset_nearst_1.nodes["Repeat Input"].width  = 100.0
  offset_nearst_1.nodes["Repeat Input"].height = 100.0

  offset_nearst_1.nodes["Repeat Output"].width  = 100.0
  offset_nearst_1.nodes["Repeat Output"].height = 100.0

  offset_nearst_1.nodes["Group Output"].width  = 111.49017333984375
  offset_nearst_1.nodes["Group Output"].height = 100.0

  offset_nearst_1.nodes["Group Input"].width  = 94.55648803710938
  offset_nearst_1.nodes["Group Input"].height = 100.0

  offset_nearst_1.nodes["Group Input.001"].width  = 98.30776977539062
  offset_nearst_1.nodes["Group Input.001"].height = 100.0

  offset_nearst_1.nodes["Set Position.005"].width  = 109.50076293945312
  offset_nearst_1.nodes["Set Position.005"].height = 100.0

  offset_nearst_1.nodes["Group.010"].width  = 109.70138549804688
  offset_nearst_1.nodes["Group.010"].height = 100.0

  offset_nearst_1.nodes["Position.001"].width  = 100.0
  offset_nearst_1.nodes["Position.001"].height = 100.0

  offset_nearst_1.nodes["Group Input.002"].width  = 98.30776977539062
  offset_nearst_1.nodes["Group Input.002"].height = 100.0

  offset_nearst_1.nodes["Switch"].width  = 109.27572631835938
  offset_nearst_1.nodes["Switch"].height = 100.0

  offset_nearst_1.nodes["Group Input.003"].width  = 98.20317077636719
  offset_nearst_1.nodes["Group Input.003"].height = 100.0

  offset_nearst_1.nodes["Reroute"].width  = 20.0
  offset_nearst_1.nodes["Reroute"].height = 100.0

  offset_nearst_1.nodes["Reroute.001"].width  = 20.0
  offset_nearst_1.nodes["Reroute.001"].height = 100.0

  offset_nearst_1.nodes["Frame"].width  = 291.701416015625
  offset_nearst_1.nodes["Frame"].height = 183.5

  offset_nearst_1.nodes["Group Input.004"].width  = 98.94233703613281
  offset_nearst_1.nodes["Group Input.004"].height = 100.0

  offset_nearst_1.nodes["Frame.001"].width  = 532.0
  offset_nearst_1.nodes["Frame.001"].height = 206.0


  # Initialize offset_nearst_1 links

  # position.Position -> group_008.Position
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Position"].outputs[0],
    offset_nearst_1.nodes["Group.008"].inputs[1]
  )
  # group_008.Position -> group_009.Target
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Group.008"].outputs[0],
    offset_nearst_1.nodes["Group.009"].inputs[0]
  )
  # group_009.Position -> set_position_004.Position
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Group.009"].outputs[0],
    offset_nearst_1.nodes["Set Position.004"].inputs[2]
  )
  # set_position_004.Geometry -> repeat_output.Geometry
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Set Position.004"].outputs[0],
    offset_nearst_1.nodes["Repeat Output"].inputs[0]
  )
  # repeat_input.Geometry -> set_position_004.Geometry
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Repeat Input"].outputs[1],
    offset_nearst_1.nodes["Set Position.004"].inputs[0]
  )
  # group_input.Geometry -> repeat_input.Geometry
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Group Input"].outputs[0],
    offset_nearst_1.nodes["Repeat Input"].inputs[1]
  )
  # group_input_001.Point Cloud -> group_008.Geometry
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Group Input.001"].outputs[1],
    offset_nearst_1.nodes["Group.008"].inputs[0]
  )
  # position_001.Position -> group_010.Position
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Position.001"].outputs[0],
    offset_nearst_1.nodes["Group.010"].inputs[1]
  )
  # group_input_002.Point Cloud -> group_010.Geometry
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Group Input.002"].outputs[1],
    offset_nearst_1.nodes["Group.010"].inputs[0]
  )
  # reroute_001.Output -> set_position_005.Geometry
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Reroute.001"].outputs[0],
    offset_nearst_1.nodes["Set Position.005"].inputs[0]
  )
  # group_010.Position -> set_position_005.Position
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Group.010"].outputs[0],
    offset_nearst_1.nodes["Set Position.005"].inputs[2]
  )
  # set_position_005.Geometry -> switch.True
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Set Position.005"].outputs[0],
    offset_nearst_1.nodes["Switch"].inputs[2]
  )
  # reroute_001.Output -> switch.False
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Reroute.001"].outputs[0],
    offset_nearst_1.nodes["Switch"].inputs[1]
  )
  # switch.Output -> group_output.Geometry
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Switch"].outputs[0],
    offset_nearst_1.nodes["Group Output"].inputs[0]
  )
  # group_input_003.Snap Last -> switch.Switch
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Group Input.003"].outputs[3],
    offset_nearst_1.nodes["Switch"].inputs[0]
  )
  # repeat_output.Geometry -> reroute.Input
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Repeat Output"].outputs[0],
    offset_nearst_1.nodes["Reroute"].inputs[0]
  )
  # reroute.Output -> reroute_001.Input
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Reroute"].outputs[0],
    offset_nearst_1.nodes["Reroute.001"].inputs[0]
  )
  # group_input_004.Iterations -> repeat_input.Iterations
  offset_nearst_1.links.new(
    offset_nearst_1.nodes["Group Input.004"].outputs[2],
    offset_nearst_1.nodes["Repeat Input"].inputs[0]
  )

  return offset_nearst_1


def get_points_to_mesh_node_group():
  node_name = "Points to Mesh"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]

  """Initialize Points to Mesh node group"""
  points_to_mesh_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  points_to_mesh_1.color_tag = 'NONE'
  points_to_mesh_1.description = ""
  points_to_mesh_1.default_group_node_width = 140
  points_to_mesh_1.show_modifier_manage_panel = True

  # points_to_mesh_1 interface

  # Socket Mesh
  mesh_socket = points_to_mesh_1.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')
  mesh_socket.attribute_domain = 'POINT'
  mesh_socket.default_input = 'VALUE'
  mesh_socket.structure_type = 'AUTO'

  # Socket Points
  points_socket = points_to_mesh_1.interface.new_socket(name="Points", in_out='INPUT', socket_type='NodeSocketGeometry')
  points_socket.attribute_domain = 'POINT'
  points_socket.default_input = 'VALUE'
  points_socket.structure_type = 'AUTO'

  # Panel Iterations
  iterations_panel = points_to_mesh_1.interface.new_panel("Iterations")
  # Socket Course Iterations
  course_iterations_socket = points_to_mesh_1.interface.new_socket(name="Course Iterations", in_out='INPUT', socket_type='NodeSocketInt', parent = iterations_panel)
  course_iterations_socket.default_value = 4
  course_iterations_socket.min_value = 0
  course_iterations_socket.max_value = 2147483647
  course_iterations_socket.subtype = 'NONE'
  course_iterations_socket.attribute_domain = 'POINT'
  course_iterations_socket.default_input = 'VALUE'
  course_iterations_socket.structure_type = 'AUTO'

  # Socket Fine Iterations
  fine_iterations_socket = points_to_mesh_1.interface.new_socket(name="Fine Iterations", in_out='INPUT', socket_type='NodeSocketInt', parent = iterations_panel)
  fine_iterations_socket.default_value = 4
  fine_iterations_socket.min_value = 0
  fine_iterations_socket.max_value = 2147483647
  fine_iterations_socket.subtype = 'NONE'
  fine_iterations_socket.attribute_domain = 'POINT'
  fine_iterations_socket.default_input = 'VALUE'
  fine_iterations_socket.structure_type = 'AUTO'

  # Socket Subdivisions
  subdivisions_socket = points_to_mesh_1.interface.new_socket(name="Subdivisions", in_out='INPUT', socket_type='NodeSocketInt', parent = iterations_panel)
  subdivisions_socket.default_value = 0
  subdivisions_socket.min_value = 0
  subdivisions_socket.max_value = 6
  subdivisions_socket.subtype = 'NONE'
  subdivisions_socket.attribute_domain = 'POINT'
  subdivisions_socket.default_input = 'VALUE'
  subdivisions_socket.structure_type = 'AUTO'


  # Panel SDF Simplify
  sdf_simplify_panel = points_to_mesh_1.interface.new_panel("SDF Simplify")
  # Socket SDF Simplify Enable
  sdf_simplify_enable_socket = points_to_mesh_1.interface.new_socket(name="SDF Simplify Enable", in_out='INPUT', socket_type='NodeSocketBool', parent = sdf_simplify_panel)
  sdf_simplify_enable_socket.default_value = False
  sdf_simplify_enable_socket.attribute_domain = 'POINT'
  sdf_simplify_enable_socket.default_input = 'VALUE'
  sdf_simplify_enable_socket.structure_type = 'AUTO'

  # Socket Voxel Size
  voxel_size_socket = points_to_mesh_1.interface.new_socket(name="Voxel Size", in_out='INPUT', socket_type='NodeSocketFloat', parent = sdf_simplify_panel)
  voxel_size_socket.default_value = 0.009999999776482582
  voxel_size_socket.min_value = 0.009999999776482582
  voxel_size_socket.max_value = 3.4028234663852886e+38
  voxel_size_socket.subtype = 'DISTANCE'
  voxel_size_socket.attribute_domain = 'POINT'
  voxel_size_socket.default_input = 'VALUE'
  voxel_size_socket.structure_type = 'AUTO'


  # Initialize points_to_mesh_1 nodes

  # Node Convex Hull.006
  convex_hull_006 = points_to_mesh_1.nodes.new("GeometryNodeConvexHull")
  convex_hull_006.name = "Convex Hull.006"
  convex_hull_006.hide = True
  convex_hull_006.show_options = True

  # Node Group.002
  group_002 = points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_002.name = "Group.002"
  group_002.show_options = True
  group_002.node_tree = get_carve_sdf_node_group()
  # Socket_3
  group_002.inputs[2].default_value = 0.019999999552965164

  # Node Group.008
  group_008 = points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_008.name = "Group.008"
  group_008.show_options = True
  group_008.node_tree = get_carve_sdf_node_group()
  # Socket_3
  group_008.inputs[2].default_value = 0.004000000189989805

  # Node Reroute.005
  reroute_005 = points_to_mesh_1.nodes.new("NodeReroute")
  reroute_005.name = "Reroute.005"
  reroute_005.show_options = True
  reroute_005.socket_idname = "NodeSocketGeometry"
  # Node Reroute.010
  reroute_010 = points_to_mesh_1.nodes.new("NodeReroute")
  reroute_010.name = "Reroute.010"
  reroute_010.show_options = True
  reroute_010.socket_idname = "NodeSocketGeometry"
  # Node Group.009
  group_009 = points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_009.name = "Group.009"
  group_009.show_options = True
  group_009.node_tree = get_smooth_geometry_node_group()
  # Socket_2
  group_009.inputs[1].default_value = True
  # Socket_3
  group_009.inputs[2].default_value = 1
  # Socket_4
  group_009.inputs[3].default_value = 1.0

  # Node Group.013
  group_013 = points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_013.name = "Group.013"
  group_013.show_options = True
  group_013.node_tree = get_offset_nearst_node_group()
  # Socket_3
  group_013.inputs[2].default_value = 4
  # Socket_4
  group_013.inputs[3].default_value = False

  # Node Mesh to SDF Grid
  mesh_to_sdf_grid = points_to_mesh_1.nodes.new("GeometryNodeMeshToSDFGrid")
  mesh_to_sdf_grid.name = "Mesh to SDF Grid"
  mesh_to_sdf_grid.show_options = True
  # Band Width
  mesh_to_sdf_grid.inputs[2].default_value = 3

  # Node Grid to Mesh
  grid_to_mesh = points_to_mesh_1.nodes.new("GeometryNodeGridToMesh")
  grid_to_mesh.name = "Grid to Mesh"
  grid_to_mesh.show_options = True
  # Threshold
  grid_to_mesh.inputs[1].default_value = 0.009999999776482582
  # Adaptivity
  grid_to_mesh.inputs[2].default_value = 0.0

  # Node Group.015
  group_015 = points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_015.name = "Group.015"
  group_015.show_options = True
  group_015.node_tree = get_offset_nearst_node_group()
  # Socket_3
  group_015.inputs[2].default_value = 4
  # Socket_4
  group_015.inputs[3].default_value = False

  # Node Group Output
  group_output = points_to_mesh_1.nodes.new("NodeGroupOutput")
  group_output.label = "Mesh Out"
  group_output.name = "Group Output"
  group_output.hide = True
  group_output.show_options = True
  group_output.is_active_output = True
  group_output.inputs[1].hide = True

  # Node Group Input
  group_input = points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input.label = "Points"
  group_input.name = "Group Input"
  group_input.hide = True
  group_input.show_options = True
  group_input.outputs[1].hide = True
  group_input.outputs[2].hide = True
  group_input.outputs[3].hide = True
  group_input.outputs[4].hide = True
  group_input.outputs[5].hide = True
  group_input.outputs[6].hide = True

  # Node Switch
  switch = points_to_mesh_1.nodes.new("GeometryNodeSwitch")
  switch.name = "Switch"
  switch.hide = True
  switch.show_options = True
  switch.input_type = 'GEOMETRY'

  # Node Reroute
  reroute = points_to_mesh_1.nodes.new("NodeReroute")
  reroute.name = "Reroute"
  reroute.show_options = True
  reroute.socket_idname = "NodeSocketGeometry"
  # Node Reroute.001
  reroute_001 = points_to_mesh_1.nodes.new("NodeReroute")
  reroute_001.name = "Reroute.001"
  reroute_001.show_options = True
  reroute_001.socket_idname = "NodeSocketGeometry"
  # Node Frame
  frame = points_to_mesh_1.nodes.new("NodeFrame")
  frame.label = "SDF Simplify"
  frame.name = "Frame"
  frame.show_options = True
  frame.label_size = 20
  frame.shrink = True

  # Node Group Input.001
  group_input_001 = points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_001.label = "SDF Simplify"
  group_input_001.name = "Group Input.001"
  group_input_001.hide = True
  group_input_001.show_options = True
  group_input_001.outputs[0].hide = True
  group_input_001.outputs[1].hide = True
  group_input_001.outputs[2].hide = True
  group_input_001.outputs[3].hide = True
  group_input_001.outputs[5].hide = True
  group_input_001.outputs[6].hide = True

  # Node Frame.001
  frame_001 = points_to_mesh_1.nodes.new("NodeFrame")
  frame_001.label = "Mesh Out"
  frame_001.name = "Frame.001"
  frame_001.show_options = True
  frame_001.label_size = 20
  frame_001.shrink = True

  # Node Group Input.002
  group_input_002 = points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_002.label = "Points"
  group_input_002.name = "Group Input.002"
  group_input_002.hide = True
  group_input_002.show_options = True
  group_input_002.outputs[1].hide = True
  group_input_002.outputs[2].hide = True
  group_input_002.outputs[3].hide = True
  group_input_002.outputs[4].hide = True
  group_input_002.outputs[5].hide = True
  group_input_002.outputs[6].hide = True

  # Node Group Input.003
  group_input_003 = points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_003.label = "Course Iterations"
  group_input_003.name = "Group Input.003"
  group_input_003.hide = True
  group_input_003.show_options = True
  group_input_003.outputs[0].hide = True
  group_input_003.outputs[2].hide = True
  group_input_003.outputs[3].hide = True
  group_input_003.outputs[4].hide = True
  group_input_003.outputs[5].hide = True
  group_input_003.outputs[6].hide = True

  # Node Group Input.004
  group_input_004 = points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_004.label = "Fine Iterations"
  group_input_004.name = "Group Input.004"
  group_input_004.hide = True
  group_input_004.show_options = True
  group_input_004.outputs[0].hide = True
  group_input_004.outputs[1].hide = True
  group_input_004.outputs[3].hide = True
  group_input_004.outputs[4].hide = True
  group_input_004.outputs[5].hide = True
  group_input_004.outputs[6].hide = True

  # Node Frame.002
  frame_002 = points_to_mesh_1.nodes.new("NodeFrame")
  frame_002.label = "Two Stage Points to Dense Mesh"
  frame_002.name = "Frame.002"
  frame_002.show_options = True
  frame_002.label_size = 20
  frame_002.shrink = True

  # Node Group Input.005
  group_input_005 = points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_005.label = "Voxel Size"
  group_input_005.name = "Group Input.005"
  group_input_005.hide = True
  group_input_005.show_options = True
  group_input_005.outputs[0].hide = True
  group_input_005.outputs[1].hide = True
  group_input_005.outputs[2].hide = True
  group_input_005.outputs[3].hide = True
  group_input_005.outputs[4].hide = True
  group_input_005.outputs[6].hide = True

  # Node Subdivision Surface
  subdivision_surface = points_to_mesh_1.nodes.new("GeometryNodeSubdivisionSurface")
  subdivision_surface.name = "Subdivision Surface"
  subdivision_surface.show_options = True
  # Edge Crease
  subdivision_surface.inputs[2].default_value = 0.0
  # Vertex Crease
  subdivision_surface.inputs[3].default_value = 0.0
  # Limit Surface
  subdivision_surface.inputs[4].default_value = True
  # UV Smooth
  subdivision_surface.inputs[5].default_value = 'Keep Boundaries'
  # Boundary Smooth
  subdivision_surface.inputs[6].default_value = 'All'

  # Node Group Input.006
  group_input_006 = points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_006.label = "Subdivisions"
  group_input_006.name = "Group Input.006"
  group_input_006.hide = True
  group_input_006.show_options = True
  group_input_006.outputs[0].hide = True
  group_input_006.outputs[1].hide = True
  group_input_006.outputs[2].hide = True
  group_input_006.outputs[4].hide = True
  group_input_006.outputs[5].hide = True
  group_input_006.outputs[6].hide = True

  # Node Reroute.002
  reroute_002 = points_to_mesh_1.nodes.new("NodeReroute")
  reroute_002.name = "Reroute.002"
  reroute_002.show_options = True
  reroute_002.socket_idname = "NodeSocketGeometry"
  # Set parents
  points_to_mesh_1.nodes["Convex Hull.006"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Group.002"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Group.008"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Reroute.005"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Reroute.010"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Group.009"].parent = points_to_mesh_1.nodes["Frame"]
  points_to_mesh_1.nodes["Group.013"].parent = points_to_mesh_1.nodes["Frame"]
  points_to_mesh_1.nodes["Mesh to SDF Grid"].parent = points_to_mesh_1.nodes["Frame"]
  points_to_mesh_1.nodes["Grid to Mesh"].parent = points_to_mesh_1.nodes["Frame"]
  points_to_mesh_1.nodes["Group.015"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Group Output"].parent = points_to_mesh_1.nodes["Frame.001"]
  points_to_mesh_1.nodes["Group Input"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Switch"].parent = points_to_mesh_1.nodes["Frame.001"]
  points_to_mesh_1.nodes["Group Input.001"].parent = points_to_mesh_1.nodes["Frame.001"]
  points_to_mesh_1.nodes["Group Input.002"].parent = points_to_mesh_1.nodes["Frame"]
  points_to_mesh_1.nodes["Group Input.003"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Group Input.004"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Group Input.005"].parent = points_to_mesh_1.nodes["Frame"]
  points_to_mesh_1.nodes["Subdivision Surface"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Group Input.006"].parent = points_to_mesh_1.nodes["Frame.002"]
  points_to_mesh_1.nodes["Reroute.002"].parent = points_to_mesh_1.nodes["Frame.002"]

  # Set locations
  points_to_mesh_1.nodes["Convex Hull.006"].location = (29.912353515625, -132.2632293701172)
  points_to_mesh_1.nodes["Group.002"].location = (150.998779296875, -60.17950439453125)
  points_to_mesh_1.nodes["Group.008"].location = (340.66180419921875, -54.775146484375)
  points_to_mesh_1.nodes["Reroute.005"].location = (137.92303466796875, -273.253173828125)
  points_to_mesh_1.nodes["Reroute.010"].location = (301.76470947265625, -271.6414794921875)
  points_to_mesh_1.nodes["Group.009"].location = (30.202194213867188, -40.92115783691406)
  points_to_mesh_1.nodes["Group.013"].location = (546.1541748046875, -35.95509338378906)
  points_to_mesh_1.nodes["Mesh to SDF Grid"].location = (200.23434448242188, -40.46043395996094)
  points_to_mesh_1.nodes["Grid to Mesh"].location = (369.7870178222656, -38.31327819824219)
  points_to_mesh_1.nodes["Group.015"].location = (706.339111328125, -83.36258697509766)
  points_to_mesh_1.nodes["Group Output"].location = (158.0023193359375, -82.76097106933594)
  points_to_mesh_1.nodes["Group Input"].location = (30.2059326171875, -205.31211853027344)
  points_to_mesh_1.nodes["Switch"].location = (30.740966796875, -82.22657775878906)
  points_to_mesh_1.nodes["Reroute"].location = (119.78084564208984, 133.0867462158203)
  points_to_mesh_1.nodes["Reroute.001"].location = (794.4444580078125, 132.1764678955078)
  points_to_mesh_1.nodes["Frame"].location = (117.5, 108.0)
  points_to_mesh_1.nodes["Group Input.001"].location = (29.86322021484375, -40.02998352050781)
  points_to_mesh_1.nodes["Frame.001"].location = (851.0, 182.0)
  points_to_mesh_1.nodes["Group Input.002"].location = (427.17449951171875, -173.46678161621094)
  points_to_mesh_1.nodes["Group Input.003"].location = (145.60260009765625, -236.43479919433594)
  points_to_mesh_1.nodes["Group Input.004"].location = (336.64208984375, -233.56689453125)
  points_to_mesh_1.nodes["Frame.002"].location = (-772.5, 202.0)
  points_to_mesh_1.nodes["Group Input.005"].location = (200.67776489257812, -174.47616577148438)
  points_to_mesh_1.nodes["Subdivision Surface"].location = (515.4307861328125, -36.03227233886719)
  points_to_mesh_1.nodes["Group Input.006"].location = (513.692626953125, -231.58740234375)
  points_to_mesh_1.nodes["Reroute.002"].location = (648.4783935546875, -271.4192810058594)

  # Set dimensions
  points_to_mesh_1.nodes["Convex Hull.006"].width  = 100.0
  points_to_mesh_1.nodes["Convex Hull.006"].height = 100.0

  points_to_mesh_1.nodes["Group.002"].width  = 140.0
  points_to_mesh_1.nodes["Group.002"].height = 100.0

  points_to_mesh_1.nodes["Group.008"].width  = 140.0
  points_to_mesh_1.nodes["Group.008"].height = 100.0

  points_to_mesh_1.nodes["Reroute.005"].width  = 20.0
  points_to_mesh_1.nodes["Reroute.005"].height = 100.0

  points_to_mesh_1.nodes["Reroute.010"].width  = 20.0
  points_to_mesh_1.nodes["Reroute.010"].height = 100.0

  points_to_mesh_1.nodes["Group.009"].width  = 140.0
  points_to_mesh_1.nodes["Group.009"].height = 100.0

  points_to_mesh_1.nodes["Group.013"].width  = 115.2186279296875
  points_to_mesh_1.nodes["Group.013"].height = 100.0

  points_to_mesh_1.nodes["Mesh to SDF Grid"].width  = 130.269287109375
  points_to_mesh_1.nodes["Mesh to SDF Grid"].height = 100.0

  points_to_mesh_1.nodes["Grid to Mesh"].width  = 140.0
  points_to_mesh_1.nodes["Grid to Mesh"].height = 100.0

  points_to_mesh_1.nodes["Group.015"].width  = 115.2186279296875
  points_to_mesh_1.nodes["Group.015"].height = 100.0

  points_to_mesh_1.nodes["Group Output"].width  = 94.4310302734375
  points_to_mesh_1.nodes["Group Output"].height = 100.0

  points_to_mesh_1.nodes["Group Input"].width  = 80.0
  points_to_mesh_1.nodes["Group Input"].height = 100.0

  points_to_mesh_1.nodes["Switch"].width  = 107.59478759765625
  points_to_mesh_1.nodes["Switch"].height = 100.0

  points_to_mesh_1.nodes["Reroute"].width  = 20.0
  points_to_mesh_1.nodes["Reroute"].height = 100.0

  points_to_mesh_1.nodes["Reroute.001"].width  = 20.0
  points_to_mesh_1.nodes["Reroute.001"].height = 100.0

  points_to_mesh_1.nodes["Frame"].width  = 691.2186279296875
  points_to_mesh_1.nodes["Frame"].height = 233.0

  points_to_mesh_1.nodes["Group Input.001"].width  = 109.0357666015625
  points_to_mesh_1.nodes["Group Input.001"].height = 100.0

  points_to_mesh_1.nodes["Frame.001"].width  = 282.4310302734375
  points_to_mesh_1.nodes["Frame.001"].height = 141.0

  points_to_mesh_1.nodes["Group Input.002"].width  = 80.0
  points_to_mesh_1.nodes["Group Input.002"].height = 100.0

  points_to_mesh_1.nodes["Group Input.003"].width  = 139.300048828125
  points_to_mesh_1.nodes["Group Input.003"].height = 100.0

  points_to_mesh_1.nodes["Group Input.004"].width  = 137.20037841796875
  points_to_mesh_1.nodes["Group Input.004"].height = 100.0

  points_to_mesh_1.nodes["Frame.002"].width  = 851.7186279296875
  points_to_mesh_1.nodes["Frame.002"].height = 308.253173828125

  points_to_mesh_1.nodes["Group Input.005"].width  = 101.7724609375
  points_to_mesh_1.nodes["Group Input.005"].height = 100.0

  points_to_mesh_1.nodes["Subdivision Surface"].width  = 136.09149169921875
  points_to_mesh_1.nodes["Subdivision Surface"].height = 100.0

  points_to_mesh_1.nodes["Group Input.006"].width  = 125.031005859375
  points_to_mesh_1.nodes["Group Input.006"].height = 100.0

  points_to_mesh_1.nodes["Reroute.002"].width  = 20.0
  points_to_mesh_1.nodes["Reroute.002"].height = 100.0


  # Initialize points_to_mesh_1 links

  # group_input.Points -> convex_hull_006.Geometry
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input"].outputs[0],
    points_to_mesh_1.nodes["Convex Hull.006"].inputs[0]
  )
  # convex_hull_006.Convex Hull -> group_002.Mesh
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Convex Hull.006"].outputs[0],
    points_to_mesh_1.nodes["Group.002"].inputs[0]
  )
  # reroute_010.Output -> group_008.Points
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Reroute.010"].outputs[0],
    points_to_mesh_1.nodes["Group.008"].inputs[1]
  )
  # group_002.Mesh -> group_008.Mesh
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group.002"].outputs[0],
    points_to_mesh_1.nodes["Group.008"].inputs[0]
  )
  # group_input.Points -> reroute_005.Input
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input"].outputs[0],
    points_to_mesh_1.nodes["Reroute.005"].inputs[0]
  )
  # reroute_005.Output -> reroute_010.Input
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Reroute.005"].outputs[0],
    points_to_mesh_1.nodes["Reroute.010"].inputs[0]
  )
  # group_015.Geometry -> group_009.Geometry
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group.015"].outputs[0],
    points_to_mesh_1.nodes["Group.009"].inputs[0]
  )
  # group_009.Geometry -> mesh_to_sdf_grid.Mesh
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group.009"].outputs[0],
    points_to_mesh_1.nodes["Mesh to SDF Grid"].inputs[0]
  )
  # mesh_to_sdf_grid.SDF Grid -> grid_to_mesh.Grid
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Mesh to SDF Grid"].outputs[0],
    points_to_mesh_1.nodes["Grid to Mesh"].inputs[0]
  )
  # grid_to_mesh.Mesh -> group_013.Geometry
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Grid to Mesh"].outputs[0],
    points_to_mesh_1.nodes["Group.013"].inputs[0]
  )
  # subdivision_surface.Mesh -> group_015.Geometry
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Subdivision Surface"].outputs[0],
    points_to_mesh_1.nodes["Group.015"].inputs[0]
  )
  # reroute_002.Output -> group_015.Point Cloud
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Reroute.002"].outputs[0],
    points_to_mesh_1.nodes["Group.015"].inputs[1]
  )
  # switch.Output -> group_output.Mesh
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Switch"].outputs[0],
    points_to_mesh_1.nodes["Group Output"].inputs[0]
  )
  # group_013.Geometry -> switch.True
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group.013"].outputs[0],
    points_to_mesh_1.nodes["Switch"].inputs[2]
  )
  # reroute_001.Output -> switch.False
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Reroute.001"].outputs[0],
    points_to_mesh_1.nodes["Switch"].inputs[1]
  )
  # group_015.Geometry -> reroute.Input
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group.015"].outputs[0],
    points_to_mesh_1.nodes["Reroute"].inputs[0]
  )
  # reroute.Output -> reroute_001.Input
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Reroute"].outputs[0],
    points_to_mesh_1.nodes["Reroute.001"].inputs[0]
  )
  # group_input_001.SDF Simplify Enable -> switch.Switch
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input.001"].outputs[4],
    points_to_mesh_1.nodes["Switch"].inputs[0]
  )
  # group_input_002.Points -> group_013.Point Cloud
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input.002"].outputs[0],
    points_to_mesh_1.nodes["Group.013"].inputs[1]
  )
  # group_input.Points -> group_002.Points
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input"].outputs[0],
    points_to_mesh_1.nodes["Group.002"].inputs[1]
  )
  # group_input_003.Course Iterations -> group_002.Iterations
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input.003"].outputs[1],
    points_to_mesh_1.nodes["Group.002"].inputs[3]
  )
  # group_input_004.Fine Iterations -> group_008.Iterations
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input.004"].outputs[2],
    points_to_mesh_1.nodes["Group.008"].inputs[3]
  )
  # group_input_005.Voxel Size -> mesh_to_sdf_grid.Voxel Size
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input.005"].outputs[5],
    points_to_mesh_1.nodes["Mesh to SDF Grid"].inputs[1]
  )
  # group_008.Mesh -> subdivision_surface.Mesh
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group.008"].outputs[0],
    points_to_mesh_1.nodes["Subdivision Surface"].inputs[0]
  )
  # group_input_006.Subdivisions -> subdivision_surface.Level
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Group Input.006"].outputs[3],
    points_to_mesh_1.nodes["Subdivision Surface"].inputs[1]
  )
  # reroute_010.Output -> reroute_002.Input
  points_to_mesh_1.links.new(
    points_to_mesh_1.nodes["Reroute.010"].outputs[0],
    points_to_mesh_1.nodes["Reroute.002"].inputs[0]
  )

  return points_to_mesh_1


def get_points_to_shell_node_group():
  node_name = "Points to Shell"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]
  
  """Initialize Points to Shell node group"""
  points_to_shell_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  points_to_shell_1.color_tag = 'NONE'
  points_to_shell_1.description = ""
  points_to_shell_1.default_group_node_width = 140
  points_to_shell_1.show_modifier_manage_panel = True

  # points_to_shell_1 interface

  # Socket Mesh
  mesh_socket = points_to_shell_1.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')
  mesh_socket.attribute_domain = 'POINT'
  mesh_socket.default_input = 'VALUE'
  mesh_socket.structure_type = 'AUTO'

  # Socket Points
  points_socket = points_to_shell_1.interface.new_socket(name="Points", in_out='INPUT', socket_type='NodeSocketGeometry')
  points_socket.attribute_domain = 'POINT'
  points_socket.description = "Point cloud or mesh to merge points of"
  points_socket.default_input = 'VALUE'
  points_socket.structure_type = 'AUTO'

  # Socket Distance
  distance_socket = points_to_shell_1.interface.new_socket(name="Distance", in_out='INPUT', socket_type='NodeSocketFloat')
  distance_socket.default_value = 0.0010000000474974513
  distance_socket.min_value = 0.0
  distance_socket.max_value = 3.4028234663852886e+38
  distance_socket.subtype = 'DISTANCE'
  distance_socket.attribute_domain = 'POINT'
  distance_socket.default_input = 'VALUE'
  distance_socket.structure_type = 'AUTO'

  # Socket Normal Inset
  normal_inset_socket = points_to_shell_1.interface.new_socket(name="Normal Inset", in_out='INPUT', socket_type='NodeSocketFloat')
  normal_inset_socket.default_value = 0.0010000000474974513
  normal_inset_socket.min_value = -10000.0
  normal_inset_socket.max_value = 10000.0
  normal_inset_socket.subtype = 'NONE'
  normal_inset_socket.attribute_domain = 'POINT'
  normal_inset_socket.default_input = 'VALUE'
  normal_inset_socket.structure_type = 'AUTO'

  # Socket Smooth Iterations
  smooth_iterations_socket = points_to_shell_1.interface.new_socket(name="Smooth Iterations", in_out='INPUT', socket_type='NodeSocketInt')
  smooth_iterations_socket.default_value = 4
  smooth_iterations_socket.min_value = 0
  smooth_iterations_socket.max_value = 2147483647
  smooth_iterations_socket.subtype = 'NONE'
  smooth_iterations_socket.attribute_domain = 'POINT'
  smooth_iterations_socket.description = "How many times to blur the values for all elements"
  smooth_iterations_socket.default_input = 'VALUE'
  smooth_iterations_socket.structure_type = 'AUTO'

  # Initialize points_to_shell_1 nodes

  # Node Merge by Distance.006
  merge_by_distance_006 = points_to_shell_1.nodes.new("GeometryNodeMergeByDistance")
  merge_by_distance_006.name = "Merge by Distance.006"
  merge_by_distance_006.show_options = True
  merge_by_distance_006.inputs[1].hide = True
  merge_by_distance_006.inputs[2].hide = True
  # Selection
  merge_by_distance_006.inputs[1].default_value = True
  # Mode
  merge_by_distance_006.inputs[2].default_value = 'All'

  # Node Points to SDF Grid.003
  points_to_sdf_grid_003 = points_to_shell_1.nodes.new("GeometryNodePointsToSDFGrid")
  points_to_sdf_grid_003.name = "Points to SDF Grid.003"
  points_to_sdf_grid_003.show_options = True

  # Node Grid to Mesh.003
  grid_to_mesh_003 = points_to_shell_1.nodes.new("GeometryNodeGridToMesh")
  grid_to_mesh_003.name = "Grid to Mesh.003"
  grid_to_mesh_003.show_options = True
  # Threshold
  grid_to_mesh_003.inputs[1].default_value = 0.009999999776482582
  # Adaptivity
  grid_to_mesh_003.inputs[2].default_value = 0.0

  # Node Set Position.004
  set_position_004 = points_to_shell_1.nodes.new("GeometryNodeSetPosition")
  set_position_004.name = "Set Position.004"
  set_position_004.show_options = True
  set_position_004.inputs[1].hide = True
  set_position_004.inputs[2].hide = True
  # Selection
  set_position_004.inputs[1].default_value = True
  # Position
  set_position_004.inputs[2].default_value = (0.0, 0.0, 0.0)

  # Node Normal.001
  normal_001 = points_to_shell_1.nodes.new("GeometryNodeInputNormal")
  normal_001.name = "Normal.001"
  normal_001.hide = True
  normal_001.show_options = True
  normal_001.legacy_corner_normals = False
  normal_001.outputs[1].hide = True

  # Node Vector Math
  vector_math = points_to_shell_1.nodes.new("ShaderNodeVectorMath")
  vector_math.name = "Vector Math"
  vector_math.hide = True
  vector_math.show_options = True
  vector_math.operation = 'SCALE'

  # Node Group Output
  group_output = points_to_shell_1.nodes.new("NodeGroupOutput")
  group_output.label = "Mesh Out"
  group_output.name = "Group Output"
  group_output.hide = True
  group_output.show_options = True
  group_output.is_active_output = True
  group_output.inputs[1].hide = True

  # Node Group Input
  group_input = points_to_shell_1.nodes.new("NodeGroupInput")
  group_input.name = "Group Input"
  group_input.show_options = True
  group_input.outputs[2].hide = True
  group_input.outputs[3].hide = True
  group_input.outputs[4].hide = True

  # Node Math
  math = points_to_shell_1.nodes.new("ShaderNodeMath")
  math.label = "Multiply 2"
  math.name = "Math"
  math.hide = True
  math.show_options = True
  math.operation = 'MULTIPLY'
  math.use_clamp = False
  math.inputs[1].hide = True
  math.inputs[2].hide = True
  # Value_001
  math.inputs[1].default_value = 2.0

  # Node Math.001
  math_001 = points_to_shell_1.nodes.new("ShaderNodeMath")
  math_001.label = "Multiply -1"
  math_001.name = "Math.001"
  math_001.hide = True
  math_001.show_options = True
  math_001.operation = 'MULTIPLY'
  math_001.use_clamp = False
  math_001.inputs[1].hide = True
  math_001.inputs[2].hide = True
  # Value_001
  math_001.inputs[1].default_value = -1.0

  # Node Group Input.003
  group_input_003 = points_to_shell_1.nodes.new("NodeGroupInput")
  group_input_003.label = "Inset"
  group_input_003.name = "Group Input.003"
  group_input_003.hide = True
  group_input_003.show_options = True
  group_input_003.outputs[0].hide = True
  group_input_003.outputs[1].hide = True
  group_input_003.outputs[3].hide = True
  group_input_003.outputs[4].hide = True

  # Node Frame.001
  frame_001 = points_to_shell_1.nodes.new("NodeFrame")
  frame_001.label = "SDF Remesh"
  frame_001.name = "Frame.001"
  frame_001.show_options = True
  frame_001.label_size = 20
  frame_001.shrink = True

  # Node Reroute.002
  reroute_002 = points_to_shell_1.nodes.new("NodeReroute")
  reroute_002.name = "Reroute.002"
  reroute_002.show_options = True
  reroute_002.socket_idname = "NodeSocketGeometry"
  # Node Frame.002
  frame_002 = points_to_shell_1.nodes.new("NodeFrame")
  frame_002.label = "Inset By Normal"
  frame_002.name = "Frame.002"
  frame_002.show_options = True
  frame_002.label_size = 20
  frame_002.shrink = True

  # Node Group
  group = points_to_shell_1.nodes.new("GeometryNodeGroup")
  group.name = "Group"
  group.node_tree = get_smooth_geometry_node_group()
  group.inputs[1].hide = True
  group.inputs[3].hide = True
  # Socket_2
  group.inputs[1].default_value = True
  # Socket_4
  group.inputs[3].default_value = 1.0

  # Node Group Input.004
  group_input_004 = points_to_shell_1.nodes.new("NodeGroupInput")
  group_input_004.label = "Iterations"
  group_input_004.name = "Group Input.004"
  group_input_004.hide = True
  group_input_004.show_options = True
  group_input_004.outputs[0].hide = True
  group_input_004.outputs[1].hide = True
  group_input_004.outputs[2].hide = True
  group_input_004.outputs[4].hide = True

  # Node Frame.003
  frame_003 = points_to_shell_1.nodes.new("NodeFrame")
  frame_003.label = "Smooth"
  frame_003.name = "Frame.003"
  frame_003.show_options = True
  frame_003.label_size = 20
  frame_003.shrink = True

  # Set parents
  points_to_shell_1.nodes["Merge by Distance.006"].parent = points_to_shell_1.nodes["Frame.001"]
  points_to_shell_1.nodes["Points to SDF Grid.003"].parent = points_to_shell_1.nodes["Frame.001"]
  points_to_shell_1.nodes["Grid to Mesh.003"].parent = points_to_shell_1.nodes["Frame.001"]
  points_to_shell_1.nodes["Set Position.004"].parent = points_to_shell_1.nodes["Frame.002"]
  points_to_shell_1.nodes["Normal.001"].parent = points_to_shell_1.nodes["Frame.002"]
  points_to_shell_1.nodes["Vector Math"].parent = points_to_shell_1.nodes["Frame.002"]
  points_to_shell_1.nodes["Group Input"].parent = points_to_shell_1.nodes["Frame.001"]
  points_to_shell_1.nodes["Math"].parent = points_to_shell_1.nodes["Frame.001"]
  points_to_shell_1.nodes["Math.001"].parent = points_to_shell_1.nodes["Frame.002"]
  points_to_shell_1.nodes["Group Input.003"].parent = points_to_shell_1.nodes["Frame.002"]
  points_to_shell_1.nodes["Reroute.002"].parent = points_to_shell_1.nodes["Frame.002"]
  points_to_shell_1.nodes["Group"].parent = points_to_shell_1.nodes["Frame.003"]
  points_to_shell_1.nodes["Group Input.004"].parent = points_to_shell_1.nodes["Frame.003"]

  # Set locations
  points_to_shell_1.nodes["Merge by Distance.006"].location = (158.70578002929688, -40.089752197265625)
  points_to_shell_1.nodes["Points to SDF Grid.003"].location = (308.7701110839844, -36.35560607910156)
  points_to_shell_1.nodes["Grid to Mesh.003"].location = (459.95562744140625, -36.145233154296875)
  points_to_shell_1.nodes["Set Position.004"].location = (152.1474609375, -36.062477111816406)
  points_to_shell_1.nodes["Normal.001"].location = (29.95709228515625, -114.8822021484375)
  points_to_shell_1.nodes["Vector Math"].location = (150.509765625, -117.01966857910156)
  points_to_shell_1.nodes["Group Output"].location = (608.6287231445312, 84.60124969482422)
  points_to_shell_1.nodes["Group Input"].location = (29.80828857421875, -59.15202331542969)
  points_to_shell_1.nodes["Math"].location = (155.48001098632812, -122.97830200195312)
  points_to_shell_1.nodes["Math.001"].location = (149.79052734375, -152.05706787109375)
  points_to_shell_1.nodes["Group Input.003"].location = (29.79022216796875, -153.6973114013672)
  points_to_shell_1.nodes["Frame.001"].location = (-590.5, 146.0)
  points_to_shell_1.nodes["Reroute.002"].location = (38.81146240234375, -69.23861694335938)
  points_to_shell_1.nodes["Frame.002"].location = (295.5, 146.0)
  points_to_shell_1.nodes["Group"].location = (29.924468994140625, -35.75804138183594)
  points_to_shell_1.nodes["Group Input.004"].location = (30.42950439453125, -142.65399169921875)
  points_to_shell_1.nodes["Frame.003"].location = (79.0, 147.0)

  # Set dimensions
  points_to_shell_1.nodes["Merge by Distance.006"].width  = 125.42990112304688
  points_to_shell_1.nodes["Merge by Distance.006"].height = 100.0

  points_to_shell_1.nodes["Points to SDF Grid.003"].width  = 124.26422119140625
  points_to_shell_1.nodes["Points to SDF Grid.003"].height = 100.0

  points_to_shell_1.nodes["Grid to Mesh.003"].width  = 138.89007568359375
  points_to_shell_1.nodes["Grid to Mesh.003"].height = 100.0

  points_to_shell_1.nodes["Set Position.004"].width  = 100.0
  points_to_shell_1.nodes["Set Position.004"].height = 100.0

  points_to_shell_1.nodes["Normal.001"].width  = 100.0
  points_to_shell_1.nodes["Normal.001"].height = 100.0

  points_to_shell_1.nodes["Vector Math"].width  = 100.0
  points_to_shell_1.nodes["Vector Math"].height = 100.0

  points_to_shell_1.nodes["Group Output"].width  = 91.26104736328125
  points_to_shell_1.nodes["Group Output"].height = 100.0

  points_to_shell_1.nodes["Group Input"].width  = 95.1239013671875
  points_to_shell_1.nodes["Group Input"].height = 100.0

  points_to_shell_1.nodes["Math"].width  = 128.55752563476562
  points_to_shell_1.nodes["Math"].height = 100.0

  points_to_shell_1.nodes["Math.001"].width  = 100.0
  points_to_shell_1.nodes["Math.001"].height = 100.0

  points_to_shell_1.nodes["Group Input.003"].width  = 100.127685546875
  points_to_shell_1.nodes["Group Input.003"].height = 100.0

  points_to_shell_1.nodes["Frame.001"].width  = 628.8900756835938
  points_to_shell_1.nodes["Frame.001"].height = 185.5

  points_to_shell_1.nodes["Reroute.002"].width  = 20.0
  points_to_shell_1.nodes["Reroute.002"].height = 100.0

  points_to_shell_1.nodes["Frame.002"].width  = 282.0
  points_to_shell_1.nodes["Frame.002"].height = 207.5

  points_to_shell_1.nodes["Group"].width  = 128.59329223632812
  points_to_shell_1.nodes["Group"].height = 100.0

  points_to_shell_1.nodes["Group Input.004"].width  = 101.39273071289062
  points_to_shell_1.nodes["Group Input.004"].height = 100.0

  points_to_shell_1.nodes["Frame.003"].width  = 188.59329223632812
  points_to_shell_1.nodes["Frame.003"].height = 196.5


  # Initialize points_to_shell_1 links

  # merge_by_distance_006.Geometry -> points_to_sdf_grid_003.Points
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Merge by Distance.006"].outputs[0],
    points_to_shell_1.nodes["Points to SDF Grid.003"].inputs[0]
  )
  # points_to_sdf_grid_003.SDF Grid -> grid_to_mesh_003.Grid
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Points to SDF Grid.003"].outputs[0],
    points_to_shell_1.nodes["Grid to Mesh.003"].inputs[0]
  )
  # normal_001.Normal -> vector_math.Vector
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Normal.001"].outputs[0],
    points_to_shell_1.nodes["Vector Math"].inputs[0]
  )
  # vector_math.Vector -> set_position_004.Offset
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Vector Math"].outputs[0],
    points_to_shell_1.nodes["Set Position.004"].inputs[3]
  )
  # reroute_002.Output -> set_position_004.Geometry
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Reroute.002"].outputs[0],
    points_to_shell_1.nodes["Set Position.004"].inputs[0]
  )
  # set_position_004.Geometry -> group_output.Mesh
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Set Position.004"].outputs[0],
    points_to_shell_1.nodes["Group Output"].inputs[0]
  )
  # group_input.Points -> merge_by_distance_006.Geometry
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Group Input"].outputs[0],
    points_to_shell_1.nodes["Merge by Distance.006"].inputs[0]
  )
  # group_input.Distance -> merge_by_distance_006.Distance
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Group Input"].outputs[1],
    points_to_shell_1.nodes["Merge by Distance.006"].inputs[3]
  )
  # group_input.Distance -> math.Value
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Group Input"].outputs[1],
    points_to_shell_1.nodes["Math"].inputs[0]
  )
  # math.Value -> points_to_sdf_grid_003.Radius
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Math"].outputs[0],
    points_to_shell_1.nodes["Points to SDF Grid.003"].inputs[1]
  )
  # math.Value -> points_to_sdf_grid_003.Voxel Size
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Math"].outputs[0],
    points_to_shell_1.nodes["Points to SDF Grid.003"].inputs[2]
  )
  # math_001.Value -> vector_math.Scale
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Math.001"].outputs[0],
    points_to_shell_1.nodes["Vector Math"].inputs[3]
  )
  # group_input_003.Normal Inset -> math_001.Value
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Group Input.003"].outputs[2],
    points_to_shell_1.nodes["Math.001"].inputs[0]
  )
  # grid_to_mesh_003.Mesh -> group.Geometry
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Grid to Mesh.003"].outputs[0],
    points_to_shell_1.nodes["Group"].inputs[0]
  )
  # group_input_004.Smooth Iterations -> group.Iterations
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Group Input.004"].outputs[3],
    points_to_shell_1.nodes["Group"].inputs[2]
  )
  # group.Geometry -> reroute_002.Input
  points_to_shell_1.links.new(
    points_to_shell_1.nodes["Group"].outputs[0],
    points_to_shell_1.nodes["Reroute.002"].inputs[0]
  )

  return points_to_shell_1


def get_sdf_points_to_mesh_node_group():
  node_name = "SDF Points to Mesh"
  if node_name in bpy.data.node_groups:
    return bpy.data.node_groups[node_name]
  
  """Initialize SDF Points to Mesh node group"""
  sdf_points_to_mesh_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name=node_name)

  sdf_points_to_mesh_1.color_tag = 'NONE'
  sdf_points_to_mesh_1.description = ""
  sdf_points_to_mesh_1.default_group_node_width = 140
  sdf_points_to_mesh_1.is_modifier = True
  sdf_points_to_mesh_1.show_modifier_manage_panel = True

  # sdf_points_to_mesh_1 interface

  # Socket Geometry
  geometry_socket = sdf_points_to_mesh_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
  geometry_socket.attribute_domain = 'POINT'
  geometry_socket.default_input = 'VALUE'
  geometry_socket.structure_type = 'AUTO'

  # Socket Points
  points_socket = sdf_points_to_mesh_1.interface.new_socket(name="Points", in_out='INPUT', socket_type='NodeSocketGeometry')
  points_socket.attribute_domain = 'POINT'
  points_socket.default_input = 'VALUE'
  points_socket.structure_type = 'AUTO'

  # Panel Transform
  transform_panel = sdf_points_to_mesh_1.interface.new_panel("Transform")
  # Socket Orientation
  orientation_socket = sdf_points_to_mesh_1.interface.new_socket(name="Orientation", in_out='INPUT', socket_type='NodeSocketMenu', parent = transform_panel)
  orientation_socket.attribute_domain = 'POINT'
  orientation_socket.default_input = 'VALUE'
  orientation_socket.menu_expanded = True
  orientation_socket.structure_type = 'AUTO'
  orientation_socket.optional_label = True

  # Socket Scale
  scale_socket = sdf_points_to_mesh_1.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat', parent = transform_panel)
  scale_socket.default_value = 1.0
  scale_socket.min_value = -10000.0
  scale_socket.max_value = 10000.0
  scale_socket.subtype = 'NONE'
  scale_socket.attribute_domain = 'POINT'
  scale_socket.default_input = 'VALUE'
  scale_socket.structure_type = 'AUTO'

  # Socket Centered
  centered_socket = sdf_points_to_mesh_1.interface.new_socket(name="Centered", in_out='INPUT', socket_type='NodeSocketBool', parent = transform_panel)
  centered_socket.default_value = True
  centered_socket.attribute_domain = 'POINT'
  centered_socket.force_non_field = True
  centered_socket.default_input = 'VALUE'
  centered_socket.structure_type = 'SINGLE'


  # Panel Meshing
  meshing_panel = sdf_points_to_mesh_1.interface.new_panel("Meshing")
  # Socket Meshing Method
  meshing_method_socket = sdf_points_to_mesh_1.interface.new_socket(name="Meshing Method", in_out='INPUT', socket_type='NodeSocketMenu', parent = meshing_panel)
  meshing_method_socket.attribute_domain = 'POINT'
  meshing_method_socket.default_input = 'VALUE'
  meshing_method_socket.structure_type = 'AUTO'
  meshing_method_socket.optional_label = True

  # Socket Course Iterations
  course_iterations_socket = sdf_points_to_mesh_1.interface.new_socket(name="Course Iterations", in_out='INPUT', socket_type='NodeSocketInt', parent = meshing_panel)
  course_iterations_socket.default_value = 4
  course_iterations_socket.min_value = 0
  course_iterations_socket.max_value = 2147483647
  course_iterations_socket.subtype = 'NONE'
  course_iterations_socket.attribute_domain = 'POINT'
  course_iterations_socket.force_non_field = True
  course_iterations_socket.default_input = 'VALUE'
  course_iterations_socket.structure_type = 'SINGLE'

  # Socket Fine Iterations
  fine_iterations_socket = sdf_points_to_mesh_1.interface.new_socket(name="Fine Iterations", in_out='INPUT', socket_type='NodeSocketInt', parent = meshing_panel)
  fine_iterations_socket.default_value = 4
  fine_iterations_socket.min_value = 0
  fine_iterations_socket.max_value = 2147483647
  fine_iterations_socket.subtype = 'NONE'
  fine_iterations_socket.attribute_domain = 'POINT'
  fine_iterations_socket.force_non_field = True
  fine_iterations_socket.default_input = 'VALUE'
  fine_iterations_socket.structure_type = 'SINGLE'

  # Socket Subdivisions
  subdivisions_socket = sdf_points_to_mesh_1.interface.new_socket(name="Subdivisions", in_out='INPUT', socket_type='NodeSocketInt', parent = meshing_panel)
  subdivisions_socket.default_value = 0
  subdivisions_socket.min_value = 0
  subdivisions_socket.max_value = 6
  subdivisions_socket.subtype = 'NONE'
  subdivisions_socket.attribute_domain = 'POINT'
  subdivisions_socket.default_input = 'VALUE'
  subdivisions_socket.structure_type = 'AUTO'

  # Socket Smooth Iterations
  smooth_iterations_socket = sdf_points_to_mesh_1.interface.new_socket(name="Smooth Iterations", in_out='INPUT', socket_type='NodeSocketInt', parent = meshing_panel)
  smooth_iterations_socket.default_value = 1
  smooth_iterations_socket.min_value = 0
  smooth_iterations_socket.max_value = 2147483647
  smooth_iterations_socket.subtype = 'NONE'
  smooth_iterations_socket.attribute_domain = 'POINT'
  smooth_iterations_socket.description = "How many times to repeat the smoothing step"
  smooth_iterations_socket.default_input = 'VALUE'
  smooth_iterations_socket.structure_type = 'AUTO'

  # Socket Voxel Size
  voxel_size_socket = sdf_points_to_mesh_1.interface.new_socket(name="Voxel Size", in_out='INPUT', socket_type='NodeSocketFloat', parent = meshing_panel)
  voxel_size_socket.default_value = 0.009999999776482582
  voxel_size_socket.min_value = 0.009999999776482582
  voxel_size_socket.max_value = 3.4028234663852886e+38
  voxel_size_socket.subtype = 'DISTANCE'
  voxel_size_socket.attribute_domain = 'POINT'
  voxel_size_socket.default_input = 'VALUE'
  voxel_size_socket.structure_type = 'AUTO'

  # Socket Thickness
  thickness_socket = sdf_points_to_mesh_1.interface.new_socket(name="Thickness", in_out='INPUT', socket_type='NodeSocketFloat', parent = meshing_panel)
  thickness_socket.default_value = 0.0010000000474974513
  thickness_socket.min_value = -10000.0
  thickness_socket.max_value = 10000.0
  thickness_socket.subtype = 'NONE'
  thickness_socket.attribute_domain = 'POINT'
  thickness_socket.force_non_field = True
  thickness_socket.default_input = 'VALUE'
  thickness_socket.structure_type = 'SINGLE'

  # Socket Shade Smooth
  shade_smooth_socket = sdf_points_to_mesh_1.interface.new_socket(name="Shade Smooth", in_out='INPUT', socket_type='NodeSocketBool', parent = meshing_panel)
  shade_smooth_socket.default_value = True
  shade_smooth_socket.attribute_domain = 'POINT'
  shade_smooth_socket.force_non_field = True
  shade_smooth_socket.default_input = 'VALUE'
  shade_smooth_socket.structure_type = 'SINGLE'


  # Panel Material
  material_panel = sdf_points_to_mesh_1.interface.new_panel("Material")
  # Socket Material
  material_socket = sdf_points_to_mesh_1.interface.new_socket(name="Material", in_out='INPUT', socket_type='NodeSocketMaterial', parent = material_panel)
  material_socket.attribute_domain = 'POINT'
  material_socket.default_input = 'VALUE'
  material_socket.structure_type = 'AUTO'
  material_socket.optional_label = True

  # Socket Color Attribute
  color_attribute_socket = sdf_points_to_mesh_1.interface.new_socket(name="Color Attribute", in_out='INPUT', socket_type='NodeSocketString', parent = material_panel)
  color_attribute_socket.default_value = "Color"
  color_attribute_socket.subtype = 'NONE'
  color_attribute_socket.attribute_domain = 'POINT'
  color_attribute_socket.default_input = 'VALUE'
  color_attribute_socket.structure_type = 'AUTO'
  color_attribute_socket.optional_label = True

  # Socket Metallic Attribute
  metallic_attribute_socket = sdf_points_to_mesh_1.interface.new_socket(name="Metallic Attribute", in_out='INPUT', socket_type='NodeSocketString', parent = material_panel)
  metallic_attribute_socket.default_value = "Metallic"
  metallic_attribute_socket.subtype = 'NONE'
  metallic_attribute_socket.attribute_domain = 'POINT'
  metallic_attribute_socket.default_input = 'VALUE'
  metallic_attribute_socket.structure_type = 'AUTO'
  metallic_attribute_socket.optional_label = True

  # Socket Roughness Attribute
  roughness_attribute_socket = sdf_points_to_mesh_1.interface.new_socket(name="Roughness Attribute", in_out='INPUT', socket_type='NodeSocketString', parent = material_panel)
  roughness_attribute_socket.default_value = "Roughness"
  roughness_attribute_socket.subtype = 'NONE'
  roughness_attribute_socket.attribute_domain = 'POINT'
  roughness_attribute_socket.default_input = 'VALUE'
  roughness_attribute_socket.structure_type = 'AUTO'
  roughness_attribute_socket.optional_label = True

  # Socket Opacity Attribute
  opacity_attribute_socket = sdf_points_to_mesh_1.interface.new_socket(name="Opacity Attribute", in_out='INPUT', socket_type='NodeSocketString', parent = material_panel)
  opacity_attribute_socket.default_value = "Opacity"
  opacity_attribute_socket.subtype = 'NONE'
  opacity_attribute_socket.attribute_domain = 'POINT'
  opacity_attribute_socket.default_input = 'VALUE'
  opacity_attribute_socket.structure_type = 'AUTO'
  opacity_attribute_socket.optional_label = True


  # Panel Point Attributes
  point_attributes_panel = sdf_points_to_mesh_1.interface.new_panel("Point Attributes")
  # Socket Color
  color_socket = sdf_points_to_mesh_1.interface.new_socket(name="Color", in_out='INPUT', socket_type='NodeSocketString', parent = point_attributes_panel)
  color_socket.default_value = "Color"
  color_socket.subtype = 'NONE'
  color_socket.attribute_domain = 'POINT'
  color_socket.default_input = 'VALUE'
  color_socket.structure_type = 'AUTO'
  color_socket.optional_label = True

  # Socket Metallic
  metallic_socket = sdf_points_to_mesh_1.interface.new_socket(name="Metallic", in_out='INPUT', socket_type='NodeSocketString', parent = point_attributes_panel)
  metallic_socket.default_value = "Metallic"
  metallic_socket.subtype = 'NONE'
  metallic_socket.attribute_domain = 'POINT'
  metallic_socket.default_input = 'VALUE'
  metallic_socket.structure_type = 'AUTO'
  metallic_socket.optional_label = True

  # Socket Roughness
  roughness_socket = sdf_points_to_mesh_1.interface.new_socket(name="Roughness", in_out='INPUT', socket_type='NodeSocketString', parent = point_attributes_panel)
  roughness_socket.default_value = "Roughness"
  roughness_socket.subtype = 'NONE'
  roughness_socket.attribute_domain = 'POINT'
  roughness_socket.default_input = 'VALUE'
  roughness_socket.structure_type = 'AUTO'
  roughness_socket.optional_label = True

  # Socket Opacity
  opacity_socket = sdf_points_to_mesh_1.interface.new_socket(name="Opacity", in_out='INPUT', socket_type='NodeSocketString', parent = point_attributes_panel)
  opacity_socket.default_value = "Opacity"
  opacity_socket.subtype = 'NONE'
  opacity_socket.attribute_domain = 'POINT'
  opacity_socket.default_input = 'VALUE'
  opacity_socket.structure_type = 'AUTO'
  opacity_socket.optional_label = True


  # Initialize sdf_points_to_mesh_1 nodes

  # Node Group Output
  group_output = sdf_points_to_mesh_1.nodes.new("NodeGroupOutput")
  group_output.label = "Geometry Out"
  group_output.name = "Group Output"
  group_output.hide = True
  group_output.show_options = True
  group_output.is_active_output = True
  group_output.inputs[1].hide = True

  # Node Set Shade Smooth.004
  set_shade_smooth_004 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSetShadeSmooth")
  set_shade_smooth_004.name = "Set Shade Smooth.004"
  set_shade_smooth_004.hide = True
  set_shade_smooth_004.show_options = True
  set_shade_smooth_004.domain = 'FACE'
  set_shade_smooth_004.inputs[1].hide = True
  # Selection
  set_shade_smooth_004.inputs[1].default_value = True

  # Node Group.012
  group_012 = sdf_points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_012.name = "Group.012"
  group_012.show_options = True
  group_012.node_tree = get_smooth_geometry_node_group()
  group_012.inputs[1].hide = True
  group_012.inputs[3].hide = True
  # Socket_2
  group_012.inputs[1].default_value = True
  # Socket_4
  group_012.inputs[3].default_value = 1.0

  # Node Group.016
  group_016 = sdf_points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_016.name = "Group.016"
  group_016.show_options = True
  group_016.node_tree = get_points_to_mesh_node_group()
  group_016.inputs[4].hide = True
  group_016.inputs[5].hide = True
  # Socket_6
  group_016.inputs[4].default_value = False
  # Socket_7
  group_016.inputs[5].default_value = 0.009999999776482582

  # Node SDF_Remesh.001
  sdf_remesh_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeGroup")
  sdf_remesh_001.name = "SDF_Remesh.001"
  sdf_remesh_001.show_options = True
  sdf_remesh_001.node_tree = get_points_to_shell_node_group()
  # Socket_2
  sdf_remesh_001.inputs[1].default_value = 0.0010000000474974513
  # Socket_4
  sdf_remesh_001.inputs[3].default_value = 4

  # Node Named Attribute.001
  named_attribute_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeInputNamedAttribute")
  named_attribute_001.name = "Named Attribute.001"
  named_attribute_001.hide = True
  named_attribute_001.show_options = True
  named_attribute_001.data_type = 'FLOAT_COLOR'

  # Node Store Named Attribute.001
  store_named_attribute_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeStoreNamedAttribute")
  store_named_attribute_001.name = "Store Named Attribute.001"
  store_named_attribute_001.hide = True
  store_named_attribute_001.show_options = True
  store_named_attribute_001.data_type = 'FLOAT_COLOR'
  store_named_attribute_001.domain = 'POINT'
  store_named_attribute_001.inputs[1].hide = True
  # Selection
  store_named_attribute_001.inputs[1].default_value = True

  # Node Set Material.001
  set_material_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSetMaterial")
  set_material_001.name = "Set Material.001"
  set_material_001.hide = True
  set_material_001.show_options = True
  set_material_001.inputs[1].hide = True
  # Selection
  set_material_001.inputs[1].default_value = True

  # Node Sample Nearest.001
  sample_nearest_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSampleNearest")
  sample_nearest_001.name = "Sample Nearest.001"
  sample_nearest_001.hide = True
  sample_nearest_001.show_options = True
  sample_nearest_001.domain = 'POINT'

  # Node Position.005
  position_005 = sdf_points_to_mesh_1.nodes.new("GeometryNodeInputPosition")
  position_005.name = "Position.005"
  position_005.hide = True
  position_005.show_options = True

  # Node Sample Index.001
  sample_index_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSampleIndex")
  sample_index_001.name = "Sample Index.001"
  sample_index_001.hide = True
  sample_index_001.show_options = True
  sample_index_001.clamp = False
  sample_index_001.data_type = 'FLOAT_COLOR'
  sample_index_001.domain = 'POINT'

  # Node Group Input.003
  group_input_003 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_003.label = "Points"
  group_input_003.name = "Group Input.003"
  group_input_003.hide = True
  group_input_003.show_options = True
  group_input_003.outputs[1].hide = True
  group_input_003.outputs[2].hide = True
  group_input_003.outputs[3].hide = True
  group_input_003.outputs[4].hide = True
  group_input_003.outputs[5].hide = True
  group_input_003.outputs[6].hide = True
  group_input_003.outputs[7].hide = True
  group_input_003.outputs[8].hide = True
  group_input_003.outputs[9].hide = True
  group_input_003.outputs[10].hide = True
  group_input_003.outputs[11].hide = True
  group_input_003.outputs[12].hide = True
  group_input_003.outputs[13].hide = True
  group_input_003.outputs[14].hide = True
  group_input_003.outputs[15].hide = True
  group_input_003.outputs[16].hide = True
  group_input_003.outputs[17].hide = True
  group_input_003.outputs[18].hide = True
  group_input_003.outputs[19].hide = True
  group_input_003.outputs[20].hide = True
  group_input_003.outputs[21].hide = True

  # Node Group Input
  group_input = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input.label = "Material"
  group_input.name = "Group Input"
  group_input.hide = True
  group_input.show_options = True
  group_input.outputs[0].hide = True
  group_input.outputs[1].hide = True
  group_input.outputs[2].hide = True
  group_input.outputs[3].hide = True
  group_input.outputs[4].hide = True
  group_input.outputs[5].hide = True
  group_input.outputs[6].hide = True
  group_input.outputs[7].hide = True
  group_input.outputs[8].hide = True
  group_input.outputs[9].hide = True
  group_input.outputs[10].hide = True
  group_input.outputs[11].hide = True
  group_input.outputs[13].hide = True
  group_input.outputs[14].hide = True
  group_input.outputs[15].hide = True
  group_input.outputs[16].hide = True
  group_input.outputs[17].hide = True
  group_input.outputs[18].hide = True
  group_input.outputs[19].hide = True
  group_input.outputs[20].hide = True
  group_input.outputs[21].hide = True

  # Node Group Input.002
  group_input_002 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_002.label = "Color Attribute"
  group_input_002.name = "Group Input.002"
  group_input_002.hide = True
  group_input_002.show_options = True
  group_input_002.outputs[0].hide = True
  group_input_002.outputs[1].hide = True
  group_input_002.outputs[2].hide = True
  group_input_002.outputs[3].hide = True
  group_input_002.outputs[4].hide = True
  group_input_002.outputs[5].hide = True
  group_input_002.outputs[6].hide = True
  group_input_002.outputs[7].hide = True
  group_input_002.outputs[8].hide = True
  group_input_002.outputs[9].hide = True
  group_input_002.outputs[10].hide = True
  group_input_002.outputs[11].hide = True
  group_input_002.outputs[12].hide = True
  group_input_002.outputs[14].hide = True
  group_input_002.outputs[15].hide = True
  group_input_002.outputs[16].hide = True
  group_input_002.outputs[17].hide = True
  group_input_002.outputs[18].hide = True
  group_input_002.outputs[19].hide = True
  group_input_002.outputs[20].hide = True
  group_input_002.outputs[21].hide = True

  # Node Group Input.004
  group_input_004 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_004.label = "Color"
  group_input_004.name = "Group Input.004"
  group_input_004.hide = True
  group_input_004.show_options = True
  group_input_004.outputs[0].hide = True
  group_input_004.outputs[1].hide = True
  group_input_004.outputs[2].hide = True
  group_input_004.outputs[3].hide = True
  group_input_004.outputs[4].hide = True
  group_input_004.outputs[5].hide = True
  group_input_004.outputs[6].hide = True
  group_input_004.outputs[7].hide = True
  group_input_004.outputs[8].hide = True
  group_input_004.outputs[9].hide = True
  group_input_004.outputs[10].hide = True
  group_input_004.outputs[11].hide = True
  group_input_004.outputs[12].hide = True
  group_input_004.outputs[13].hide = True
  group_input_004.outputs[14].hide = True
  group_input_004.outputs[15].hide = True
  group_input_004.outputs[16].hide = True
  group_input_004.outputs[18].hide = True
  group_input_004.outputs[19].hide = True
  group_input_004.outputs[20].hide = True
  group_input_004.outputs[21].hide = True

  # Node Frame
  frame = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame.label = "Set Material with Point Attributes"
  frame.name = "Frame"
  frame.show_options = True
  frame.label_size = 20
  frame.shrink = True

  # Node Group Input.005
  group_input_005 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_005.label = "Dense Shell"
  group_input_005.name = "Group Input.005"
  group_input_005.show_options = True
  group_input_005.outputs[1].hide = True
  group_input_005.outputs[2].hide = True
  group_input_005.outputs[3].hide = True
  group_input_005.outputs[4].hide = True
  group_input_005.outputs[5].hide = True
  group_input_005.outputs[6].hide = True
  group_input_005.outputs[7].hide = True
  group_input_005.outputs[8].hide = True
  group_input_005.outputs[9].hide = True
  group_input_005.outputs[11].hide = True
  group_input_005.outputs[12].hide = True
  group_input_005.outputs[13].hide = True
  group_input_005.outputs[14].hide = True
  group_input_005.outputs[15].hide = True
  group_input_005.outputs[16].hide = True
  group_input_005.outputs[17].hide = True
  group_input_005.outputs[18].hide = True
  group_input_005.outputs[19].hide = True
  group_input_005.outputs[20].hide = True
  group_input_005.outputs[21].hide = True

  # Node Menu Switch
  menu_switch = sdf_points_to_mesh_1.nodes.new("GeometryNodeMenuSwitch")
  menu_switch.name = "Menu Switch"
  menu_switch.show_options = True
  menu_switch.active_index = 2
  menu_switch.data_type = 'GEOMETRY'
  menu_switch.enum_items.clear()
  menu_switch.enum_items.new("Dense Shell")
  menu_switch.enum_items[0].description = ""
  menu_switch.enum_items.new("Dense SDF")
  menu_switch.enum_items[1].description = ""
  menu_switch.enum_items.new("Reduced SDF")
  menu_switch.enum_items[2].description = ""
  menu_switch.inputs[4].hide = True
  menu_switch.outputs[1].hide = True
  menu_switch.outputs[2].hide = True
  menu_switch.outputs[3].hide = True

  # Node Group Input.006
  group_input_006 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_006.label = "Method"
  group_input_006.name = "Group Input.006"
  group_input_006.hide = True
  group_input_006.show_options = True
  group_input_006.outputs[0].hide = True
  group_input_006.outputs[1].hide = True
  group_input_006.outputs[2].hide = True
  group_input_006.outputs[3].hide = True
  group_input_006.outputs[5].hide = True
  group_input_006.outputs[6].hide = True
  group_input_006.outputs[7].hide = True
  group_input_006.outputs[8].hide = True
  group_input_006.outputs[9].hide = True
  group_input_006.outputs[10].hide = True
  group_input_006.outputs[11].hide = True
  group_input_006.outputs[12].hide = True
  group_input_006.outputs[13].hide = True
  group_input_006.outputs[14].hide = True
  group_input_006.outputs[15].hide = True
  group_input_006.outputs[16].hide = True
  group_input_006.outputs[17].hide = True
  group_input_006.outputs[18].hide = True
  group_input_006.outputs[19].hide = True
  group_input_006.outputs[20].hide = True
  group_input_006.outputs[21].hide = True

  # Node Group Input.007
  group_input_007 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_007.label = "SDF Iterations"
  group_input_007.name = "Group Input.007"
  group_input_007.show_options = True
  group_input_007.outputs[1].hide = True
  group_input_007.outputs[2].hide = True
  group_input_007.outputs[3].hide = True
  group_input_007.outputs[4].hide = True
  group_input_007.outputs[8].hide = True
  group_input_007.outputs[9].hide = True
  group_input_007.outputs[10].hide = True
  group_input_007.outputs[11].hide = True
  group_input_007.outputs[12].hide = True
  group_input_007.outputs[13].hide = True
  group_input_007.outputs[14].hide = True
  group_input_007.outputs[15].hide = True
  group_input_007.outputs[16].hide = True
  group_input_007.outputs[17].hide = True
  group_input_007.outputs[18].hide = True
  group_input_007.outputs[19].hide = True
  group_input_007.outputs[20].hide = True
  group_input_007.outputs[21].hide = True

  # Node Group Input.008
  group_input_008 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_008.label = "Smooth Iterations"
  group_input_008.name = "Group Input.008"
  group_input_008.hide = True
  group_input_008.show_options = True
  group_input_008.outputs[0].hide = True
  group_input_008.outputs[1].hide = True
  group_input_008.outputs[2].hide = True
  group_input_008.outputs[3].hide = True
  group_input_008.outputs[4].hide = True
  group_input_008.outputs[5].hide = True
  group_input_008.outputs[6].hide = True
  group_input_008.outputs[7].hide = True
  group_input_008.outputs[9].hide = True
  group_input_008.outputs[10].hide = True
  group_input_008.outputs[11].hide = True
  group_input_008.outputs[12].hide = True
  group_input_008.outputs[13].hide = True
  group_input_008.outputs[14].hide = True
  group_input_008.outputs[15].hide = True
  group_input_008.outputs[16].hide = True
  group_input_008.outputs[17].hide = True
  group_input_008.outputs[18].hide = True
  group_input_008.outputs[19].hide = True
  group_input_008.outputs[20].hide = True
  group_input_008.outputs[21].hide = True

  # Node Group.013
  group_013 = sdf_points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_013.name = "Group.013"
  group_013.show_options = True
  group_013.node_tree = get_smooth_geometry_node_group()
  group_013.inputs[1].hide = True
  group_013.inputs[3].hide = True
  # Socket_2
  group_013.inputs[1].default_value = True
  # Socket_4
  group_013.inputs[3].default_value = 1.0

  # Node Group.017
  group_017 = sdf_points_to_mesh_1.nodes.new("GeometryNodeGroup")
  group_017.name = "Group.017"
  group_017.show_options = True
  group_017.node_tree = get_points_to_mesh_node_group()
  group_017.inputs[3].hide = True
  group_017.inputs[4].hide = True
  # Socket_8
  group_017.inputs[3].default_value = 0
  # Socket_6
  group_017.inputs[4].default_value = True

  # Node Group Input.010
  group_input_010 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_010.label = "SDF Iterations"
  group_input_010.name = "Group Input.010"
  group_input_010.show_options = True
  group_input_010.outputs[1].hide = True
  group_input_010.outputs[2].hide = True
  group_input_010.outputs[3].hide = True
  group_input_010.outputs[4].hide = True
  group_input_010.outputs[7].hide = True
  group_input_010.outputs[8].hide = True
  group_input_010.outputs[10].hide = True
  group_input_010.outputs[11].hide = True
  group_input_010.outputs[12].hide = True
  group_input_010.outputs[13].hide = True
  group_input_010.outputs[14].hide = True
  group_input_010.outputs[15].hide = True
  group_input_010.outputs[16].hide = True
  group_input_010.outputs[17].hide = True
  group_input_010.outputs[18].hide = True
  group_input_010.outputs[19].hide = True
  group_input_010.outputs[20].hide = True
  group_input_010.outputs[21].hide = True

  # Node Group Input.011
  group_input_011 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_011.label = "Smooth Iterations"
  group_input_011.name = "Group Input.011"
  group_input_011.hide = True
  group_input_011.show_options = True
  group_input_011.outputs[0].hide = True
  group_input_011.outputs[1].hide = True
  group_input_011.outputs[2].hide = True
  group_input_011.outputs[3].hide = True
  group_input_011.outputs[4].hide = True
  group_input_011.outputs[5].hide = True
  group_input_011.outputs[6].hide = True
  group_input_011.outputs[7].hide = True
  group_input_011.outputs[9].hide = True
  group_input_011.outputs[10].hide = True
  group_input_011.outputs[11].hide = True
  group_input_011.outputs[12].hide = True
  group_input_011.outputs[13].hide = True
  group_input_011.outputs[14].hide = True
  group_input_011.outputs[15].hide = True
  group_input_011.outputs[16].hide = True
  group_input_011.outputs[17].hide = True
  group_input_011.outputs[18].hide = True
  group_input_011.outputs[19].hide = True
  group_input_011.outputs[20].hide = True
  group_input_011.outputs[21].hide = True

  # Node Group Input.001
  group_input_001 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_001.label = "Shade Smooth"
  group_input_001.name = "Group Input.001"
  group_input_001.hide = True
  group_input_001.show_options = True
  group_input_001.outputs[0].hide = True
  group_input_001.outputs[1].hide = True
  group_input_001.outputs[2].hide = True
  group_input_001.outputs[3].hide = True
  group_input_001.outputs[4].hide = True
  group_input_001.outputs[5].hide = True
  group_input_001.outputs[6].hide = True
  group_input_001.outputs[7].hide = True
  group_input_001.outputs[8].hide = True
  group_input_001.outputs[9].hide = True
  group_input_001.outputs[10].hide = True
  group_input_001.outputs[12].hide = True
  group_input_001.outputs[13].hide = True
  group_input_001.outputs[14].hide = True
  group_input_001.outputs[15].hide = True
  group_input_001.outputs[16].hide = True
  group_input_001.outputs[17].hide = True
  group_input_001.outputs[18].hide = True
  group_input_001.outputs[19].hide = True
  group_input_001.outputs[20].hide = True
  group_input_001.outputs[21].hide = True

  # Node Frame.001
  frame_001 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_001.label = "Shade Smooth"
  frame_001.name = "Frame.001"
  frame_001.show_options = True
  frame_001.label_size = 20
  frame_001.shrink = True

  # Node Reroute
  reroute = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute.name = "Reroute"
  reroute.show_options = True
  reroute.socket_idname = "NodeSocketGeometry"
  # Node Frame.002
  frame_002 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_002.label = "Select Method"
  frame_002.name = "Frame.002"
  frame_002.show_options = True
  frame_002.label_size = 20
  frame_002.shrink = True

  # Node Frame.003
  frame_003 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_003.label = "Dense Shell"
  frame_003.name = "Frame.003"
  frame_003.show_options = True
  frame_003.label_size = 20
  frame_003.shrink = True

  # Node Frame.004
  frame_004 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_004.label = "Dense SDF"
  frame_004.name = "Frame.004"
  frame_004.show_options = True
  frame_004.label_size = 20
  frame_004.shrink = True

  # Node Frame.005
  frame_005 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_005.label = "Reduced SDF"
  frame_005.name = "Frame.005"
  frame_005.show_options = True
  frame_005.label_size = 20
  frame_005.shrink = True

  # Node Bounding Box
  bounding_box = sdf_points_to_mesh_1.nodes.new("GeometryNodeBoundBox")
  bounding_box.name = "Bounding Box"
  bounding_box.hide = True
  bounding_box.show_options = True
  bounding_box.inputs[1].hide = True
  bounding_box.outputs[0].hide = True
  bounding_box.outputs[2].hide = True
  # Use Radius
  bounding_box.inputs[1].default_value = True

  # Node Reroute.001
  reroute_001 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_001.name = "Reroute.001"
  reroute_001.show_options = True
  reroute_001.socket_idname = "NodeSocketGeometry"
  # Node Transform Geometry
  transform_geometry = sdf_points_to_mesh_1.nodes.new("GeometryNodeTransform")
  transform_geometry.name = "Transform Geometry"
  transform_geometry.hide = True
  transform_geometry.show_options = True
  transform_geometry.inputs[1].hide = True
  transform_geometry.inputs[3].hide = True
  transform_geometry.inputs[4].hide = True
  transform_geometry.inputs[5].hide = True
  # Mode
  transform_geometry.inputs[1].default_value = 'Components'
  # Rotation
  transform_geometry.inputs[3].default_value = (0.0, 0.0, 0.0)
  # Scale
  transform_geometry.inputs[4].default_value = (1.0, 1.0, 1.0)

  # Node Vector Math
  vector_math = sdf_points_to_mesh_1.nodes.new("ShaderNodeVectorMath")
  vector_math.label = "Multiply -Z"
  vector_math.name = "Vector Math"
  vector_math.hide = True
  vector_math.show_options = True
  vector_math.operation = 'MULTIPLY'
  vector_math.inputs[1].hide = True
  vector_math.inputs[2].hide = True
  vector_math.inputs[3].hide = True
  vector_math.outputs[1].hide = True
  # Vector_001
  vector_math.inputs[1].default_value = (0.0, 0.0, -1.0)

  # Node Switch
  switch = sdf_points_to_mesh_1.nodes.new("GeometryNodeSwitch")
  switch.name = "Switch"
  switch.hide = True
  switch.show_options = True
  switch.input_type = 'GEOMETRY'

  # Node Group Input.009
  group_input_009 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_009.label = "Centered"
  group_input_009.name = "Group Input.009"
  group_input_009.hide = True
  group_input_009.show_options = True
  group_input_009.outputs[0].hide = True
  group_input_009.outputs[1].hide = True
  group_input_009.outputs[2].hide = True
  group_input_009.outputs[4].hide = True
  group_input_009.outputs[5].hide = True
  group_input_009.outputs[6].hide = True
  group_input_009.outputs[7].hide = True
  group_input_009.outputs[8].hide = True
  group_input_009.outputs[9].hide = True
  group_input_009.outputs[10].hide = True
  group_input_009.outputs[11].hide = True
  group_input_009.outputs[12].hide = True
  group_input_009.outputs[13].hide = True
  group_input_009.outputs[14].hide = True
  group_input_009.outputs[15].hide = True
  group_input_009.outputs[16].hide = True
  group_input_009.outputs[17].hide = True
  group_input_009.outputs[18].hide = True
  group_input_009.outputs[19].hide = True
  group_input_009.outputs[20].hide = True
  group_input_009.outputs[21].hide = True

  # Node Reroute.002
  reroute_002 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_002.name = "Reroute.002"
  reroute_002.show_options = True
  reroute_002.socket_idname = "NodeSocketGeometry"
  # Node Frame.006
  frame_006 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_006.label = "Center"
  frame_006.name = "Frame.006"
  frame_006.show_options = True
  frame_006.label_size = 20
  frame_006.shrink = True

  # Node Transform Geometry.001
  transform_geometry_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeTransform")
  transform_geometry_001.name = "Transform Geometry.001"
  transform_geometry_001.show_options = True
  transform_geometry_001.inputs[1].hide = True
  transform_geometry_001.inputs[2].hide = True
  transform_geometry_001.inputs[5].hide = True
  # Mode
  transform_geometry_001.inputs[1].default_value = 'Components'
  # Translation
  transform_geometry_001.inputs[2].default_value = (0.0, 0.0, 0.0)

  # Node Group Input.012
  group_input_012 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_012.label = "Scale"
  group_input_012.name = "Group Input.012"
  group_input_012.hide = True
  group_input_012.show_options = True
  group_input_012.outputs[0].hide = True
  group_input_012.outputs[1].hide = True
  group_input_012.outputs[3].hide = True
  group_input_012.outputs[4].hide = True
  group_input_012.outputs[5].hide = True
  group_input_012.outputs[6].hide = True
  group_input_012.outputs[7].hide = True
  group_input_012.outputs[8].hide = True
  group_input_012.outputs[9].hide = True
  group_input_012.outputs[10].hide = True
  group_input_012.outputs[11].hide = True
  group_input_012.outputs[12].hide = True
  group_input_012.outputs[13].hide = True
  group_input_012.outputs[14].hide = True
  group_input_012.outputs[15].hide = True
  group_input_012.outputs[16].hide = True
  group_input_012.outputs[17].hide = True
  group_input_012.outputs[18].hide = True
  group_input_012.outputs[19].hide = True
  group_input_012.outputs[20].hide = True
  group_input_012.outputs[21].hide = True

  # Node Frame.007
  frame_007 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_007.label = "Scale Rotate"
  frame_007.name = "Frame.007"
  frame_007.show_options = True
  frame_007.label_size = 20
  frame_007.shrink = True

  # Node Menu Switch.001
  menu_switch_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeMenuSwitch")
  menu_switch_001.name = "Menu Switch.001"
  menu_switch_001.hide = True
  menu_switch_001.show_options = True
  menu_switch_001.active_index = 3
  menu_switch_001.data_type = 'FLOAT'
  menu_switch_001.enum_items.clear()
  menu_switch_001.enum_items.new("Front")
  menu_switch_001.enum_items[0].description = ""
  menu_switch_001.enum_items.new("Left")
  menu_switch_001.enum_items[1].description = ""
  menu_switch_001.enum_items.new("Right")
  menu_switch_001.enum_items[2].description = ""
  menu_switch_001.enum_items.new("Back")
  menu_switch_001.enum_items[3].description = ""
  menu_switch_001.inputs[1].hide = True
  menu_switch_001.inputs[2].hide = True
  menu_switch_001.inputs[3].hide = True
  menu_switch_001.inputs[4].hide = True
  menu_switch_001.inputs[5].hide = True
  menu_switch_001.outputs[1].hide = True
  menu_switch_001.outputs[2].hide = True
  menu_switch_001.outputs[3].hide = True
  menu_switch_001.outputs[4].hide = True
  # Item_2
  menu_switch_001.inputs[1].default_value = 0.0
  # Item_3
  menu_switch_001.inputs[2].default_value = 1.5707963705062866
  # Item_4
  menu_switch_001.inputs[3].default_value = -1.5707963705062866
  # Item_5
  menu_switch_001.inputs[4].default_value = 3.1415927410125732

  # Node Group Input.013
  group_input_013 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_013.label = "Orientation"
  group_input_013.name = "Group Input.013"
  group_input_013.hide = True
  group_input_013.show_options = True
  group_input_013.outputs[0].hide = True
  group_input_013.outputs[2].hide = True
  group_input_013.outputs[3].hide = True
  group_input_013.outputs[4].hide = True
  group_input_013.outputs[5].hide = True
  group_input_013.outputs[6].hide = True
  group_input_013.outputs[7].hide = True
  group_input_013.outputs[8].hide = True
  group_input_013.outputs[9].hide = True
  group_input_013.outputs[10].hide = True
  group_input_013.outputs[11].hide = True
  group_input_013.outputs[12].hide = True
  group_input_013.outputs[13].hide = True
  group_input_013.outputs[14].hide = True
  group_input_013.outputs[15].hide = True
  group_input_013.outputs[16].hide = True
  group_input_013.outputs[17].hide = True
  group_input_013.outputs[18].hide = True
  group_input_013.outputs[19].hide = True
  group_input_013.outputs[20].hide = True
  group_input_013.outputs[21].hide = True

  # Node Euler to Rotation
  euler_to_rotation = sdf_points_to_mesh_1.nodes.new("FunctionNodeEulerToRotation")
  euler_to_rotation.name = "Euler to Rotation"
  euler_to_rotation.hide = True
  euler_to_rotation.show_options = True

  # Node Combine XYZ
  combine_xyz = sdf_points_to_mesh_1.nodes.new("ShaderNodeCombineXYZ")
  combine_xyz.label = "Combine Z"
  combine_xyz.name = "Combine XYZ"
  combine_xyz.hide = True
  combine_xyz.show_options = True
  combine_xyz.inputs[0].hide = True
  combine_xyz.inputs[1].hide = True
  # X
  combine_xyz.inputs[0].default_value = 0.0
  # Y
  combine_xyz.inputs[1].default_value = 0.0

  # Node Reroute.003
  reroute_003 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_003.name = "Reroute.003"
  reroute_003.show_options = True
  reroute_003.socket_idname = "NodeSocketGeometry"
  # Node Frame.008
  frame_008 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_008.label = "Transform Geometry"
  frame_008.name = "Frame.008"
  frame_008.show_options = True
  frame_008.label_size = 20
  frame_008.shrink = True

  # Node Switch.001
  switch_001 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSwitch")
  switch_001.name = "Switch.001"
  switch_001.show_options = True
  switch_001.input_type = 'RGBA'
  # False
  switch_001.inputs[1].default_value = (0.6038312911987305, 0.6038312911987305, 0.6038312911987305, 1.0)

  # Node Sample Index
  sample_index = sdf_points_to_mesh_1.nodes.new("GeometryNodeSampleIndex")
  sample_index.name = "Sample Index"
  sample_index.hide = True
  sample_index.show_options = True
  sample_index.clamp = False
  sample_index.data_type = 'FLOAT'
  sample_index.domain = 'POINT'

  # Node Named Attribute
  named_attribute = sdf_points_to_mesh_1.nodes.new("GeometryNodeInputNamedAttribute")
  named_attribute.name = "Named Attribute"
  named_attribute.hide = True
  named_attribute.show_options = True
  named_attribute.data_type = 'FLOAT'

  # Node Store Named Attribute
  store_named_attribute = sdf_points_to_mesh_1.nodes.new("GeometryNodeStoreNamedAttribute")
  store_named_attribute.name = "Store Named Attribute"
  store_named_attribute.hide = True
  store_named_attribute.show_options = True
  store_named_attribute.data_type = 'FLOAT'
  store_named_attribute.domain = 'POINT'
  store_named_attribute.inputs[1].hide = True
  # Selection
  store_named_attribute.inputs[1].default_value = True

  # Node Sample Index.002
  sample_index_002 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSampleIndex")
  sample_index_002.name = "Sample Index.002"
  sample_index_002.hide = True
  sample_index_002.show_options = True
  sample_index_002.clamp = False
  sample_index_002.data_type = 'FLOAT'
  sample_index_002.domain = 'POINT'

  # Node Named Attribute.002
  named_attribute_002 = sdf_points_to_mesh_1.nodes.new("GeometryNodeInputNamedAttribute")
  named_attribute_002.name = "Named Attribute.002"
  named_attribute_002.hide = True
  named_attribute_002.show_options = True
  named_attribute_002.data_type = 'FLOAT'

  # Node Store Named Attribute.002
  store_named_attribute_002 = sdf_points_to_mesh_1.nodes.new("GeometryNodeStoreNamedAttribute")
  store_named_attribute_002.name = "Store Named Attribute.002"
  store_named_attribute_002.hide = True
  store_named_attribute_002.show_options = True
  store_named_attribute_002.data_type = 'FLOAT'
  store_named_attribute_002.domain = 'POINT'
  store_named_attribute_002.inputs[1].hide = True
  # Selection
  store_named_attribute_002.inputs[1].default_value = True

  # Node Sample Index.003
  sample_index_003 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSampleIndex")
  sample_index_003.name = "Sample Index.003"
  sample_index_003.hide = True
  sample_index_003.show_options = True
  sample_index_003.clamp = False
  sample_index_003.data_type = 'FLOAT'
  sample_index_003.domain = 'POINT'

  # Node Named Attribute.003
  named_attribute_003 = sdf_points_to_mesh_1.nodes.new("GeometryNodeInputNamedAttribute")
  named_attribute_003.name = "Named Attribute.003"
  named_attribute_003.hide = True
  named_attribute_003.show_options = True
  named_attribute_003.data_type = 'FLOAT'

  # Node Store Named Attribute.003
  store_named_attribute_003 = sdf_points_to_mesh_1.nodes.new("GeometryNodeStoreNamedAttribute")
  store_named_attribute_003.name = "Store Named Attribute.003"
  store_named_attribute_003.hide = True
  store_named_attribute_003.show_options = True
  store_named_attribute_003.data_type = 'FLOAT'
  store_named_attribute_003.domain = 'POINT'
  store_named_attribute_003.inputs[1].hide = True
  # Selection
  store_named_attribute_003.inputs[1].default_value = True

  # Node Math
  math = sdf_points_to_mesh_1.nodes.new("ShaderNodeMath")
  math.name = "Math"
  math.hide = True
  math.show_options = True
  math.operation = 'SUBTRACT'
  math.use_clamp = False
  math.inputs[0].hide = True
  math.inputs[2].hide = True
  # Value
  math.inputs[0].default_value = 0.0020000000949949026

  # Node Group Input.014
  group_input_014 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_014.label = "Metallic Attribute"
  group_input_014.name = "Group Input.014"
  group_input_014.hide = True
  group_input_014.show_options = True
  group_input_014.outputs[0].hide = True
  group_input_014.outputs[1].hide = True
  group_input_014.outputs[2].hide = True
  group_input_014.outputs[3].hide = True
  group_input_014.outputs[4].hide = True
  group_input_014.outputs[5].hide = True
  group_input_014.outputs[6].hide = True
  group_input_014.outputs[7].hide = True
  group_input_014.outputs[8].hide = True
  group_input_014.outputs[9].hide = True
  group_input_014.outputs[10].hide = True
  group_input_014.outputs[11].hide = True
  group_input_014.outputs[12].hide = True
  group_input_014.outputs[13].hide = True
  group_input_014.outputs[15].hide = True
  group_input_014.outputs[16].hide = True
  group_input_014.outputs[17].hide = True
  group_input_014.outputs[18].hide = True
  group_input_014.outputs[19].hide = True
  group_input_014.outputs[20].hide = True
  group_input_014.outputs[21].hide = True

  # Node Group Input.015
  group_input_015 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_015.label = "Metallic"
  group_input_015.name = "Group Input.015"
  group_input_015.hide = True
  group_input_015.show_options = True
  group_input_015.outputs[0].hide = True
  group_input_015.outputs[1].hide = True
  group_input_015.outputs[2].hide = True
  group_input_015.outputs[3].hide = True
  group_input_015.outputs[4].hide = True
  group_input_015.outputs[5].hide = True
  group_input_015.outputs[6].hide = True
  group_input_015.outputs[7].hide = True
  group_input_015.outputs[8].hide = True
  group_input_015.outputs[9].hide = True
  group_input_015.outputs[10].hide = True
  group_input_015.outputs[11].hide = True
  group_input_015.outputs[12].hide = True
  group_input_015.outputs[13].hide = True
  group_input_015.outputs[14].hide = True
  group_input_015.outputs[15].hide = True
  group_input_015.outputs[16].hide = True
  group_input_015.outputs[17].hide = True
  group_input_015.outputs[19].hide = True
  group_input_015.outputs[20].hide = True
  group_input_015.outputs[21].hide = True

  # Node Group Input.016
  group_input_016 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_016.label = "Roughness"
  group_input_016.name = "Group Input.016"
  group_input_016.hide = True
  group_input_016.show_options = True
  group_input_016.outputs[0].hide = True
  group_input_016.outputs[1].hide = True
  group_input_016.outputs[2].hide = True
  group_input_016.outputs[3].hide = True
  group_input_016.outputs[4].hide = True
  group_input_016.outputs[5].hide = True
  group_input_016.outputs[6].hide = True
  group_input_016.outputs[7].hide = True
  group_input_016.outputs[8].hide = True
  group_input_016.outputs[9].hide = True
  group_input_016.outputs[10].hide = True
  group_input_016.outputs[11].hide = True
  group_input_016.outputs[12].hide = True
  group_input_016.outputs[13].hide = True
  group_input_016.outputs[14].hide = True
  group_input_016.outputs[15].hide = True
  group_input_016.outputs[16].hide = True
  group_input_016.outputs[17].hide = True
  group_input_016.outputs[18].hide = True
  group_input_016.outputs[20].hide = True
  group_input_016.outputs[21].hide = True

  # Node Group Input.017
  group_input_017 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_017.label = "Roughness Attribute"
  group_input_017.name = "Group Input.017"
  group_input_017.hide = True
  group_input_017.show_options = True
  group_input_017.outputs[0].hide = True
  group_input_017.outputs[1].hide = True
  group_input_017.outputs[2].hide = True
  group_input_017.outputs[3].hide = True
  group_input_017.outputs[4].hide = True
  group_input_017.outputs[5].hide = True
  group_input_017.outputs[6].hide = True
  group_input_017.outputs[7].hide = True
  group_input_017.outputs[8].hide = True
  group_input_017.outputs[9].hide = True
  group_input_017.outputs[10].hide = True
  group_input_017.outputs[11].hide = True
  group_input_017.outputs[12].hide = True
  group_input_017.outputs[13].hide = True
  group_input_017.outputs[14].hide = True
  group_input_017.outputs[16].hide = True
  group_input_017.outputs[17].hide = True
  group_input_017.outputs[18].hide = True
  group_input_017.outputs[19].hide = True
  group_input_017.outputs[20].hide = True
  group_input_017.outputs[21].hide = True

  # Node Group Input.018
  group_input_018 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_018.label = "Opacity"
  group_input_018.name = "Group Input.018"
  group_input_018.hide = True
  group_input_018.show_options = True
  group_input_018.outputs[0].hide = True
  group_input_018.outputs[1].hide = True
  group_input_018.outputs[2].hide = True
  group_input_018.outputs[3].hide = True
  group_input_018.outputs[4].hide = True
  group_input_018.outputs[5].hide = True
  group_input_018.outputs[6].hide = True
  group_input_018.outputs[7].hide = True
  group_input_018.outputs[8].hide = True
  group_input_018.outputs[9].hide = True
  group_input_018.outputs[10].hide = True
  group_input_018.outputs[11].hide = True
  group_input_018.outputs[12].hide = True
  group_input_018.outputs[13].hide = True
  group_input_018.outputs[14].hide = True
  group_input_018.outputs[15].hide = True
  group_input_018.outputs[16].hide = True
  group_input_018.outputs[17].hide = True
  group_input_018.outputs[18].hide = True
  group_input_018.outputs[19].hide = True
  group_input_018.outputs[21].hide = True

  # Node Group Input.019
  group_input_019 = sdf_points_to_mesh_1.nodes.new("NodeGroupInput")
  group_input_019.label = "Opacity Attribute"
  group_input_019.name = "Group Input.019"
  group_input_019.hide = True
  group_input_019.show_options = True
  group_input_019.outputs[0].hide = True
  group_input_019.outputs[1].hide = True
  group_input_019.outputs[2].hide = True
  group_input_019.outputs[3].hide = True
  group_input_019.outputs[4].hide = True
  group_input_019.outputs[5].hide = True
  group_input_019.outputs[6].hide = True
  group_input_019.outputs[7].hide = True
  group_input_019.outputs[8].hide = True
  group_input_019.outputs[9].hide = True
  group_input_019.outputs[10].hide = True
  group_input_019.outputs[11].hide = True
  group_input_019.outputs[12].hide = True
  group_input_019.outputs[13].hide = True
  group_input_019.outputs[14].hide = True
  group_input_019.outputs[15].hide = True
  group_input_019.outputs[17].hide = True
  group_input_019.outputs[18].hide = True
  group_input_019.outputs[19].hide = True
  group_input_019.outputs[20].hide = True
  group_input_019.outputs[21].hide = True

  # Node Switch.002
  switch_002 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSwitch")
  switch_002.name = "Switch.002"
  switch_002.show_options = True
  switch_002.input_type = 'FLOAT'
  # False
  switch_002.inputs[1].default_value = 1.0

  # Node Switch.003
  switch_003 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSwitch")
  switch_003.name = "Switch.003"
  switch_003.show_options = True
  switch_003.input_type = 'FLOAT'
  # False
  switch_003.inputs[1].default_value = 0.800000011920929

  # Node Switch.004
  switch_004 = sdf_points_to_mesh_1.nodes.new("GeometryNodeSwitch")
  switch_004.name = "Switch.004"
  switch_004.show_options = True
  switch_004.input_type = 'FLOAT'
  # False
  switch_004.inputs[1].default_value = 0.0

  # Node Reroute.004
  reroute_004 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_004.name = "Reroute.004"
  reroute_004.show_options = True
  reroute_004.socket_idname = "NodeSocketGeometry"
  # Node Reroute.005
  reroute_005 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_005.name = "Reroute.005"
  reroute_005.show_options = True
  reroute_005.socket_idname = "NodeSocketInt"
  # Node Reroute.006
  reroute_006 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_006.name = "Reroute.006"
  reroute_006.show_options = True
  reroute_006.socket_idname = "NodeSocketInt"
  # Node Reroute.007
  reroute_007 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_007.name = "Reroute.007"
  reroute_007.show_options = True
  reroute_007.socket_idname = "NodeSocketGeometry"
  # Node Reroute.008
  reroute_008 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_008.name = "Reroute.008"
  reroute_008.show_options = True
  reroute_008.socket_idname = "NodeSocketInt"
  # Node Reroute.009
  reroute_009 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_009.name = "Reroute.009"
  reroute_009.show_options = True
  reroute_009.socket_idname = "NodeSocketGeometry"
  # Node Reroute.010
  reroute_010 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_010.name = "Reroute.010"
  reroute_010.show_options = True
  reroute_010.socket_idname = "NodeSocketInt"
  # Node Frame.009
  frame_009 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_009.label = "Set Material"
  frame_009.name = "Frame.009"
  frame_009.show_options = True
  frame_009.label_size = 20
  frame_009.shrink = True

  # Node Frame.010
  frame_010 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_010.label = "Opacity"
  frame_010.name = "Frame.010"
  frame_010.show_options = True
  frame_010.label_size = 20
  frame_010.shrink = True

  # Node Frame.011
  frame_011 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_011.label = "Roughness"
  frame_011.name = "Frame.011"
  frame_011.show_options = True
  frame_011.label_size = 20
  frame_011.shrink = True

  # Node Reroute.011
  reroute_011 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_011.name = "Reroute.011"
  reroute_011.show_options = True
  reroute_011.socket_idname = "NodeSocketInt"
  # Node Reroute.012
  reroute_012 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_012.name = "Reroute.012"
  reroute_012.show_options = True
  reroute_012.socket_idname = "NodeSocketGeometry"
  # Node Frame.012
  frame_012 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_012.label = "Metallic"
  frame_012.name = "Frame.012"
  frame_012.show_options = True
  frame_012.label_size = 20
  frame_012.shrink = True

  # Node Reroute.013
  reroute_013 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_013.name = "Reroute.013"
  reroute_013.show_options = True
  reroute_013.socket_idname = "NodeSocketGeometry"
  # Node Reroute.014
  reroute_014 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_014.name = "Reroute.014"
  reroute_014.show_options = True
  reroute_014.socket_idname = "NodeSocketInt"
  # Node Reroute.015
  reroute_015 = sdf_points_to_mesh_1.nodes.new("NodeReroute")
  reroute_015.name = "Reroute.015"
  reroute_015.show_options = True
  reroute_015.socket_idname = "NodeSocketGeometry"
  # Node Frame.013
  frame_013 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_013.label = "Nearest Point"
  frame_013.name = "Frame.013"
  frame_013.show_options = True
  frame_013.label_size = 20
  frame_013.shrink = True

  # Node Frame.014
  frame_014 = sdf_points_to_mesh_1.nodes.new("NodeFrame")
  frame_014.label = "Color"
  frame_014.name = "Frame.014"
  frame_014.show_options = True
  frame_014.label_size = 20
  frame_014.shrink = True

  # Set parents
  sdf_points_to_mesh_1.nodes["Group Output"].parent = sdf_points_to_mesh_1.nodes["Frame.008"]
  sdf_points_to_mesh_1.nodes["Set Shade Smooth.004"].parent = sdf_points_to_mesh_1.nodes["Frame.001"]
  sdf_points_to_mesh_1.nodes["Group.012"].parent = sdf_points_to_mesh_1.nodes["Frame.004"]
  sdf_points_to_mesh_1.nodes["Group.016"].parent = sdf_points_to_mesh_1.nodes["Frame.004"]
  sdf_points_to_mesh_1.nodes["SDF_Remesh.001"].parent = sdf_points_to_mesh_1.nodes["Frame.003"]
  sdf_points_to_mesh_1.nodes["Named Attribute.001"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Store Named Attribute.001"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Set Material.001"].parent = sdf_points_to_mesh_1.nodes["Frame.009"]
  sdf_points_to_mesh_1.nodes["Sample Nearest.001"].parent = sdf_points_to_mesh_1.nodes["Frame.013"]
  sdf_points_to_mesh_1.nodes["Position.005"].parent = sdf_points_to_mesh_1.nodes["Frame.013"]
  sdf_points_to_mesh_1.nodes["Sample Index.001"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Group Input.003"].parent = sdf_points_to_mesh_1.nodes["Frame.013"]
  sdf_points_to_mesh_1.nodes["Group Input"].parent = sdf_points_to_mesh_1.nodes["Frame.009"]
  sdf_points_to_mesh_1.nodes["Group Input.002"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Group Input.004"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Group Input.005"].parent = sdf_points_to_mesh_1.nodes["Frame.003"]
  sdf_points_to_mesh_1.nodes["Menu Switch"].parent = sdf_points_to_mesh_1.nodes["Frame.002"]
  sdf_points_to_mesh_1.nodes["Group Input.006"].parent = sdf_points_to_mesh_1.nodes["Frame.002"]
  sdf_points_to_mesh_1.nodes["Group Input.007"].parent = sdf_points_to_mesh_1.nodes["Frame.004"]
  sdf_points_to_mesh_1.nodes["Group Input.008"].parent = sdf_points_to_mesh_1.nodes["Frame.004"]
  sdf_points_to_mesh_1.nodes["Group.013"].parent = sdf_points_to_mesh_1.nodes["Frame.005"]
  sdf_points_to_mesh_1.nodes["Group.017"].parent = sdf_points_to_mesh_1.nodes["Frame.005"]
  sdf_points_to_mesh_1.nodes["Group Input.010"].parent = sdf_points_to_mesh_1.nodes["Frame.005"]
  sdf_points_to_mesh_1.nodes["Group Input.011"].parent = sdf_points_to_mesh_1.nodes["Frame.005"]
  sdf_points_to_mesh_1.nodes["Group Input.001"].parent = sdf_points_to_mesh_1.nodes["Frame.001"]
  sdf_points_to_mesh_1.nodes["Reroute"].parent = sdf_points_to_mesh_1.nodes["Frame"]
  sdf_points_to_mesh_1.nodes["Bounding Box"].parent = sdf_points_to_mesh_1.nodes["Frame.006"]
  sdf_points_to_mesh_1.nodes["Reroute.001"].parent = sdf_points_to_mesh_1.nodes["Frame.006"]
  sdf_points_to_mesh_1.nodes["Transform Geometry"].parent = sdf_points_to_mesh_1.nodes["Frame.006"]
  sdf_points_to_mesh_1.nodes["Vector Math"].parent = sdf_points_to_mesh_1.nodes["Frame.006"]
  sdf_points_to_mesh_1.nodes["Switch"].parent = sdf_points_to_mesh_1.nodes["Frame.006"]
  sdf_points_to_mesh_1.nodes["Group Input.009"].parent = sdf_points_to_mesh_1.nodes["Frame.006"]
  sdf_points_to_mesh_1.nodes["Reroute.002"].parent = sdf_points_to_mesh_1.nodes["Frame.006"]
  sdf_points_to_mesh_1.nodes["Frame.006"].parent = sdf_points_to_mesh_1.nodes["Frame.008"]
  sdf_points_to_mesh_1.nodes["Transform Geometry.001"].parent = sdf_points_to_mesh_1.nodes["Frame.007"]
  sdf_points_to_mesh_1.nodes["Group Input.012"].parent = sdf_points_to_mesh_1.nodes["Frame.007"]
  sdf_points_to_mesh_1.nodes["Frame.007"].parent = sdf_points_to_mesh_1.nodes["Frame.008"]
  sdf_points_to_mesh_1.nodes["Menu Switch.001"].parent = sdf_points_to_mesh_1.nodes["Frame.007"]
  sdf_points_to_mesh_1.nodes["Group Input.013"].parent = sdf_points_to_mesh_1.nodes["Frame.007"]
  sdf_points_to_mesh_1.nodes["Euler to Rotation"].parent = sdf_points_to_mesh_1.nodes["Frame.007"]
  sdf_points_to_mesh_1.nodes["Combine XYZ"].parent = sdf_points_to_mesh_1.nodes["Frame.007"]
  sdf_points_to_mesh_1.nodes["Reroute.003"].parent = sdf_points_to_mesh_1.nodes["Frame.007"]
  sdf_points_to_mesh_1.nodes["Switch.001"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Sample Index"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Named Attribute"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Store Named Attribute"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Sample Index.002"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Named Attribute.002"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Store Named Attribute.002"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Sample Index.003"].parent = sdf_points_to_mesh_1.nodes["Frame.010"]
  sdf_points_to_mesh_1.nodes["Named Attribute.003"].parent = sdf_points_to_mesh_1.nodes["Frame.010"]
  sdf_points_to_mesh_1.nodes["Store Named Attribute.003"].parent = sdf_points_to_mesh_1.nodes["Frame.010"]
  sdf_points_to_mesh_1.nodes["Math"].parent = sdf_points_to_mesh_1.nodes["Frame.003"]
  sdf_points_to_mesh_1.nodes["Group Input.014"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Group Input.015"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Group Input.016"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Group Input.017"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Group Input.018"].parent = sdf_points_to_mesh_1.nodes["Frame.010"]
  sdf_points_to_mesh_1.nodes["Group Input.019"].parent = sdf_points_to_mesh_1.nodes["Frame.010"]
  sdf_points_to_mesh_1.nodes["Switch.002"].parent = sdf_points_to_mesh_1.nodes["Frame.010"]
  sdf_points_to_mesh_1.nodes["Switch.003"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Switch.004"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Reroute.004"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Reroute.005"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Reroute.006"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Reroute.007"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Reroute.008"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Reroute.009"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Reroute.010"].parent = sdf_points_to_mesh_1.nodes["Frame.011"]
  sdf_points_to_mesh_1.nodes["Frame.009"].parent = sdf_points_to_mesh_1.nodes["Frame"]
  sdf_points_to_mesh_1.nodes["Frame.010"].parent = sdf_points_to_mesh_1.nodes["Frame"]
  sdf_points_to_mesh_1.nodes["Frame.011"].parent = sdf_points_to_mesh_1.nodes["Frame"]
  sdf_points_to_mesh_1.nodes["Reroute.011"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Reroute.012"].parent = sdf_points_to_mesh_1.nodes["Frame.012"]
  sdf_points_to_mesh_1.nodes["Frame.012"].parent = sdf_points_to_mesh_1.nodes["Frame"]
  sdf_points_to_mesh_1.nodes["Reroute.013"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Reroute.014"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Reroute.015"].parent = sdf_points_to_mesh_1.nodes["Frame.014"]
  sdf_points_to_mesh_1.nodes["Frame.013"].parent = sdf_points_to_mesh_1.nodes["Frame"]
  sdf_points_to_mesh_1.nodes["Frame.014"].parent = sdf_points_to_mesh_1.nodes["Frame"]

  # Set locations
  sdf_points_to_mesh_1.nodes["Group Output"].location = (709.477783203125, -96.32781982421875)
  sdf_points_to_mesh_1.nodes["Set Shade Smooth.004"].location = (30.197296142578125, -40.23419189453125)
  sdf_points_to_mesh_1.nodes["Group.012"].location = (306.7373046875, -36.8153076171875)
  sdf_points_to_mesh_1.nodes["Group.016"].location = (166.56793212890625, -35.8245849609375)
  sdf_points_to_mesh_1.nodes["SDF_Remesh.001"].location = (154.32952880859375, -35.822723388671875)
  sdf_points_to_mesh_1.nodes["Named Attribute.001"].location = (69.27349853515625, -387.15081787109375)
  sdf_points_to_mesh_1.nodes["Store Named Attribute.001"].location = (31.49542236328125, -64.8436279296875)
  sdf_points_to_mesh_1.nodes["Set Material.001"].location = (29.9215087890625, -40.16949462890625)
  sdf_points_to_mesh_1.nodes["Sample Nearest.001"].location = (32.110755920410156, -74.17803955078125)
  sdf_points_to_mesh_1.nodes["Position.005"].location = (32.075843811035156, -108.75494384765625)
  sdf_points_to_mesh_1.nodes["Sample Index.001"].location = (69.3455810546875, -178.24298095703125)
  sdf_points_to_mesh_1.nodes["Group Input.003"].location = (29.85059356689453, -40.24755859375)
  sdf_points_to_mesh_1.nodes["Group Input"].location = (30.0592041015625, -75.16046142578125)
  sdf_points_to_mesh_1.nodes["Group Input.002"].location = (29.9857177734375, -104.73675537109375)
  sdf_points_to_mesh_1.nodes["Group Input.004"].location = (71.73223876953125, -421.36279296875)
  sdf_points_to_mesh_1.nodes["Frame"].location = (-98.11019897460938, -580.5)
  sdf_points_to_mesh_1.nodes["Group Input.005"].location = (30.27447509765625, -73.03662109375)
  sdf_points_to_mesh_1.nodes["Menu Switch"].location = (29.9031982421875, -73.4696044921875)
  sdf_points_to_mesh_1.nodes["Group Input.006"].location = (31.0472412109375, -39.86297607421875)
  sdf_points_to_mesh_1.nodes["Group Input.007"].location = (30.2237548828125, -93.10687255859375)
  sdf_points_to_mesh_1.nodes["Group Input.008"].location = (305.0556640625, -171.864013671875)
  sdf_points_to_mesh_1.nodes["Group.013"].location = (306.8751220703125, -37.00897216796875)
  sdf_points_to_mesh_1.nodes["Group.017"].location = (162.9666748046875, -36.01824951171875)
  sdf_points_to_mesh_1.nodes["Group Input.010"].location = (29.92431640625, -106.1834716796875)
  sdf_points_to_mesh_1.nodes["Group Input.011"].location = (305.193359375, -173.0)
  sdf_points_to_mesh_1.nodes["Group Input.001"].location = (30.02508544921875, -76.2791748046875)
  sdf_points_to_mesh_1.nodes["Frame.001"].location = (-328.0, -580.0)
  sdf_points_to_mesh_1.nodes["Reroute"].location = (35.0, -99.28228759765625)
  sdf_points_to_mesh_1.nodes["Frame.002"].location = (-550.5, -582.5)
  sdf_points_to_mesh_1.nodes["Frame.003"].location = (-956.5, -439.5)
  sdf_points_to_mesh_1.nodes["Frame.004"].location = (-1085.0, -689.0)
  sdf_points_to_mesh_1.nodes["Frame.005"].location = (-1088.0, -978.0)
  sdf_points_to_mesh_1.nodes["Bounding Box"].location = (136.2802734375, -150.60968017578125)
  sdf_points_to_mesh_1.nodes["Reroute.001"].location = (116.31494140625, -77.11236572265625)
  sdf_points_to_mesh_1.nodes["Transform Geometry"].location = (137.611083984375, -81.67303466796875)
  sdf_points_to_mesh_1.nodes["Vector Math"].location = (136.556396484375, -116.1771240234375)
  sdf_points_to_mesh_1.nodes["Switch"].location = (138.73974609375, -45.24969482421875)
  sdf_points_to_mesh_1.nodes["Group Input.009"].location = (29.865966796875, -41.45977783203125)
  sdf_points_to_mesh_1.nodes["Reroute.002"].location = (48.04052734375, -113.5772705078125)
  sdf_points_to_mesh_1.nodes["Frame.006"].location = (30.0, -36.0)
  sdf_points_to_mesh_1.nodes["Transform Geometry.001"].location = (174.245849609375, -35.822265625)
  sdf_points_to_mesh_1.nodes["Group Input.012"].location = (175.181396484375, -140.17169189453125)
  sdf_points_to_mesh_1.nodes["Frame.007"].location = (342.774169921875, -36.5)
  sdf_points_to_mesh_1.nodes["Menu Switch.001"].location = (32.40380859375, -153.40411376953125)
  sdf_points_to_mesh_1.nodes["Group Input.013"].location = (31.8017578125, -187.322509765625)
  sdf_points_to_mesh_1.nodes["Euler to Rotation"].location = (32.91845703125, -83.0426025390625)
  sdf_points_to_mesh_1.nodes["Combine XYZ"].location = (32.929931640625, -118.174560546875)
  sdf_points_to_mesh_1.nodes["Reroute.003"].location = (35.0, -70.5528564453125)
  sdf_points_to_mesh_1.nodes["Frame.008"].location = (1331.5, -576.5)
  sdf_points_to_mesh_1.nodes["Switch.001"].location = (70.2318115234375, -215.0889892578125)
  sdf_points_to_mesh_1.nodes["Sample Index"].location = (61.84051513671875, -178.41595458984375)
  sdf_points_to_mesh_1.nodes["Named Attribute"].location = (58.4222412109375, -387.44903564453125)
  sdf_points_to_mesh_1.nodes["Store Named Attribute"].location = (31.57427978515625, -65.046630859375)
  sdf_points_to_mesh_1.nodes["Sample Index.002"].location = (65.7523193359375, -180.243408203125)
  sdf_points_to_mesh_1.nodes["Named Attribute.002"].location = (68.42724609375, -387.785400390625)
  sdf_points_to_mesh_1.nodes["Store Named Attribute.002"].location = (32.8275146484375, -64.9759521484375)
  sdf_points_to_mesh_1.nodes["Sample Index.003"].location = (32.481201171875, -149.838134765625)
  sdf_points_to_mesh_1.nodes["Named Attribute.003"].location = (33.16357421875, -358.12701416015625)
  sdf_points_to_mesh_1.nodes["Store Named Attribute.003"].location = (30.1923828125, -64.7882080078125)
  sdf_points_to_mesh_1.nodes["Math"].location = (29.92279052734375, -158.61273193359375)
  sdf_points_to_mesh_1.nodes["Group Input.014"].location = (30.021728515625, -105.23248291015625)
  sdf_points_to_mesh_1.nodes["Group Input.015"].location = (58.3154296875, -420.9464111328125)
  sdf_points_to_mesh_1.nodes["Group Input.016"].location = (67.487060546875, -423.5496826171875)
  sdf_points_to_mesh_1.nodes["Group Input.017"].location = (29.81982421875, -106.971435546875)
  sdf_points_to_mesh_1.nodes["Group Input.018"].location = (34.0438232421875, -394.20928955078125)
  sdf_points_to_mesh_1.nodes["Group Input.019"].location = (29.92724609375, -105.20123291015625)
  sdf_points_to_mesh_1.nodes["Switch.002"].location = (32.3282470703125, -185.1488037109375)
  sdf_points_to_mesh_1.nodes["Switch.003"].location = (66.242919921875, -216.77008056640625)
  sdf_points_to_mesh_1.nodes["Switch.004"].location = (61.69903564453125, -214.942626953125)
  sdf_points_to_mesh_1.nodes["Reroute.004"].location = (35.51776123046875, -140.05035400390625)
  sdf_points_to_mesh_1.nodes["Reroute.005"].location = (35.7640380859375, -155.5517578125)
  sdf_points_to_mesh_1.nodes["Reroute.006"].location = (35.67822265625, -153.1019287109375)
  sdf_points_to_mesh_1.nodes["Reroute.007"].location = (35.9537353515625, -142.2314453125)
  sdf_points_to_mesh_1.nodes["Reroute.008"].location = (35.4603271484375, -156.31622314453125)
  sdf_points_to_mesh_1.nodes["Reroute.009"].location = (181.5743408203125, -142.7099609375)
  sdf_points_to_mesh_1.nodes["Reroute.010"].location = (180.8067626953125, -157.09490966796875)
  sdf_points_to_mesh_1.nodes["Frame.009"].location = (1187.6102294921875, -38.0)
  sdf_points_to_mesh_1.nodes["Frame.010"].location = (952.1102294921875, -38.0)
  sdf_points_to_mesh_1.nodes["Frame.011"].location = (706.6102294921875, -36.0)
  sdf_points_to_mesh_1.nodes["Reroute.011"].location = (179.72674560546875, -154.52947998046875)
  sdf_points_to_mesh_1.nodes["Reroute.012"].location = (179.72674560546875, -140.6551513671875)
  sdf_points_to_mesh_1.nodes["Frame.012"].location = (463.1101989746094, -38.0)
  sdf_points_to_mesh_1.nodes["Reroute.013"].location = (182.23611450195312, -142.04095458984375)
  sdf_points_to_mesh_1.nodes["Reroute.014"].location = (182.23611450195312, -154.8863525390625)
  sdf_points_to_mesh_1.nodes["Reroute.015"].location = (36.33892822265625, -140.418701171875)
  sdf_points_to_mesh_1.nodes["Frame.013"].location = (30.610198974609375, -133.5)
  sdf_points_to_mesh_1.nodes["Frame.014"].location = (217.61019897460938, -36.5)

  # Set dimensions
  sdf_points_to_mesh_1.nodes["Group Output"].width  = 117.588134765625
  sdf_points_to_mesh_1.nodes["Group Output"].height = 100.0

  sdf_points_to_mesh_1.nodes["Set Shade Smooth.004"].width  = 140.0
  sdf_points_to_mesh_1.nodes["Set Shade Smooth.004"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group.012"].width  = 134.47119140625
  sdf_points_to_mesh_1.nodes["Group.012"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group.016"].width  = 114.056640625
  sdf_points_to_mesh_1.nodes["Group.016"].height = 100.0

  sdf_points_to_mesh_1.nodes["SDF_Remesh.001"].width  = 158.1834716796875
  sdf_points_to_mesh_1.nodes["SDF_Remesh.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Named Attribute.001"].width  = 121.30899047851562
  sdf_points_to_mesh_1.nodes["Named Attribute.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Store Named Attribute.001"].width  = 152.94659423828125
  sdf_points_to_mesh_1.nodes["Store Named Attribute.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Set Material.001"].width  = 102.26641845703125
  sdf_points_to_mesh_1.nodes["Set Material.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Sample Nearest.001"].width  = 100.0
  sdf_points_to_mesh_1.nodes["Sample Nearest.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Position.005"].width  = 100.0
  sdf_points_to_mesh_1.nodes["Position.005"].height = 100.0

  sdf_points_to_mesh_1.nodes["Sample Index.001"].width  = 119.60791015625
  sdf_points_to_mesh_1.nodes["Sample Index.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.003"].width  = 80.0
  sdf_points_to_mesh_1.nodes["Group Input.003"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input"].width  = 99.48046875
  sdf_points_to_mesh_1.nodes["Group Input"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.002"].width  = 153.3594970703125
  sdf_points_to_mesh_1.nodes["Group Input.002"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.004"].width  = 98.4730224609375
  sdf_points_to_mesh_1.nodes["Group Input.004"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame"].width  = 1379.8765869140625
  sdf_points_to_mesh_1.nodes["Frame"].height = 543.5

  sdf_points_to_mesh_1.nodes["Group Input.005"].width  = 99.4149169921875
  sdf_points_to_mesh_1.nodes["Group Input.005"].height = 100.0

  sdf_points_to_mesh_1.nodes["Menu Switch"].width  = 113.4481201171875
  sdf_points_to_mesh_1.nodes["Menu Switch"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.006"].width  = 86.19781494140625
  sdf_points_to_mesh_1.nodes["Group Input.006"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.007"].width  = 109.5919189453125
  sdf_points_to_mesh_1.nodes["Group Input.007"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.008"].width  = 135.56048583984375
  sdf_points_to_mesh_1.nodes["Group Input.008"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group.013"].width  = 134.47119140625
  sdf_points_to_mesh_1.nodes["Group.013"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group.017"].width  = 120.993408203125
  sdf_points_to_mesh_1.nodes["Group.017"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.010"].width  = 109.5919189453125
  sdf_points_to_mesh_1.nodes["Group Input.010"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.011"].width  = 136.314208984375
  sdf_points_to_mesh_1.nodes["Group Input.011"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.001"].width  = 121.13421630859375
  sdf_points_to_mesh_1.nodes["Group Input.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame.001"].width  = 200.0
  sdf_points_to_mesh_1.nodes["Frame.001"].height = 130.5

  sdf_points_to_mesh_1.nodes["Reroute"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame.002"].width  = 173.4481201171875
  sdf_points_to_mesh_1.nodes["Frame.002"].height = 265.5

  sdf_points_to_mesh_1.nodes["Frame.003"].width  = 342.6834716796875
  sdf_points_to_mesh_1.nodes["Frame.003"].height = 228.0

  sdf_points_to_mesh_1.nodes["Frame.004"].width  = 470.97119140625
  sdf_points_to_mesh_1.nodes["Frame.004"].height = 254.0

  sdf_points_to_mesh_1.nodes["Frame.005"].width  = 471.47119140625
  sdf_points_to_mesh_1.nodes["Frame.005"].height = 282.0

  sdf_points_to_mesh_1.nodes["Bounding Box"].width  = 110.116943359375
  sdf_points_to_mesh_1.nodes["Bounding Box"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.001"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Transform Geometry"].width  = 108.8175048828125
  sdf_points_to_mesh_1.nodes["Transform Geometry"].height = 100.0

  sdf_points_to_mesh_1.nodes["Vector Math"].width  = 109.0948486328125
  sdf_points_to_mesh_1.nodes["Vector Math"].height = 100.0

  sdf_points_to_mesh_1.nodes["Switch"].width  = 105.7275390625
  sdf_points_to_mesh_1.nodes["Switch"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.009"].width  = 86.93499755859375
  sdf_points_to_mesh_1.nodes["Group Input.009"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.002"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.002"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame.006"].width  = 276.616943359375
  sdf_points_to_mesh_1.nodes["Frame.006"].height = 204.5

  sdf_points_to_mesh_1.nodes["Transform Geometry.001"].width  = 137.92730712890625
  sdf_points_to_mesh_1.nodes["Transform Geometry.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.012"].width  = 80.0
  sdf_points_to_mesh_1.nodes["Group Input.012"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame.007"].width  = 342.153076171875
  sdf_points_to_mesh_1.nodes["Frame.007"].height = 241.5

  sdf_points_to_mesh_1.nodes["Menu Switch.001"].width  = 111.8701171875
  sdf_points_to_mesh_1.nodes["Menu Switch.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.013"].width  = 112.47991943359375
  sdf_points_to_mesh_1.nodes["Group Input.013"].height = 100.0

  sdf_points_to_mesh_1.nodes["Euler to Rotation"].width  = 123.6221923828125
  sdf_points_to_mesh_1.nodes["Euler to Rotation"].height = 100.0

  sdf_points_to_mesh_1.nodes["Combine XYZ"].width  = 112.1944580078125
  sdf_points_to_mesh_1.nodes["Combine XYZ"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.003"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.003"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame.008"].width  = 857.088134765625
  sdf_points_to_mesh_1.nodes["Frame.008"].height = 308.0

  sdf_points_to_mesh_1.nodes["Switch.001"].width  = 119.03564453125
  sdf_points_to_mesh_1.nodes["Switch.001"].height = 100.0

  sdf_points_to_mesh_1.nodes["Sample Index"].width  = 119.238037109375
  sdf_points_to_mesh_1.nodes["Sample Index"].height = 100.0

  sdf_points_to_mesh_1.nodes["Named Attribute"].width  = 120.6697998046875
  sdf_points_to_mesh_1.nodes["Named Attribute"].height = 100.0

  sdf_points_to_mesh_1.nodes["Store Named Attribute"].width  = 153.6026611328125
  sdf_points_to_mesh_1.nodes["Store Named Attribute"].height = 100.0

  sdf_points_to_mesh_1.nodes["Sample Index.002"].width  = 119.238037109375
  sdf_points_to_mesh_1.nodes["Sample Index.002"].height = 100.0

  sdf_points_to_mesh_1.nodes["Named Attribute.002"].width  = 120.6697998046875
  sdf_points_to_mesh_1.nodes["Named Attribute.002"].height = 100.0

  sdf_points_to_mesh_1.nodes["Store Named Attribute.002"].width  = 153.6026611328125
  sdf_points_to_mesh_1.nodes["Store Named Attribute.002"].height = 100.0

  sdf_points_to_mesh_1.nodes["Sample Index.003"].width  = 119.238037109375
  sdf_points_to_mesh_1.nodes["Sample Index.003"].height = 100.0

  sdf_points_to_mesh_1.nodes["Named Attribute.003"].width  = 120.6697998046875
  sdf_points_to_mesh_1.nodes["Named Attribute.003"].height = 100.0

  sdf_points_to_mesh_1.nodes["Store Named Attribute.003"].width  = 153.6026611328125
  sdf_points_to_mesh_1.nodes["Store Named Attribute.003"].height = 100.0

  sdf_points_to_mesh_1.nodes["Math"].width  = 100.0
  sdf_points_to_mesh_1.nodes["Math"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.014"].width  = 155.70596313476562
  sdf_points_to_mesh_1.nodes["Group Input.014"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.015"].width  = 120.64425659179688
  sdf_points_to_mesh_1.nodes["Group Input.015"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.016"].width  = 122.24398803710938
  sdf_points_to_mesh_1.nodes["Group Input.016"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.017"].width  = 156.53857421875
  sdf_points_to_mesh_1.nodes["Group Input.017"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.018"].width  = 119.79571533203125
  sdf_points_to_mesh_1.nodes["Group Input.018"].height = 100.0

  sdf_points_to_mesh_1.nodes["Group Input.019"].width  = 153.093017578125
  sdf_points_to_mesh_1.nodes["Group Input.019"].height = 100.0

  sdf_points_to_mesh_1.nodes["Switch.002"].width  = 118.42364501953125
  sdf_points_to_mesh_1.nodes["Switch.002"].height = 100.0

  sdf_points_to_mesh_1.nodes["Switch.003"].width  = 117.944580078125
  sdf_points_to_mesh_1.nodes["Switch.003"].height = 100.0

  sdf_points_to_mesh_1.nodes["Switch.004"].width  = 117.944580078125
  sdf_points_to_mesh_1.nodes["Switch.004"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.004"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.004"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.005"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.005"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.006"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.006"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.007"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.007"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.008"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.008"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.009"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.009"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.010"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.010"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame.009"].width  = 162.266357421875
  sdf_points_to_mesh_1.nodes["Frame.009"].height = 129.0

  sdf_points_to_mesh_1.nodes["Frame.010"].width  = 213.6026611328125
  sdf_points_to_mesh_1.nodes["Frame.010"].height = 448.0

  sdf_points_to_mesh_1.nodes["Frame.011"].width  = 219.7440185546875
  sdf_points_to_mesh_1.nodes["Frame.011"].height = 477.5

  sdf_points_to_mesh_1.nodes["Reroute.011"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.011"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.012"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.012"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame.012"].width  = 215.7059326171875
  sdf_points_to_mesh_1.nodes["Frame.012"].height = 475.0

  sdf_points_to_mesh_1.nodes["Reroute.013"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.013"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.014"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.014"].height = 100.0

  sdf_points_to_mesh_1.nodes["Reroute.015"].width  = 20.0
  sdf_points_to_mesh_1.nodes["Reroute.015"].height = 100.0

  sdf_points_to_mesh_1.nodes["Frame.013"].width  = 162.0
  sdf_points_to_mesh_1.nodes["Frame.013"].height = 163.0

  sdf_points_to_mesh_1.nodes["Frame.014"].width  = 220.80899047851562
  sdf_points_to_mesh_1.nodes["Frame.014"].height = 475.5


  # Initialize sdf_points_to_mesh_1 links

  # group_016.Mesh -> group_012.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group.016"].outputs[0],
    sdf_points_to_mesh_1.nodes["Group.012"].inputs[0]
  )
  # position_005.Position -> sample_nearest_001.Sample Position
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Position.005"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Nearest.001"].inputs[1]
  )
  # reroute_015.Output -> sample_index_001.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.015"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.001"].inputs[0]
  )
  # group_input_003.Points -> sample_nearest_001.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.003"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Nearest.001"].inputs[0]
  )
  # group_input.Material -> set_material_001.Material
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input"].outputs[12],
    sdf_points_to_mesh_1.nodes["Set Material.001"].inputs[2]
  )
  # group_input_002.Color Attribute -> store_named_attribute_001.Name
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.002"].outputs[13],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.001"].inputs[2]
  )
  # group_input_004.Color -> named_attribute_001.Name
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.004"].outputs[17],
    sdf_points_to_mesh_1.nodes["Named Attribute.001"].inputs[0]
  )
  # group_input_005.Points -> sdf_remesh_001.Points
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.005"].outputs[0],
    sdf_points_to_mesh_1.nodes["SDF_Remesh.001"].inputs[0]
  )
  # reroute.Output -> store_named_attribute_001.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute"].outputs[0],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.001"].inputs[0]
  )
  # sdf_remesh_001.Mesh -> menu_switch.Dense Shell
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["SDF_Remesh.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Menu Switch"].inputs[1]
  )
  # group_012.Geometry -> menu_switch.Dense SDF
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group.012"].outputs[0],
    sdf_points_to_mesh_1.nodes["Menu Switch"].inputs[2]
  )
  # menu_switch.Output -> set_shade_smooth_004.Mesh
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Menu Switch"].outputs[0],
    sdf_points_to_mesh_1.nodes["Set Shade Smooth.004"].inputs[0]
  )
  # group_input_006.Meshing Method -> menu_switch.Menu
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.006"].outputs[4],
    sdf_points_to_mesh_1.nodes["Menu Switch"].inputs[0]
  )
  # group_input_007.Course Iterations -> group_016.Course Iterations
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.007"].outputs[5],
    sdf_points_to_mesh_1.nodes["Group.016"].inputs[1]
  )
  # group_input_007.Fine Iterations -> group_016.Fine Iterations
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.007"].outputs[6],
    sdf_points_to_mesh_1.nodes["Group.016"].inputs[2]
  )
  # group_input_008.Smooth Iterations -> group_012.Iterations
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.008"].outputs[8],
    sdf_points_to_mesh_1.nodes["Group.012"].inputs[2]
  )
  # group_017.Mesh -> group_013.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group.017"].outputs[0],
    sdf_points_to_mesh_1.nodes["Group.013"].inputs[0]
  )
  # group_input_010.Course Iterations -> group_017.Course Iterations
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.010"].outputs[5],
    sdf_points_to_mesh_1.nodes["Group.017"].inputs[1]
  )
  # group_input_010.Fine Iterations -> group_017.Fine Iterations
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.010"].outputs[6],
    sdf_points_to_mesh_1.nodes["Group.017"].inputs[2]
  )
  # group_input_011.Smooth Iterations -> group_013.Iterations
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.011"].outputs[8],
    sdf_points_to_mesh_1.nodes["Group.013"].inputs[2]
  )
  # group_013.Geometry -> menu_switch.Reduced SDF
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group.013"].outputs[0],
    sdf_points_to_mesh_1.nodes["Menu Switch"].inputs[3]
  )
  # group_input_010.Voxel Size -> group_017.Voxel Size
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.010"].outputs[9],
    sdf_points_to_mesh_1.nodes["Group.017"].inputs[5]
  )
  # group_input_010.Points -> group_017.Points
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.010"].outputs[0],
    sdf_points_to_mesh_1.nodes["Group.017"].inputs[0]
  )
  # group_input_007.Points -> group_016.Points
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.007"].outputs[0],
    sdf_points_to_mesh_1.nodes["Group.016"].inputs[0]
  )
  # group_input_001.Shade Smooth -> set_shade_smooth_004.Shade Smooth
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.001"].outputs[11],
    sdf_points_to_mesh_1.nodes["Set Shade Smooth.004"].inputs[2]
  )
  # set_shade_smooth_004.Mesh -> reroute.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Set Shade Smooth.004"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute"].inputs[0]
  )
  # reroute_002.Output -> reroute_001.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.002"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.001"].inputs[0]
  )
  # reroute_001.Output -> transform_geometry.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Transform Geometry"].inputs[0]
  )
  # bounding_box.Min -> vector_math.Vector
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Bounding Box"].outputs[1],
    sdf_points_to_mesh_1.nodes["Vector Math"].inputs[0]
  )
  # vector_math.Vector -> transform_geometry.Translation
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Vector Math"].outputs[0],
    sdf_points_to_mesh_1.nodes["Transform Geometry"].inputs[2]
  )
  # transform_geometry.Geometry -> switch.False
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Transform Geometry"].outputs[0],
    sdf_points_to_mesh_1.nodes["Switch"].inputs[1]
  )
  # reroute_001.Output -> switch.True
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Switch"].inputs[2]
  )
  # group_input_009.Centered -> switch.Switch
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.009"].outputs[3],
    sdf_points_to_mesh_1.nodes["Switch"].inputs[0]
  )
  # set_material_001.Geometry -> reroute_002.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Set Material.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.002"].inputs[0]
  )
  # reroute_002.Output -> bounding_box.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.002"].outputs[0],
    sdf_points_to_mesh_1.nodes["Bounding Box"].inputs[0]
  )
  # reroute_003.Output -> transform_geometry_001.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.003"].outputs[0],
    sdf_points_to_mesh_1.nodes["Transform Geometry.001"].inputs[0]
  )
  # group_input_012.Scale -> transform_geometry_001.Scale
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.012"].outputs[2],
    sdf_points_to_mesh_1.nodes["Transform Geometry.001"].inputs[4]
  )
  # group_input_013.Orientation -> menu_switch_001.Menu
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.013"].outputs[1],
    sdf_points_to_mesh_1.nodes["Menu Switch.001"].inputs[0]
  )
  # menu_switch_001.Output -> combine_xyz.Z
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Menu Switch.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Combine XYZ"].inputs[2]
  )
  # combine_xyz.Vector -> euler_to_rotation.Euler
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Combine XYZ"].outputs[0],
    sdf_points_to_mesh_1.nodes["Euler to Rotation"].inputs[0]
  )
  # euler_to_rotation.Rotation -> transform_geometry_001.Rotation
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Euler to Rotation"].outputs[0],
    sdf_points_to_mesh_1.nodes["Transform Geometry.001"].inputs[3]
  )
  # switch.Output -> reroute_003.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Switch"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.003"].inputs[0]
  )
  # named_attribute_001.Exists -> switch_001.Switch
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Named Attribute.001"].outputs[1],
    sdf_points_to_mesh_1.nodes["Switch.001"].inputs[0]
  )
  # switch_001.Output -> sample_index_001.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Switch.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.001"].inputs[1]
  )
  # sample_index_001.Value -> store_named_attribute_001.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Sample Index.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.001"].inputs[3]
  )
  # named_attribute_001.Attribute -> switch_001.True
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Named Attribute.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Switch.001"].inputs[2]
  )
  # reroute_004.Output -> sample_index.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.004"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index"].inputs[0]
  )
  # reroute_006.Output -> sample_index.Index
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.006"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index"].inputs[2]
  )
  # sample_index.Value -> store_named_attribute.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Sample Index"].outputs[0],
    sdf_points_to_mesh_1.nodes["Store Named Attribute"].inputs[3]
  )
  # store_named_attribute_001.Geometry -> store_named_attribute.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Store Named Attribute.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Store Named Attribute"].inputs[0]
  )
  # reroute_007.Output -> sample_index_002.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.007"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.002"].inputs[0]
  )
  # reroute_008.Output -> sample_index_002.Index
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.008"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.002"].inputs[2]
  )
  # sample_index_002.Value -> store_named_attribute_002.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Sample Index.002"].outputs[0],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.002"].inputs[3]
  )
  # store_named_attribute.Geometry -> store_named_attribute_002.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Store Named Attribute"].outputs[0],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.002"].inputs[0]
  )
  # reroute_009.Output -> sample_index_003.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.009"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.003"].inputs[0]
  )
  # reroute_010.Output -> sample_index_003.Index
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.010"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.003"].inputs[2]
  )
  # sample_index_003.Value -> store_named_attribute_003.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Sample Index.003"].outputs[0],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.003"].inputs[3]
  )
  # store_named_attribute_002.Geometry -> store_named_attribute_003.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Store Named Attribute.002"].outputs[0],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.003"].inputs[0]
  )
  # store_named_attribute_003.Geometry -> set_material_001.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Store Named Attribute.003"].outputs[0],
    sdf_points_to_mesh_1.nodes["Set Material.001"].inputs[0]
  )
  # transform_geometry_001.Geometry -> group_output.Geometry
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Transform Geometry.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Group Output"].inputs[0]
  )
  # math.Value -> sdf_remesh_001.Normal Inset
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Math"].outputs[0],
    sdf_points_to_mesh_1.nodes["SDF_Remesh.001"].inputs[2]
  )
  # group_input_005.Thickness -> math.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.005"].outputs[10],
    sdf_points_to_mesh_1.nodes["Math"].inputs[1]
  )
  # group_input_014.Metallic Attribute -> store_named_attribute.Name
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.014"].outputs[14],
    sdf_points_to_mesh_1.nodes["Store Named Attribute"].inputs[2]
  )
  # group_input_015.Metallic -> named_attribute.Name
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.015"].outputs[18],
    sdf_points_to_mesh_1.nodes["Named Attribute"].inputs[0]
  )
  # group_input_016.Roughness -> named_attribute_002.Name
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.016"].outputs[19],
    sdf_points_to_mesh_1.nodes["Named Attribute.002"].inputs[0]
  )
  # group_input_017.Roughness Attribute -> store_named_attribute_002.Name
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.017"].outputs[15],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.002"].inputs[2]
  )
  # group_input_018.Opacity -> named_attribute_003.Name
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.018"].outputs[20],
    sdf_points_to_mesh_1.nodes["Named Attribute.003"].inputs[0]
  )
  # group_input_019.Opacity Attribute -> store_named_attribute_003.Name
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.019"].outputs[16],
    sdf_points_to_mesh_1.nodes["Store Named Attribute.003"].inputs[2]
  )
  # named_attribute_003.Attribute -> switch_002.True
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Named Attribute.003"].outputs[0],
    sdf_points_to_mesh_1.nodes["Switch.002"].inputs[2]
  )
  # named_attribute_003.Exists -> switch_002.Switch
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Named Attribute.003"].outputs[1],
    sdf_points_to_mesh_1.nodes["Switch.002"].inputs[0]
  )
  # switch_002.Output -> sample_index_003.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Switch.002"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.003"].inputs[1]
  )
  # switch_003.Output -> sample_index_002.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Switch.003"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.002"].inputs[1]
  )
  # named_attribute_002.Attribute -> switch_003.True
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Named Attribute.002"].outputs[0],
    sdf_points_to_mesh_1.nodes["Switch.003"].inputs[2]
  )
  # named_attribute_002.Exists -> switch_003.Switch
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Named Attribute.002"].outputs[1],
    sdf_points_to_mesh_1.nodes["Switch.003"].inputs[0]
  )
  # switch_004.Output -> sample_index.Value
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Switch.004"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index"].inputs[1]
  )
  # named_attribute.Exists -> switch_004.Switch
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Named Attribute"].outputs[1],
    sdf_points_to_mesh_1.nodes["Switch.004"].inputs[0]
  )
  # named_attribute.Attribute -> switch_004.True
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Named Attribute"].outputs[0],
    sdf_points_to_mesh_1.nodes["Switch.004"].inputs[2]
  )
  # reroute_013.Output -> reroute_004.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.013"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.004"].inputs[0]
  )
  # sample_nearest_001.Index -> reroute_005.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Sample Nearest.001"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.005"].inputs[0]
  )
  # reroute_014.Output -> reroute_006.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.014"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.006"].inputs[0]
  )
  # reroute_012.Output -> reroute_007.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.012"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.007"].inputs[0]
  )
  # reroute_011.Output -> reroute_008.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.011"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.008"].inputs[0]
  )
  # reroute_007.Output -> reroute_009.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.007"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.009"].inputs[0]
  )
  # reroute_008.Output -> reroute_010.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.008"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.010"].inputs[0]
  )
  # reroute_006.Output -> reroute_011.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.006"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.011"].inputs[0]
  )
  # reroute_004.Output -> reroute_012.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.004"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.012"].inputs[0]
  )
  # reroute_015.Output -> reroute_013.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.015"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.013"].inputs[0]
  )
  # reroute_005.Output -> reroute_014.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.005"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.014"].inputs[0]
  )
  # group_input_003.Points -> reroute_015.Input
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.003"].outputs[0],
    sdf_points_to_mesh_1.nodes["Reroute.015"].inputs[0]
  )
  # reroute_005.Output -> sample_index_001.Index
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Reroute.005"].outputs[0],
    sdf_points_to_mesh_1.nodes["Sample Index.001"].inputs[2]
  )
  # group_input_007.Subdivisions -> group_016.Subdivisions
  sdf_points_to_mesh_1.links.new(
    sdf_points_to_mesh_1.nodes["Group Input.007"].outputs[7],
    sdf_points_to_mesh_1.nodes["Group.016"].inputs[3]
  )
  orientation_socket.default_value = 'Front'
  meshing_method_socket.default_value = 'Dense SDF'

  return sdf_points_to_mesh_1





#vertexcolor.alpha_threshold = 0.5
#vertexcolor.line_priority = 0
#vertexcolor.max_vertex_displacement = 0.0
#vertexcolor.metallic = 0.0
#vertexcolor.paint_active_slot = 0
#vertexcolor.paint_clone_slot = 0
#vertexcolor.pass_index = 0
#vertexcolor.refraction_depth = 0.0
#vertexcolor.roughness = 0.4000000059604645
#vertexcolor.show_transparent_back = True
#vertexcolor.specular_intensity = 0.5
#vertexcolor.use_backface_culling = False
#vertexcolor.use_backface_culling_lightprobe_volume = True
#vertexcolor.use_backface_culling_shadow = False
#vertexcolor.use_preview_world = False
#vertexcolor.use_raytrace_refraction = False
#vertexcolor.use_screen_refraction = False
#vertexcolor.use_sss_translucency = False
#vertexcolor.use_thickness_from_shadow = False
#vertexcolor.use_transparency_overlap = True
#vertexcolor.use_transparent_shadow = True
#vertexcolor.blend_method = 'HASHED'
#vertexcolor.displacement_method = 'BUMP'
#vertexcolor.preview_render_type = 'SPHERE'
#vertexcolor.surface_render_method = 'DITHERED'
#vertexcolor.thickness_mode = 'SPHERE'
#vertexcolor.volume_intersection_method = 'FAST'
#vertexcolor.specular_color = (1.0, 1.0, 1.0)
#vertexcolor.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
#vertexcolor.line_color = (0.0, 0.0, 0.0, 0.0)

#def get_vertex_color_material():
#  material_name = "VertexColor"
#  if material_name in bpy.data.materials:
#    return bpy.data.materials[material_name]
#  
#  vertexcolor = bpy.data.materials.new(name = "VertexColor")
#  if bpy.app.version < (5, 0, 0):
#    vertexcolor.use_nodes = True
#  
#  """Initialize Shader Nodetree node group"""
#  shader_nodetree = vertexcolor.node_tree
#
#  # Start with a clean node tree
#  for node in shader_nodetree.nodes:
#    shader_nodetree.nodes.remove(node)
#  shader_nodetree.color_tag = 'NONE'
#  shader_nodetree.description = ""
#  shader_nodetree.default_group_node_width = 140
#  # Initialize shader_nodetree nodes
#
#  # Node Material Output
#  material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
#  material_output.name = "Material Output"
#  material_output.show_options = True
#  material_output.is_active_output = True
#  material_output.target = 'ALL'
#  # Displacement
#  material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
#  # Thickness
#  material_output.inputs[3].default_value = 0.0
#
#  # Node Attribute
#  attribute = shader_nodetree.nodes.new("ShaderNodeAttribute")
#  attribute.name = "Attribute"
#  attribute.show_options = True
#  attribute.attribute_name = "Color"
#  attribute.attribute_type = 'GEOMETRY'
#  attribute.outputs[1].hide = True
#  attribute.outputs[2].hide = True
#  attribute.outputs[3].hide = True
#
#  # Node Attribute.001
#  attribute_001 = shader_nodetree.nodes.new("ShaderNodeAttribute")
#  attribute_001.name = "Attribute.001"
#  attribute_001.show_options = True
#  attribute_001.attribute_name = "Metallic"
#  attribute_001.attribute_type = 'GEOMETRY'
#  attribute_001.outputs[0].hide = True
#  attribute_001.outputs[1].hide = True
#  attribute_001.outputs[3].hide = True
#
#  # Node Attribute.002
#  attribute_002 = shader_nodetree.nodes.new("ShaderNodeAttribute")
#  attribute_002.name = "Attribute.002"
#  attribute_002.show_options = True
#  attribute_002.attribute_name = "Roughness"
#  attribute_002.attribute_type = 'GEOMETRY'
#  attribute_002.outputs[0].hide = True
#  attribute_002.outputs[1].hide = True
#  attribute_002.outputs[3].hide = True
#
#  # Node Attribute.003
#  attribute_003 = shader_nodetree.nodes.new("ShaderNodeAttribute")
#  attribute_003.name = "Attribute.003"
#  attribute_003.show_options = True
#  attribute_003.attribute_name = "Opacity"
#  attribute_003.attribute_type = 'GEOMETRY'
#  attribute_003.outputs[0].hide = True
#  attribute_003.outputs[1].hide = True
#  attribute_003.outputs[3].hide = True
#
#  # Node Principled BSDF
#  principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
#  principled_bsdf.name = "Principled BSDF"
#  principled_bsdf.show_options = True
#  principled_bsdf.distribution = 'MULTI_GGX'
#  principled_bsdf.subsurface_method = 'RANDOM_WALK'
#  # IOR
#  principled_bsdf.inputs[3].default_value = 1.5
#  # Normal
#  principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
#  # Diffuse Roughness
#  principled_bsdf.inputs[7].default_value = 0.0
#  # Subsurface Weight
#  principled_bsdf.inputs[8].default_value = 0.0
#  # Subsurface Radius
#  principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
#  # Subsurface Scale
#  principled_bsdf.inputs[10].default_value = 0.05000000074505806
#  # Subsurface Anisotropy
#  principled_bsdf.inputs[12].default_value = 0.0
#  # Specular IOR Level
#  principled_bsdf.inputs[13].default_value = 0.5
#  # Specular Tint
#  principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
#  # Anisotropic
#  principled_bsdf.inputs[15].default_value = 0.0
#  # Anisotropic Rotation
#  principled_bsdf.inputs[16].default_value = 0.0
#  # Tangent
#  principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
#  # Transmission Weight
#  principled_bsdf.inputs[18].default_value = 0.0
#  # Coat Weight
#  principled_bsdf.inputs[19].default_value = 0.0
#  # Coat Roughness
#  principled_bsdf.inputs[20].default_value = 0.029999999329447746
#  # Coat IOR
#  principled_bsdf.inputs[21].default_value = 1.5
#  # Coat Tint
#  principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
#  # Coat Normal
#  principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
#  # Sheen Weight
#  principled_bsdf.inputs[24].default_value = 0.0
#  # Sheen Roughness
#  principled_bsdf.inputs[25].default_value = 0.5
#  # Sheen Tint
#  principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
#  # Emission Color
#  principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
#  # Emission Strength
#  principled_bsdf.inputs[28].default_value = 0.0
#  # Thin Film Thickness
#  principled_bsdf.inputs[29].default_value = 0.0
#  # Thin Film IOR
#  principled_bsdf.inputs[30].default_value = 1.3300000429153442
#
#  # Node Brightness/Contrast
#  brightness_contrast = shader_nodetree.nodes.new("ShaderNodeBrightContrast")
#  brightness_contrast.name = "Brightness/Contrast"
#  brightness_contrast.show_options = True
#  # Bright
#  brightness_contrast.inputs[1].default_value = 0.0
#  # Contrast
#  brightness_contrast.inputs[2].default_value = 0.20000000298023224
#
#  # Node Float Curve
#  float_curve = shader_nodetree.nodes.new("ShaderNodeFloatCurve")
#  float_curve.name = "Float Curve"
#  float_curve.show_options = True
#  # Mapping settings
#  float_curve.mapping.extend = 'EXTRAPOLATED'
#  float_curve.mapping.tone = 'STANDARD'
#  float_curve.mapping.black_level = (0.0, 0.0, 0.0)
#  float_curve.mapping.white_level = (1.0, 1.0, 1.0)
#  float_curve.mapping.clip_min_x = 0.0
#  float_curve.mapping.clip_min_y = 0.0
#  float_curve.mapping.clip_max_x = 1.0
#  float_curve.mapping.clip_max_y = 1.0
#  float_curve.mapping.use_clip = True
#  # Curve 0
#  float_curve_curve_0 = float_curve.mapping.curves[0]
#  float_curve_curve_0_point_0 = float_curve_curve_0.points[0]
#  float_curve_curve_0_point_0.location = (0.0, 0.0)
#  float_curve_curve_0_point_0.handle_type = 'AUTO'
#  float_curve_curve_0_point_1 = float_curve_curve_0.points[1]
#  float_curve_curve_0_point_1.location = (0.2909089922904968, 0.10312504321336746)
#  float_curve_curve_0_point_1.handle_type = 'AUTO'
#  float_curve_curve_0_point_2 = float_curve_curve_0.points.new(0.6704545617103577, 0.8968756794929504)
#  float_curve_curve_0_point_2.handle_type = 'AUTO'
#  float_curve_curve_0_point_3 = float_curve_curve_0.points.new(1.0, 1.0)
#  float_curve_curve_0_point_3.handle_type = 'AUTO'
#  # Update curve after changes
#  float_curve.mapping.update()
#  float_curve.inputs[0].hide = True
#  # Factor
#  float_curve.inputs[0].default_value = 1.0
#
#  # Node Float Curve.001
#  float_curve_001 = shader_nodetree.nodes.new("ShaderNodeFloatCurve")
#  float_curve_001.name = "Float Curve.001"
#  float_curve_001.show_options = True
#  # Mapping settings
#  float_curve_001.mapping.extend = 'EXTRAPOLATED'
#  float_curve_001.mapping.tone = 'STANDARD'
#  float_curve_001.mapping.black_level = (0.0, 0.0, 0.0)
#  float_curve_001.mapping.white_level = (1.0, 1.0, 1.0)
#  float_curve_001.mapping.clip_min_x = 0.0
#  float_curve_001.mapping.clip_min_y = 0.0
#  float_curve_001.mapping.clip_max_x = 1.0
#  float_curve_001.mapping.clip_max_y = 1.0
#  float_curve_001.mapping.use_clip = True
#  # Curve 0
#  float_curve_001_curve_0 = float_curve_001.mapping.curves[0]
#  float_curve_001_curve_0_point_0 = float_curve_001_curve_0.points[0]
#  float_curve_001_curve_0_point_0.location = (0.0, 0.0)
#  float_curve_001_curve_0_point_0.handle_type = 'AUTO'
#  float_curve_001_curve_0_point_1 = float_curve_001_curve_0.points[1]
#  float_curve_001_curve_0_point_1.location = (0.3454543650150299, 0.10000000149011612)
#  float_curve_001_curve_0_point_1.handle_type = 'AUTO'
#  float_curve_001_curve_0_point_2 = float_curve_001_curve_0.points.new(0.6795456409454346, 0.7031254768371582)
#  float_curve_001_curve_0_point_2.handle_type = 'AUTO'
#  float_curve_001_curve_0_point_3 = float_curve_001_curve_0.points.new(1.0, 1.0)
#  float_curve_001_curve_0_point_3.handle_type = 'AUTO'
#  # Update curve after changes
#  float_curve_001.mapping.update()
#  # Factor
#  float_curve_001.inputs[0].default_value = 1.0
#
#  # Node Hue/Saturation/Value
#  hue_saturation_value = shader_nodetree.nodes.new("ShaderNodeHueSaturation")
#  hue_saturation_value.name = "Hue/Saturation/Value"
#  hue_saturation_value.show_options = True
#  # Hue
#  hue_saturation_value.inputs[0].default_value = 0.5
#  # Saturation
#  hue_saturation_value.inputs[1].default_value = 1.2000000476837158
#  # Value
#  hue_saturation_value.inputs[2].default_value = 1.0
#  # Fac
#  hue_saturation_value.inputs[3].default_value = 1.0
#
#  # Set locations
#  shader_nodetree.nodes["Material Output"].location = (-96.0218505859375, 115.58757781982422)
#  shader_nodetree.nodes["Attribute"].location = (-948.1951904296875, 202.04180908203125)
#  shader_nodetree.nodes["Attribute.001"].location = (-952.6959228515625, -159.60340881347656)
#  shader_nodetree.nodes["Attribute.002"].location = (-947.7696533203125, -492.9845275878906)
#  shader_nodetree.nodes["Attribute.003"].location = (-508.7360534667969, -144.01214599609375)
#  shader_nodetree.nodes["Principled BSDF"].location = (-303.44244384765625, 114.03108978271484)
#  shader_nodetree.nodes["Brightness/Contrast"].location = (-775.271728515625, 205.02523803710938)
#  shader_nodetree.nodes["Float Curve"].location = (-780.567626953125, 23.923927307128906)
#  shader_nodetree.nodes["Float Curve.001"].location = (-775.6277465820312, -289.9515075683594)
#  shader_nodetree.nodes["Hue/Saturation/Value"].location = (-546.5394287109375, 250.22039794921875)
#
#  # Set dimensions
#  shader_nodetree.nodes["Material Output"].width  = 140.0
#  shader_nodetree.nodes["Material Output"].height = 100.0
#
#  shader_nodetree.nodes["Attribute"].width  = 140.0
#  shader_nodetree.nodes["Attribute"].height = 100.0
#
#  shader_nodetree.nodes["Attribute.001"].width  = 140.0
#  shader_nodetree.nodes["Attribute.001"].height = 100.0
#
#  shader_nodetree.nodes["Attribute.002"].width  = 140.0
#  shader_nodetree.nodes["Attribute.002"].height = 100.0
#
#  shader_nodetree.nodes["Attribute.003"].width  = 140.0
#  shader_nodetree.nodes["Attribute.003"].height = 100.0
#
#  shader_nodetree.nodes["Principled BSDF"].width  = 151.86029052734375
#  shader_nodetree.nodes["Principled BSDF"].height = 100.0
#
#  shader_nodetree.nodes["Brightness/Contrast"].width  = 140.0
#  shader_nodetree.nodes["Brightness/Contrast"].height = 100.0
#
#  shader_nodetree.nodes["Float Curve"].width  = 240.0
#  shader_nodetree.nodes["Float Curve"].height = 100.0
#
#  shader_nodetree.nodes["Float Curve.001"].width  = 240.0
#  shader_nodetree.nodes["Float Curve.001"].height = 100.0
#
#  shader_nodetree.nodes["Hue/Saturation/Value"].width  = 150.0
#  shader_nodetree.nodes["Hue/Saturation/Value"].height = 100.0
#
#
#  # Initialize shader_nodetree links
#
#  # float_curve_001.Value -> principled_bsdf.Roughness
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Float Curve.001"].outputs[0],
#    shader_nodetree.nodes["Principled BSDF"].inputs[2]
#  )
#  # attribute_003.Factor -> principled_bsdf.Alpha
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Attribute.003"].outputs[2],
#    shader_nodetree.nodes["Principled BSDF"].inputs[4]
#  )
#  # attribute.Color -> brightness_contrast.Color
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Attribute"].outputs[0],
#    shader_nodetree.nodes["Brightness/Contrast"].inputs[0]
#  )
#  # attribute_001.Factor -> float_curve.Value
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Attribute.001"].outputs[2],
#    shader_nodetree.nodes["Float Curve"].inputs[1]
#  )
#  # float_curve.Value -> principled_bsdf.Metallic
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Float Curve"].outputs[0],
#    shader_nodetree.nodes["Principled BSDF"].inputs[1]
#  )
#  # attribute_002.Factor -> float_curve_001.Value
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Attribute.002"].outputs[2],
#    shader_nodetree.nodes["Float Curve.001"].inputs[1]
#  )
#  # principled_bsdf.BSDF -> material_output.Surface
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Principled BSDF"].outputs[0],
#    shader_nodetree.nodes["Material Output"].inputs[0]
#  )
#  # brightness_contrast.Color -> hue_saturation_value.Color
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Brightness/Contrast"].outputs[0],
#    shader_nodetree.nodes["Hue/Saturation/Value"].inputs[4]
#  )
#  # hue_saturation_value.Color -> principled_bsdf.Base Color
#  shader_nodetree.links.new(
#    shader_nodetree.nodes["Hue/Saturation/Value"].outputs[0],
#    shader_nodetree.nodes["Principled BSDF"].inputs[0]
#  )
#  return vertexcolor



#vertexshadedbsdf = bpy.data.materials.new(name = "VertexShadedBSDF")
#if bpy.app.version < (5, 0, 0):
#  vertexshadedbsdf.use_nodes = True


#vertexshadedbsdf.alpha_threshold = 0.5
#vertexshadedbsdf.line_priority = 0
#vertexshadedbsdf.max_vertex_displacement = 0.0
#vertexshadedbsdf.metallic = 0.0
#vertexshadedbsdf.paint_active_slot = 0
#vertexshadedbsdf.paint_clone_slot = 0
#vertexshadedbsdf.pass_index = 0
#vertexshadedbsdf.refraction_depth = 0.0
#vertexshadedbsdf.roughness = 0.4000000059604645
#vertexshadedbsdf.show_transparent_back = True
#vertexshadedbsdf.specular_intensity = 0.5
#vertexshadedbsdf.use_backface_culling = False
#vertexshadedbsdf.use_backface_culling_lightprobe_volume = True
#vertexshadedbsdf.use_backface_culling_shadow = False
#vertexshadedbsdf.use_preview_world = False
#vertexshadedbsdf.use_raytrace_refraction = False
#vertexshadedbsdf.use_screen_refraction = False
#vertexshadedbsdf.use_sss_translucency = False
#vertexshadedbsdf.use_thickness_from_shadow = False
#vertexshadedbsdf.use_transparency_overlap = True
#vertexshadedbsdf.use_transparent_shadow = True
#vertexshadedbsdf.blend_method = 'HASHED'
#vertexshadedbsdf.displacement_method = 'BUMP'
#vertexshadedbsdf.preview_render_type = 'SPHERE'
#vertexshadedbsdf.surface_render_method = 'DITHERED'
#vertexshadedbsdf.thickness_mode = 'SPHERE'
#vertexshadedbsdf.volume_intersection_method = 'FAST'
#vertexshadedbsdf.specular_color = (1.0, 1.0, 1.0)
#vertexshadedbsdf.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
#vertexshadedbsdf.line_color = (0.0, 0.0, 0.0, 0.0)

def set_vertex_bsdf_node_tree(material):
  """Initialize Vertex Shader BSDF Nodetree node group"""
  shader_nodetree = material.node_tree
  
  # Start with a clean node tree
  for node in shader_nodetree.nodes:
    shader_nodetree.nodes.remove(node)
  shader_nodetree.color_tag = 'NONE'
  shader_nodetree.description = ""
  shader_nodetree.default_group_node_width = 140
  # Initialize shader_nodetree nodes

  # Node Material Output
  material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
  material_output.name = "Material Output"
  material_output.show_options = True
  material_output.is_active_output = True
  material_output.target = 'ALL'
  # Displacement
  material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
  # Thickness
  material_output.inputs[3].default_value = 0.0

  # Node Attribute
  attribute = shader_nodetree.nodes.new("ShaderNodeAttribute")
  attribute.name = "Attribute"
  attribute.show_options = True
  attribute.attribute_name = "Color"
  attribute.attribute_type = 'GEOMETRY'
  attribute.outputs[1].hide = True
  attribute.outputs[2].hide = True
  attribute.outputs[3].hide = True

  # Node Attribute.001
  attribute_001 = shader_nodetree.nodes.new("ShaderNodeAttribute")
  attribute_001.name = "Attribute.001"
  attribute_001.show_options = True
  attribute_001.attribute_name = "Metallic"
  attribute_001.attribute_type = 'GEOMETRY'
  attribute_001.outputs[0].hide = True
  attribute_001.outputs[1].hide = True
  attribute_001.outputs[3].hide = True

  # Node Attribute.002
  attribute_002 = shader_nodetree.nodes.new("ShaderNodeAttribute")
  attribute_002.name = "Attribute.002"
  attribute_002.show_options = True
  attribute_002.attribute_name = "Roughness"
  attribute_002.attribute_type = 'GEOMETRY'
  attribute_002.outputs[0].hide = True
  attribute_002.outputs[1].hide = True
  attribute_002.outputs[3].hide = True

  # Node Attribute.003
  attribute_003 = shader_nodetree.nodes.new("ShaderNodeAttribute")
  attribute_003.name = "Attribute.003"
  attribute_003.show_options = True
  attribute_003.attribute_name = "Opacity"
  attribute_003.attribute_type = 'GEOMETRY'
  attribute_003.outputs[0].hide = True
  attribute_003.outputs[1].hide = True
  attribute_003.outputs[3].hide = True

  # Node Principled BSDF
  principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
  principled_bsdf.name = "Principled BSDF"
  principled_bsdf.show_options = True
  principled_bsdf.distribution = 'MULTI_GGX'
  principled_bsdf.subsurface_method = 'RANDOM_WALK'
  # IOR
  principled_bsdf.inputs[3].default_value = 1.5
  # Normal
  principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
  # Diffuse Roughness
  principled_bsdf.inputs[7].default_value = 0.0
  # Subsurface Weight
  principled_bsdf.inputs[8].default_value = 0.0
  # Subsurface Radius
  principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
  # Subsurface Scale
  principled_bsdf.inputs[10].default_value = 0.05000000074505806
  # Subsurface Anisotropy
  principled_bsdf.inputs[12].default_value = 0.0
  # Specular IOR Level
  principled_bsdf.inputs[13].default_value = 0.5
  # Specular Tint
  principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
  # Anisotropic
  principled_bsdf.inputs[15].default_value = 0.0
  # Anisotropic Rotation
  principled_bsdf.inputs[16].default_value = 0.0
  # Tangent
  principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
  # Transmission Weight
  principled_bsdf.inputs[18].default_value = 0.0
  # Coat Weight
  principled_bsdf.inputs[19].default_value = 0.0
  # Coat Roughness
  principled_bsdf.inputs[20].default_value = 0.029999999329447746
  # Coat IOR
  principled_bsdf.inputs[21].default_value = 1.5
  # Coat Tint
  principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
  # Coat Normal
  principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
  # Sheen Weight
  principled_bsdf.inputs[24].default_value = 0.0
  # Sheen Roughness
  principled_bsdf.inputs[25].default_value = 0.5
  # Sheen Tint
  principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
  # Emission Color
  principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
  # Emission Strength
  principled_bsdf.inputs[28].default_value = 0.0
  # Thin Film Thickness
  principled_bsdf.inputs[29].default_value = 0.0
  # Thin Film IOR
  principled_bsdf.inputs[30].default_value = 1.3300000429153442

  # Node Brightness/Contrast
  brightness_contrast = shader_nodetree.nodes.new("ShaderNodeBrightContrast")
  brightness_contrast.name = "Brightness/Contrast"
  brightness_contrast.show_options = True
  # Bright
  brightness_contrast.inputs[1].default_value = 0.0
  # Contrast
  brightness_contrast.inputs[2].default_value = 0.20000000298023224

  # Node Float Curve
  float_curve = shader_nodetree.nodes.new("ShaderNodeFloatCurve")
  float_curve.name = "Float Curve"
  float_curve.show_options = True
  # Mapping settings
  float_curve.mapping.extend = 'EXTRAPOLATED'
  float_curve.mapping.tone = 'STANDARD'
  float_curve.mapping.black_level = (0.0, 0.0, 0.0)
  float_curve.mapping.white_level = (1.0, 1.0, 1.0)
  float_curve.mapping.clip_min_x = 0.0
  float_curve.mapping.clip_min_y = 0.0
  float_curve.mapping.clip_max_x = 1.0
  float_curve.mapping.clip_max_y = 1.0
  float_curve.mapping.use_clip = True
  # Curve 0
  float_curve_curve_0 = float_curve.mapping.curves[0]
  float_curve_curve_0_point_0 = float_curve_curve_0.points[0]
  float_curve_curve_0_point_0.location = (0.0, 0.0)
  float_curve_curve_0_point_0.handle_type = 'AUTO'
  float_curve_curve_0_point_1 = float_curve_curve_0.points[1]
  float_curve_curve_0_point_1.location = (0.2909089922904968, 0.10312504321336746)
  float_curve_curve_0_point_1.handle_type = 'AUTO'
  float_curve_curve_0_point_2 = float_curve_curve_0.points.new(0.6704545617103577, 0.8968756794929504)
  float_curve_curve_0_point_2.handle_type = 'AUTO'
  float_curve_curve_0_point_3 = float_curve_curve_0.points.new(1.0, 1.0)
  float_curve_curve_0_point_3.handle_type = 'AUTO'
  # Update curve after changes
  float_curve.mapping.update()
  float_curve.inputs[0].hide = True
  # Factor
  float_curve.inputs[0].default_value = 1.0

  # Node Float Curve.001
  float_curve_001 = shader_nodetree.nodes.new("ShaderNodeFloatCurve")
  float_curve_001.name = "Float Curve.001"
  float_curve_001.show_options = True
  # Mapping settings
  float_curve_001.mapping.extend = 'EXTRAPOLATED'
  float_curve_001.mapping.tone = 'STANDARD'
  float_curve_001.mapping.black_level = (0.0, 0.0, 0.0)
  float_curve_001.mapping.white_level = (1.0, 1.0, 1.0)
  float_curve_001.mapping.clip_min_x = 0.0
  float_curve_001.mapping.clip_min_y = 0.0
  float_curve_001.mapping.clip_max_x = 1.0
  float_curve_001.mapping.clip_max_y = 1.0
  float_curve_001.mapping.use_clip = True
  # Curve 0
  float_curve_001_curve_0 = float_curve_001.mapping.curves[0]
  float_curve_001_curve_0_point_0 = float_curve_001_curve_0.points[0]
  float_curve_001_curve_0_point_0.location = (0.0, 0.0)
  float_curve_001_curve_0_point_0.handle_type = 'AUTO'
  float_curve_001_curve_0_point_1 = float_curve_001_curve_0.points[1]
  float_curve_001_curve_0_point_1.location = (0.670454204082489, 0.328125)
  float_curve_001_curve_0_point_1.handle_type = 'AUTO'
  float_curve_001_curve_0_point_2 = float_curve_001_curve_0.points.new(1.0, 1.0)
  float_curve_001_curve_0_point_2.handle_type = 'AUTO'
  # Update curve after changes
  float_curve_001.mapping.update()
  # Factor
  float_curve_001.inputs[0].default_value = 1.0

  # Node Hue/Saturation/Value
  hue_saturation_value = shader_nodetree.nodes.new("ShaderNodeHueSaturation")
  hue_saturation_value.name = "Hue/Saturation/Value"
  hue_saturation_value.show_options = True
  # Hue
  hue_saturation_value.inputs[0].default_value = 0.5
  # Saturation
  hue_saturation_value.inputs[1].default_value = 1.2000000476837158
  # Value
  hue_saturation_value.inputs[2].default_value = 1.0
  # Fac
  hue_saturation_value.inputs[3].default_value = 1.0

  # Set locations
  shader_nodetree.nodes["Material Output"].location = (-96.0218505859375, 115.58757781982422)
  shader_nodetree.nodes["Attribute"].location = (-948.1951904296875, 202.04180908203125)
  shader_nodetree.nodes["Attribute.001"].location = (-952.6959228515625, -159.60340881347656)
  shader_nodetree.nodes["Attribute.002"].location = (-947.7696533203125, -492.9845275878906)
  shader_nodetree.nodes["Attribute.003"].location = (-508.7360534667969, -144.01214599609375)
  shader_nodetree.nodes["Principled BSDF"].location = (-303.44244384765625, 114.03108978271484)
  shader_nodetree.nodes["Brightness/Contrast"].location = (-775.271728515625, 205.02523803710938)
  shader_nodetree.nodes["Float Curve"].location = (-780.567626953125, 23.923927307128906)
  shader_nodetree.nodes["Float Curve.001"].location = (-775.6277465820312, -289.9515075683594)
  shader_nodetree.nodes["Hue/Saturation/Value"].location = (-546.5394287109375, 250.22039794921875)

  # Set dimensions
  shader_nodetree.nodes["Material Output"].width  = 140.0
  shader_nodetree.nodes["Material Output"].height = 100.0

  shader_nodetree.nodes["Attribute"].width  = 140.0
  shader_nodetree.nodes["Attribute"].height = 100.0

  shader_nodetree.nodes["Attribute.001"].width  = 140.0
  shader_nodetree.nodes["Attribute.001"].height = 100.0

  shader_nodetree.nodes["Attribute.002"].width  = 140.0
  shader_nodetree.nodes["Attribute.002"].height = 100.0

  shader_nodetree.nodes["Attribute.003"].width  = 140.0
  shader_nodetree.nodes["Attribute.003"].height = 100.0

  shader_nodetree.nodes["Principled BSDF"].width  = 151.86029052734375
  shader_nodetree.nodes["Principled BSDF"].height = 100.0

  shader_nodetree.nodes["Brightness/Contrast"].width  = 140.0
  shader_nodetree.nodes["Brightness/Contrast"].height = 100.0

  shader_nodetree.nodes["Float Curve"].width  = 240.0
  shader_nodetree.nodes["Float Curve"].height = 100.0

  shader_nodetree.nodes["Float Curve.001"].width  = 240.0
  shader_nodetree.nodes["Float Curve.001"].height = 100.0

  shader_nodetree.nodes["Hue/Saturation/Value"].width  = 150.0
  shader_nodetree.nodes["Hue/Saturation/Value"].height = 100.0


  # Initialize shader_nodetree links

  # float_curve_001.Value -> principled_bsdf.Roughness
  shader_nodetree.links.new(
    shader_nodetree.nodes["Float Curve.001"].outputs[0],
    shader_nodetree.nodes["Principled BSDF"].inputs[2]
  )
  # attribute_003.Factor -> principled_bsdf.Alpha
  shader_nodetree.links.new(
    shader_nodetree.nodes["Attribute.003"].outputs[2],
    shader_nodetree.nodes["Principled BSDF"].inputs[4]
  )
  # attribute.Color -> brightness_contrast.Color
  shader_nodetree.links.new(
    shader_nodetree.nodes["Attribute"].outputs[0],
    shader_nodetree.nodes["Brightness/Contrast"].inputs[0]
  )
  # attribute_001.Factor -> float_curve.Value
  shader_nodetree.links.new(
    shader_nodetree.nodes["Attribute.001"].outputs[2],
    shader_nodetree.nodes["Float Curve"].inputs[1]
  )
  # float_curve.Value -> principled_bsdf.Metallic
  shader_nodetree.links.new(
    shader_nodetree.nodes["Float Curve"].outputs[0],
    shader_nodetree.nodes["Principled BSDF"].inputs[1]
  )
  # attribute_002.Factor -> float_curve_001.Value
  shader_nodetree.links.new(
    shader_nodetree.nodes["Attribute.002"].outputs[2],
    shader_nodetree.nodes["Float Curve.001"].inputs[1]
  )
  # principled_bsdf.BSDF -> material_output.Surface
  shader_nodetree.links.new(
    shader_nodetree.nodes["Principled BSDF"].outputs[0],
    shader_nodetree.nodes["Material Output"].inputs[0]
  )
  # brightness_contrast.Color -> hue_saturation_value.Color
  shader_nodetree.links.new(
    shader_nodetree.nodes["Brightness/Contrast"].outputs[0],
    shader_nodetree.nodes["Hue/Saturation/Value"].inputs[4]
  )
  # hue_saturation_value.Color -> principled_bsdf.Base Color
  shader_nodetree.links.new(
    shader_nodetree.nodes["Hue/Saturation/Value"].outputs[0],
    shader_nodetree.nodes["Principled BSDF"].inputs[0]
  )
  return shader_nodetree


def get_vertex_bsdf_material():
  material_name = "VertexShadedBSDF"
  
  # Check if already created
  if material_name in bpy.data.materials:
    return bpy.data.materials[material_name]
  
  # Create new Vertex Shader BSDF Material
  material = bpy.data.materials.new(name = material_name)
  if bpy.app.version < (5, 0, 0):
      material.use_nodes = True
  
  material.alpha_threshold = 0.5
  material.line_priority = 0
  material.max_vertex_displacement = 0.0
  material.metallic = 0.0
  material.paint_active_slot = 0
  material.paint_clone_slot = 0
  material.pass_index = 0
  material.refraction_depth = 0.0
  material.roughness = 0.4000000059604645
  material.show_transparent_back = True
  material.specular_intensity = 0.5
  material.use_backface_culling = False
  material.use_backface_culling_lightprobe_volume = True
  material.use_backface_culling_shadow = False
  material.use_preview_world = False
  material.use_raytrace_refraction = False
  material.use_screen_refraction = False
  material.use_sss_translucency = False
  material.use_thickness_from_shadow = False
  material.use_transparency_overlap = True
  material.use_transparent_shadow = True
  material.blend_method = 'HASHED'
  material.displacement_method = 'BUMP'
  material.preview_render_type = 'SPHERE'
  material.surface_render_method = 'DITHERED'
  material.thickness_mode = 'SPHERE'
  material.volume_intersection_method = 'FAST'
  material.specular_color = (1.0, 1.0, 1.0)
  material.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
  material.line_color = (0.0, 0.0, 0.0, 0.0)
  
  set_vertex_bsdf_node_tree(material)
  return material


if __name__ == "__main__":
  get_smooth_geometry_node_group()
  get_nearest_position_group()
  get_carve_sdf_node_group()
  get_nearest_point_node_group()
  get_normal_offset_node_group()
  get_offset_nearst_node_group()
  get_points_to_mesh_node_group()
  get_points_to_shell_node_group()
  get_sdf_points_to_mesh_node_group()
  get_vertex_bsdf_material()
