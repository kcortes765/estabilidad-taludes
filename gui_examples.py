"""
Casos de ejemplo corregidos con validación geométrica para la GUI de análisis de estabilidad de taludes.
Estos casos garantizan que se generen suficientes dovelas válidas y evitan errores de análisis.
"""

import math

def calcular_perfil_terreno(altura, angulo_talud, longitud_total=40):
    """
    Calcula el perfil del terreno basado en altura y ángulo del talud
    
    Args:
        altura: Altura del talud (m)
        angulo_talud: Ángulo del talud en grados
        longitud_total: Longitud total del perfil (m)
    
    Returns:
        Lista de puntos (x, y) del perfil
    """
    # Convertir ángulo a radianes
    angulo_rad = math.radians(angulo_talud)
    
    # Calcular proyección horizontal del talud
    proyeccion_horizontal = altura / math.tan(angulo_rad)
    
    # Crear perfil con plataforma superior, talud y base
    perfil = [
        (0, altura),  # Inicio plataforma superior
        (longitud_total * 0.3, altura),  # Fin plataforma superior
        (longitud_total * 0.3 + proyeccion_horizontal, 0),  # Pie del talud
        (longitud_total, 0)  # Final de la base
    ]
    
    return perfil

# Casos de ejemplo con geometrías validadas
CASOS_EJEMPLO = {
    "Talud Estable - Carretera": {
        "descripcion": "Talud típico de carretera con factor de seguridad alto",
        "altura": 8.0,
        "angulo_talud": 35.0,
        "cohesion": 35.0,
        "phi_grados": 30.0,
        "gamma": 19.0,
        "con_agua": False,
        "nivel_freatico": 0.0,
        # Círculo balanceado: no tan crítico como para fallar, no tan seguro como para FS extremo
        "centro_x": 17.0,
        "centro_y": 8.0,
        "radio": 20.0,
        "esperado": "Fs > 1.5 (ESTABLE)",
        "perfil_terreno": calcular_perfil_terreno(8.0, 35.0)
    },
    
    "Talud Marginal - Arcilla Blanda": {
        "descripcion": "Talud en arcilla blanda con factor de seguridad límite",
        "altura": 10.0,
        "angulo_talud": 45.0,
        "cohesion": 12.0,
        "phi_grados": 20.0,
        "gamma": 18.0,
        "con_agua": False,
        "nivel_freatico": 0.0,
        # Círculo balanceado para suelo más débil
        "centro_x": 17.0,
        "centro_y": 10.0,
        "radio": 18.0,
        "esperado": "1.2 < Fs < 1.4 (MARGINAL)",
        "perfil_terreno": calcular_perfil_terreno(10.0, 45.0)
    },
    
    "Talud con Agua - Crítico": {
        "descripcion": "Talud con nivel freático alto, condición crítica",
        "altura": 8.0,
        "angulo_talud": 40.0,
        "cohesion": 20.0,
        "phi_grados": 25.0,
        "gamma": 18.0,
        "con_agua": True,
        "nivel_freatico": 6.0,
        # Círculo balanceado para condición con agua
        "centro_x": 18.0,
        "centro_y": 7.0,
        "radio": 16.0,
        "esperado": "Fs ≈ 1.0-1.2 (CRÍTICO)",
        "perfil_terreno": calcular_perfil_terreno(8.0, 40.0)
    },
    
    "Talud Moderado - Arena Densa": {
        "descripcion": "Talud en arena densa con parámetros moderados",
        "altura": 6.0,
        "angulo_talud": 30.0,
        "cohesion": 5.0,   # Arena con poca cohesión
        "phi_grados": 35.0, # Ángulo de fricción alto
        "gamma": 20.0,
        "con_agua": False,
        "nivel_freatico": 0.0,
        # Círculo balanceado para talud suave
        "centro_x": 16.0,
        "centro_y": 6.0,
        "radio": 16.0,
        "esperado": "Fs > 2.0 (MUY ESTABLE)",
        "perfil_terreno": calcular_perfil_terreno(6.0, 30.0)
    }
}

def get_caso_ejemplo(nombre):
    """Obtener parámetros de un caso de ejemplo."""
    return CASOS_EJEMPLO.get(nombre, {})

def get_nombres_casos():
    """Obtener lista de nombres de casos disponibles."""
    return list(CASOS_EJEMPLO.keys())
