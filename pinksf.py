import bpy

# Создание сферы
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))

# Выбор созданной сферы
sphere = bpy.context.object

# Создание нового материала
material = bpy.data.materials.new(name="SphereMaterial")

# Присваивание материала сфере
if sphere.data.materials:
    sphere.data.materials[0] = material
else:
    sphere.data.materials.append(material)

# Настройка материала
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# Удаление стандартных нодов
for node in nodes:
    nodes.remove(node)

# Создание нода Diffuse BSDF
diffuse_node = nodes.new(type='ShaderNodeBsdfDiffuse')
diffuse_node.inputs['Color'].default_value = (0.8, 0.2, 0.2, 1)

# Создание нода Output
output_node = nodes.new(type='ShaderNodeOutputMaterial')

# Создание нода Material Output
material_output_node = nodes.new(type='ShaderNodeOutputMaterial')
material_output_node.location = (200, 0)

# Создание нода Mix Shader
mix_shader_node = nodes.new(type='ShaderNodeMixShader')
mix_shader_node.location = (400, 0)

# Создание нода Glossy BSDF
glossy_node = nodes.new(type='ShaderNodeBsdfGlossy')
glossy_node.location = (200, 200)

# Подключение нодов
links.new(diffuse_node.outputs['BSDF'], mix_shader_node.inputs[1])
links.new(glossy_node.outputs['BSDF'], mix_shader_node.inputs[2])
links.new(mix_shader_node.outputs['Shader'], material_output_node.inputs['Surface'])
links.new(material_output_node.outputs['Surface'], output_node.inputs['Surface'])

# Настройка параметров Mix Shader
mix_shader_node.inputs['Fac'].default_value = 0.5

# Вывод информации о созданном материале
print("Material created and assigned to the sphere.")