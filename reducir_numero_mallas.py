"""
Reduce el numero de caras (mallas) del objeto 'galbot' con Decimate.
No requiere que el mesh este separado en partes.

COMO USARLO:
1. Pestana "Scripting" > Open > selecciona este archivo.
2. Ajusta CONFIG.
3. Run Script (Alt+P).
4. Revisa el conteo de caras antes/despues en la consola.
"""

import bpy
import math

# ---------------- CONFIG ----------------
target_name = "galbot"
mode = 'PLANAR'        # 'PLANAR' (mejor para paneles planos tipo CAD/robot) o 'COLLAPSE' (general)
ratio = 0.2             # solo aplica si mode == 'COLLAPSE'. 0.2 = deja 20% de las caras
angle_limit_deg = 5     # solo aplica si mode == 'PLANAR'. Mas alto = mas reduccion, menos detalle
# -----------------------------------------

obj = bpy.data.objects.get(target_name)
if obj is None:
    raise Exception(f"No se encontro el objeto '{target_name}'.")

faces_before = len(obj.data.polygons)
print(f"\nCaras antes: {faces_before}")

mod = obj.modifiers.new(name="Decimate", type='DECIMATE')

if mode == 'PLANAR':
    mod.decimate_type = 'DISSOLVE'  # 'DISSOLVE' es el nombre interno del modo "Planar" en Blender
    mod.angle_limit = math.radians(angle_limit_deg)
else:
    mod.decimate_type = 'COLLAPSE'
    mod.ratio = ratio

bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_apply(modifier=mod.name)

faces_after = len(obj.data.polygons)
print(f"Caras despues: {faces_after}  ({faces_after/faces_before*100:.1f}% del original)")
