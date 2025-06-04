"""
Módulo data para análisis de estabilidad de taludes.

Contiene:
- Modelos de datos (Estrato, Dovela, CirculoFalla)
- Validaciones críticas del sistema
- Constantes y configuraciones
"""

from .models import (
    Estrato, Dovela, CirculoFalla,
    crear_estrato_homogeneo, crear_circulo_simple,
    GRAVEDAD, DENSIDAD_AGUA
)

from .validation import (
    ResultadoValidacion, ValidacionError,
    validar_parametros_geotecnicos, validar_geometria_circulo_avanzada,
    validar_dovela_critica, validar_conjunto_dovelas,
    validar_convergencia_bishop, validar_factor_seguridad,
    validar_perfil_terreno, validar_entrada_completa,
    verificar_consistencia_unidades, lanzar_si_invalido, validar_y_reportar
)

from .constants import (
    TOLERANCIA_CONVERGENCIA_BISHOP,
    MAX_ITERACIONES_BISHOP,
    MIN_FACTOR_SEGURIDAD,
    MAX_FACTOR_SEGURIDAD,
    FACTOR_SEGURIDAD_CRITICO,
    FACTOR_SEGURIDAD_MARGINAL,
    FACTOR_SEGURIDAD_SEGURO,
    CLASIFICACIONES_ESTABILIDAD,
    FACTORES_SEGURIDAD_TIPICOS,
    PARAMETROS_DEFAULT,
    GAMMA_AGUA
)

__all__ = [
    # Modelos
    'Estrato', 'Dovela', 'CirculoFalla',
    'crear_estrato_homogeneo', 'crear_circulo_simple',
    
    # Constantes
    'GRAVEDAD', 'DENSIDAD_AGUA',
    'TOLERANCIA_CONVERGENCIA_BISHOP', 'MAX_ITERACIONES_BISHOP',
    'MIN_FACTOR_SEGURIDAD', 'MAX_FACTOR_SEGURIDAD',
    'FACTOR_SEGURIDAD_CRITICO', 'FACTOR_SEGURIDAD_MARGINAL', 'FACTOR_SEGURIDAD_SEGURO',
    'CLASIFICACIONES_ESTABILIDAD', 'FACTORES_SEGURIDAD_TIPICOS',
    'PARAMETROS_DEFAULT', 'GAMMA_AGUA',
    
    # Validaciones
    'ResultadoValidacion', 'ValidacionError',
    'validar_parametros_geotecnicos', 'validar_geometria_circulo_avanzada',
    'validar_dovela_critica', 'validar_conjunto_dovelas',
    'validar_convergencia_bishop', 'validar_factor_seguridad',
    'validar_perfil_terreno', 'validar_entrada_completa',
    'verificar_consistencia_unidades', 'lanzar_si_invalido', 'validar_y_reportar'
]
