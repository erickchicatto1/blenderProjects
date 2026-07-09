"""
Script para animar huesos automáticamente en Blender (Pose Mode).

CÓMO USARLO:
1. Abre tu archivo .blend en Blender.
2. Ve a la pestaña "Scripting" (arriba, junto a Layout, Modeling, etc.)
3. Crea un nuevo archivo de texto (New) y pega este código.
4. Ajusta los valores en la sección "CONFIGURACIÓN" más abajo.
5. Presiona el botón ▶ (Run Script) o Alt+P con el cursor en el editor de texto.
"""

import bpy
import math

# ============================================================
# CONFIGURACIÓN - Ajusta esto según tu rig
# ============================================================

NOMBRE_ARMATURE = "BasicBot"  # nombre del objeto Armature en el Outliner

# Diccionario: nombre del hueso -> lista de (frame, (rot_x, rot_y, rot_z) en grados)
ANIMACION_HUESOS = {
    "Bone.001": [
        (1,  (0, 0, 0)),
        (25, (45, 0, 0)),
        (50, (0, 0, 0)),
    ],
    "Bone.004": [
        (1,  (0, 0, 0)),
        (25, (-45, 0, 0)),
        (50, (0, 0, 0)),
    ],
    "Bone.005": [
        (1,  (0, 0, 0)),
        (25, (30, 0, 0)),
        (50, (0, 0, 0)),
    ],
    # Agrega más huesos aquí siguiendo el mismo patrón:
    # "Bone.00X": [
    #     (frame, (rot_x, rot_y, rot_z)),
    #     ...
    # ],
}

# ============================================================
# EJECUCIÓN - No necesitas tocar esto
# ============================================================

def animar():
    armature = bpy.data.objects.get(NOMBRE_ARMATURE)
    if armature is None:
        print(f"ERROR: no se encontró el objeto '{NOMBRE_ARMATURE}'")
        return

    # Activar el armature y entrar en Pose Mode
    bpy.context.view_layer.objects.active = armature
    if bpy.context.object.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')

    for nombre_hueso, keyframes in ANIMACION_HUESOS.items():
        bone = armature.pose.bones.get(nombre_hueso)
        if bone is None:
            print(f"AVISO: hueso '{nombre_hueso}' no encontrado, se salta.")
            continue

        bone.rotation_mode = 'XYZ'

        for frame, (rx, ry, rz) in keyframes:
            bpy.context.scene.frame_set(frame)
            bone.rotation_euler = (
                math.radians(rx),
                math.radians(ry),
                math.radians(rz),
            )
            bone.keyframe_insert(data_path="rotation_euler", frame=frame)

    # Regresar al frame 1 al terminar
    bpy.context.scene.frame_set(1)
    print("Animación de huesos creada correctamente.")


animar()
