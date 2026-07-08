"""Limpieza: borra rigs viejos (Sal_Rig*) y sus restos antes de re-correr
el script de rig+caminata. Correr UNA vez en Scripting (Alt+P)."""
import bpy

if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

# 1) Borrar los armatures viejos
removed = []
for obj in list(bpy.data.objects):
    if obj.name.startswith("Sal_Rig"):
        removed.append(obj.name)
        bpy.data.objects.remove(obj, do_unlink=True)

# 2) Quitar modificadores Armature huerfanos y vertex groups del rig viejo
BONE_PREFIXES = ("UpperLeg", "LowerLeg", "Foot", "Toe", "Seg")
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    for mod in list(obj.modifiers):
        if mod.type == 'ARMATURE' and (
            mod.object is None or mod.object.name.startswith("Sal_Rig")
        ):
            obj.modifiers.remove(mod)
    for vg in list(obj.vertex_groups):
        if vg.name.startswith(BONE_PREFIXES):
            obj.vertex_groups.remove(vg)

# 3) Purgar datablocks sin usuarios (armatures y acciones viejas)
for arm in list(bpy.data.armatures):
    if arm.users == 0:
        bpy.data.armatures.remove(arm)
for act in list(bpy.data.actions):
    if act.users == 0:
        bpy.data.actions.remove(act)

print(f"Limpieza lista. Rigs borrados: {removed or 'ninguno'}")
print("Guarda (Ctrl+S) y luego corre sal_rig_walk_fixed.py")
