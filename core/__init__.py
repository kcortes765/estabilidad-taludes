"""
Paquete core para análisis de estabilidad de taludes.

Contiene:
- Funciones geométricas fundamentales
- Métodos de análisis (Fellenius, Bishop)
- Algoritmos de cálculo y discretización
"""

# Importar funciones geométricas
from .geometry import (
    calcular_y_circulo, interpolar_terreno, calcular_angulo_alpha,
    calcular_longitud_arco, calcular_altura_dovela, calcular_peso_dovela,
    calcular_presion_poros, crear_dovelas, validar_geometria_circulo,
    crear_perfil_simple, crear_nivel_freatico_horizontal
)

# Importar método de Fellenius
from .fellenius import (
    analizar_fellenius,
    ResultadoFellenius,
    generar_reporte_fellenius,
    comparar_con_factor_teorico,
    fellenius_talud_homogeneo,
    fellenius_con_nivel_freatico
)

# Importar funciones del módulo bishop
from .bishop import (
    analizar_bishop,
    ResultadoBishop,
    calcular_m_alpha,
    calcular_fuerza_resistente_bishop,
    calcular_fuerza_actuante_bishop,
    iteracion_bishop,
    generar_reporte_bishop,
    bishop_talud_homogeneo,
    bishop_con_nivel_freatico,
    comparar_bishop_fellenius,
    generar_reporte_comparacion
)

# Lista de todas las funciones y clases exportadas
__all__ = [
    # Geometría
    'crear_perfil_simple',
    'crear_nivel_freatico_horizontal',
    'crear_dovelas',
    'calcular_presion_poros',
    'validar_geometria_circulo',
    
    # Fellenius
    'analizar_fellenius',
    'ResultadoFellenius',
    'generar_reporte_fellenius',
    'comparar_con_factor_teorico',
    'fellenius_talud_homogeneo',
    'fellenius_con_nivel_freatico',
    
    # Bishop
    'analizar_bishop',
    'ResultadoBishop',
    'calcular_m_alpha',
    'calcular_fuerza_resistente_bishop',
    'calcular_fuerza_actuante_bishop',
    'iteracion_bishop',
    'generar_reporte_bishop',
    'bishop_talud_homogeneo',
    'bishop_con_nivel_freatico',
    'comparar_bishop_fellenius',
    'generar_reporte_comparacion'
]
