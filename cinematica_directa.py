import numpy as np

def matriz_dh(theta, d, a, alpha):
    """
    Calcula la matriz de transformación homogénea para un eslabón 
    usando los parámetros de Denavit-Hartenberg.
    """
    # Convertir ángulos a radianes si vienen en grados
    # (En este caso asumimos que ya entran en radianes)
    
    T = np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha),  np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta),  np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0,              np.sin(alpha),                 np.cos(alpha),                d],
        [0,              0,                             0,                            1]
    ])
    return T

def cinematica_directa(articulaciones, tabla_dh):
    """
    Calcula la matriz de transformación final multiplicando las matrices de cada eslabón.
    """
    # Matriz identidad para empezar la multiplicación
    T_total = np.eye(4)
    
    for i, parametros in enumerate(tabla_dh):
        # En robots rotacionales (revoluta), theta es la variable articular
        # Sumamos el valor actual de la articulación al offset theta_dh
        theta = articulaciones[i] + parametros['theta']
        d = parametros['d']
        a = parametros['a']
        alpha = parametros['alpha']
        
        # Calcular matriz del eslabón actual y multiplicar
        T_i = matriz_dh(theta, d, a, alpha)
        T_total = np.dot(T_total, T_i)
        
    return T_total

# --- CONFIGURACIÓN DEL ROBOT (Ejemplo: Robot de 3 eslabones) ---
# Longitudes de los eslabones (en metros o la unidad que prefieras)
l1, l2, l3 = 0.5, 0.4, 0.3

# Parámetros DH estáticos: {'theta': offset, 'd': distancia_z, 'a': longitud_x, 'alpha': torsion_x}
# Nota: Los ángulos alpha deben estar en radianes (ej. np.pi/2)
tabla_dh_config = [
    {'theta': 0, 'd': l1, 'a': 0,  'alpha': np.pi/2},  # Eslabón 1
    {'theta': 0, 'd': 0,  'a': l2, 'alpha': 0},        # Eslabón 2
    {'theta': 0, 'd': 0,  'a': l3, 'alpha': 0}         # Eslabón 3
]

# --- PRUEBA DEL ALGORITMO ---
# Definimos los ángulos actuales de las articulaciones (en radianes)
# Ejemplo: Q1 = 45°, Q2 = 30°, Q3 = 0°
q1 = np.radians(45)
q2 = np.radians(30)
q3 = np.radians(0)

angulos_actuales = [q1, q2, q3]

# Calcular la matriz de transformación homogénea final
T_final = cinematica_directa(angulos_actuales, tabla_dh_config)

# Extraer posición (X, Y, Z) de la última columna
posicion = T_final[:3, 3]
# Extraer la matriz de rotación (orientación)
rotacion = T_final[:3, :3]

print("=== MATRIZ DE TRANSFORMACIÓN HOMOGÉNEA (T) ===")
print(np.round(T_final, 4))
print("\n=== POSICIÓN DEL EFECTOR FINAL ===")
print(f"X: {posicion[0]:.4f}")
print(f"Y: {posicion[1]:.4f}")
print(f"Z: {posicion[2]:.4f}")
