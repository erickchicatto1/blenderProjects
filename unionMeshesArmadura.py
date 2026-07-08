import bpy

arm = bpy.data.objects["Armature"]
root = bpy.data.objects["Sal_Textured_Root"]

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

meshes = [ob for ob in root.children_recursive if ob.type == 'MESH']

# 1. Congela la posición mundial de cada malla y suéltala de los empties
for ob in meshes:
    mw = ob.matrix_world.copy()
    ob.parent = None
    ob.matrix_world = mw   # conserva su posición visual exacta
    ob.select_set(True)

# 2. Aplica transformaciones (escala/rotación heredadas quedan "horneadas")
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

# 3. Emparenta al armature con automatic weights
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

print(f"Listo: {len(meshes)} mallas")
