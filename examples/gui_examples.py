"""
Casos de ejemplo para GUI - Compatibilidad con sistema ultra-completo

Estos casos están optimizados para el nuevo sistema de límites y validaciones
"""

from data.models import CirculoFalla

# Casos de ejemplo optimizados
casos_ejemplo = [
    {
        'nombre': 'Talud Simple Optimizado',
        'descripcion': 'Caso básico con geometría validada',
        'perfil_terreno': [
            (0, 10),
            (10, 10),
            (20, 0),
            (40, 0)
        ],
        'circulo': CirculoFalla(15, 12, 18),
        'cohesion': 25.0,
        'angulo_friccion': 30.0,
        'peso_especifico': 19.0,
        'nivel_freatico': 0.0,
        'esperado_fs': 1.8
    },
    
    {
        'nombre': 'Talud Empinado',
        'descripcion': 'Talud con pendiente empinada',
        'perfil_terreno': [
            (0, 15),
            (8, 15),
            (18, 0),
            (35, 0)
        ],
        'circulo': CirculoFalla(12, 18, 22),
        'cohesion': 20.0,
        'angulo_friccion': 25.0,
        'peso_especifico': 18.5,
        'nivel_freatico': 0.0,
        'esperado_fs': 1.4
    },
    
    {
        'nombre': 'Talud con Agua',
        'descripcion': 'Talud con nivel freático',
        'perfil_terreno': [
            (0, 12),
            (12, 12),
            (25, 0),
            (40, 0)
        ],
        'circulo': CirculoFalla(18, 15, 20),
        'cohesion': 30.0,
        'angulo_friccion': 28.0,
        'peso_especifico': 20.0,
        'nivel_freatico': 5.0,
        'esperado_fs': 1.6
    },
    
    {
        'nombre': 'Talud Crítico',
        'descripcion': 'Caso límite de estabilidad',
        'perfil_terreno': [
            (0, 8),
            (6, 8),
            (16, 0),
            (30, 0)
        ],
        'circulo': CirculoFalla(10, 12, 16),
        'cohesion': 15.0,
        'angulo_friccion': 20.0,
        'peso_especifico': 17.5,
        'nivel_freatico': 0.0,
        'esperado_fs': 1.1
    }
]
