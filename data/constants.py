"""
Constantes utilizadas en el análisis de estabilidad de taludes.

Este módulo define todas las constantes numéricas, tolerancias y límites
utilizados en los cálculos de estabilidad.
"""

# Tolerancias de convergencia
TOLERANCIA_CONVERGENCIA_BISHOP = 0.001  # Tolerancia para convergencia de Bishop
TOLERANCIA_GEOMETRICA = 1e-6            # Tolerancia para cálculos geométricos
TOLERANCIA_NUMERICA = 1e-10             # Tolerancia para comparaciones numéricas

# Límites de iteración
MAX_ITERACIONES_BISHOP = 50             # Máximo número de iteraciones para Bishop
MAX_ITERACIONES_BUSQUEDA = 100          # Máximo para búsquedas geométricas

# Rangos de validación para parámetros geotécnicos
MIN_COHESION = 0.0                      # kPa
MAX_COHESION = 500.0                    # kPa
MIN_PHI_GRADOS = 0.0                    # grados
MAX_PHI_GRADOS = 50.0                   # grados
MIN_GAMMA = 10.0                        # kN/m³
MAX_GAMMA = 30.0                        # kN/m³

# Rangos de validación para factor de seguridad
MIN_FACTOR_SEGURIDAD = 0.1              # Mínimo teórico
MAX_FACTOR_SEGURIDAD = 10.0             # Máximo teórico
FACTOR_SEGURIDAD_CRITICO = 1.0          # Límite de estabilidad
FACTOR_SEGURIDAD_MARGINAL = 1.2         # Límite marginal
FACTOR_SEGURIDAD_SEGURO = 1.5           # Límite seguro

# Rangos geométricos
MIN_RADIO_CIRCULO = 1.0                 # m
MAX_RADIO_CIRCULO = 1000.0              # m
MIN_NUM_DOVELAS = 3                     # Mínimo número de dovelas
MAX_NUM_DOVELAS = 100                   # Máximo número de dovelas
MIN_ANCHO_DOVELA = 0.1                  # m
MAX_ANCHO_DOVELA = 50.0                 # m

# Límites para detección de problemas
MAX_ANGULO_ALPHA_GRADOS = 85.0          # Ángulo máximo de dovela (grados)
MIN_M_ALPHA = 0.001                     # Valor mínimo aceptable para mα
MAX_PORCENTAJE_TRACCION = 50.0          # % máximo de dovelas en tracción

# Constantes físicas
GAMMA_AGUA = 9.81                       # kN/m³ - Peso específico del agua
GRAVEDAD = 9.81                         # m/s² - Aceleración de la gravedad

# Constantes de clasificación
CLASIFICACIONES_ESTABILIDAD = {
    'INESTABLE': (0.0, 1.0),
    'MARGINALMENTE_ESTABLE': (1.0, 1.2),
    'ESTABLE': (1.2, 1.5),
    'MUY_ESTABLE': (1.5, float('inf'))
}

# Factores de seguridad típicos por tipo de proyecto
FACTORES_SEGURIDAD_TIPICOS = {
    'TEMPORAL': 1.2,                    # Obras temporales
    'PERMANENTE': 1.5,                  # Obras permanentes
    'CRITICO': 1.8,                     # Estructuras críticas
    'MINERO': 1.3,                      # Taludes mineros
    'CARRETERA': 1.4,                   # Taludes de carretera
    'FERROCARRIL': 1.5,                 # Taludes ferroviarios
}

# Parámetros por defecto
PARAMETROS_DEFAULT = {
    'num_dovelas': 10,
    'factor_inicial_bishop': 1.0,
    'tolerancia_bishop': TOLERANCIA_CONVERGENCIA_BISHOP,
    'max_iteraciones_bishop': MAX_ITERACIONES_BISHOP,
    'validar_entrada': True,
    'generar_reporte': True
}

# Códigos de error para validaciones
CODIGOS_ERROR = {
    'PARAMETROS_INVALIDOS': 'E001',
    'GEOMETRIA_INVALIDA': 'E002',
    'DOVELAS_INVALIDAS': 'E003',
    'CONVERGENCIA_FALLIDA': 'E004',
    'FACTOR_SEGURIDAD_INVALIDO': 'E005',
    'TRACCION_EXCESIVA': 'W001',
    'M_ALPHA_BAJO': 'W002',
    'ITERACIONES_ALTAS': 'W003'
}

# Mensajes de advertencia
MENSAJES_ADVERTENCIA = {
    'TRACCION_DETECTADA': "Dovelas en tracción detectadas - revisar superficie de falla",
    'M_ALPHA_BAJO': "Factores mα bajos detectados - posible inestabilidad numérica",
    'CONVERGENCIA_LENTA': "Convergencia lenta - verificar parámetros iniciales",
    'DIFERENCIA_METODOS_ALTA': "Gran diferencia entre métodos - revisar geometría"
}

# Configuración de reportes
FORMATO_REPORTE = {
    'ancho_linea': 70,
    'decimales_fs': 3,
    'decimales_momento': 1,
    'decimales_fuerza': 1,
    'decimales_convergencia': 6,
    'max_iteraciones_mostrar': 10
}
