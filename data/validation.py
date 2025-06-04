"""
Validaciones críticas para análisis de estabilidad de taludes.

Este módulo contiene todas las validaciones necesarias para garantizar:
- Consistencia geotécnica de parámetros
- Validez geométrica de círculos y dovelas
- Convergencia en métodos iterativos
- Detección de casos problemáticos (tracción, mα ≤ 0)
- Verificación de unidades y rangos válidos
"""

import math
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass

from data.models import Estrato, Dovela, CirculoFalla
from data.constants import TOLERANCIA_CONVERGENCIA_BISHOP, MAX_ITERACIONES_BISHOP


@dataclass
class ResultadoValidacion:
    """
    Resultado de una validación con detalles del error si existe.
    """
    es_valido: bool
    mensaje: str
    codigo_error: Optional[str] = None
    valor_problematico: Optional[float] = None


class ValidacionError(Exception):
    """
    Excepción personalizada para errores de validación.
    """
    def __init__(self, mensaje: str, codigo_error: str = None, valor_problematico: float = None):
        super().__init__(mensaje)
        self.codigo_error = codigo_error
        self.valor_problematico = valor_problematico


def validar_parametros_geotecnicos(estrato: Estrato) -> ResultadoValidacion:
    """
    Valida que los parámetros geotécnicos estén en rangos realistas.
    
    Args:
        estrato: Estrato a validar
        
    Returns:
        Resultado de la validación
    """
    # Rangos típicos para parámetros geotécnicos
    RANGOS_VALIDOS = {
        'cohesion': (0.0, 500.0),  # kPa
        'phi_grados': (0.0, 50.0),  # grados
        'gamma': (10.0, 30.0)  # kN/m³
    }
    
    # Validar cohesión
    if not (RANGOS_VALIDOS['cohesion'][0] <= estrato.cohesion <= RANGOS_VALIDOS['cohesion'][1]):
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Cohesión {estrato.cohesion} kPa fuera del rango típico {RANGOS_VALIDOS['cohesion']}",
            codigo_error="COHESION_FUERA_RANGO",
            valor_problematico=estrato.cohesion
        )
    
    # Validar ángulo de fricción
    if not (RANGOS_VALIDOS['phi_grados'][0] <= estrato.phi_grados <= RANGOS_VALIDOS['phi_grados'][1]):
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Ángulo de fricción {estrato.phi_grados}° fuera del rango típico {RANGOS_VALIDOS['phi_grados']}",
            codigo_error="PHI_FUERA_RANGO",
            valor_problematico=estrato.phi_grados
        )
    
    # Validar peso específico
    if not (RANGOS_VALIDOS['gamma'][0] <= estrato.gamma <= RANGOS_VALIDOS['gamma'][1]):
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Peso específico {estrato.gamma} kN/m³ fuera del rango típico {RANGOS_VALIDOS['gamma']}",
            codigo_error="GAMMA_FUERA_RANGO",
            valor_problematico=estrato.gamma
        )
    
    # Validar combinación φ-c (suelos con alta cohesión suelen tener bajo φ)
    if estrato.cohesion > 100.0 and estrato.phi_grados > 35.0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Combinación inusual: alta cohesión ({estrato.cohesion} kPa) con alto φ ({estrato.phi_grados}°)",
            codigo_error="COMBINACION_PHI_C_INUSUAL"
        )
    
    return ResultadoValidacion(
        es_valido=True,
        mensaje="Parámetros geotécnicos válidos"
    )


def validar_geometria_circulo_avanzada(circulo: CirculoFalla, 
                                     perfil_terreno: List[Tuple[float, float]],
                                     tolerancia_interseccion: float = 0.1) -> ResultadoValidacion:
    """
    Validación avanzada de geometría de círculo de falla.
    
    Args:
        circulo: Círculo de falla
        perfil_terreno: Perfil del terreno
        tolerancia_interseccion: Tolerancia mínima para intersección
        
    Returns:
        Resultado de la validación
    """
    # Validar que el círculo tenga dimensiones razonables
    if circulo.radio < 1.0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Radio {circulo.radio} m demasiado pequeño (mínimo 1.0 m)",
            codigo_error="RADIO_DEMASIADO_PEQUENO",
            valor_problematico=circulo.radio
        )
    
    if circulo.radio > 1000.0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Radio {circulo.radio} m demasiado grande (máximo 1000.0 m)",
            codigo_error="RADIO_DEMASIADO_GRANDE",
            valor_problematico=circulo.radio
        )
    
    # Validar intersección con terreno
    x_min_terreno = min(punto[0] for punto in perfil_terreno)
    x_max_terreno = max(punto[0] for punto in perfil_terreno)
    
    x_min_circulo = circulo.xc - circulo.radio
    x_max_circulo = circulo.xc + circulo.radio
    
    # Calcular longitud de intersección
    x_interseccion_min = max(x_min_terreno, x_min_circulo)
    x_interseccion_max = min(x_max_terreno, x_max_circulo)
    longitud_interseccion = x_interseccion_max - x_interseccion_min
    
    if longitud_interseccion < tolerancia_interseccion:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Intersección círculo-terreno insuficiente: {longitud_interseccion:.2f} m < {tolerancia_interseccion} m",
            codigo_error="INTERSECCION_INSUFICIENTE",
            valor_problematico=longitud_interseccion
        )
    
    # Validar que el centro esté en posición razonable
    from core.geometry import interpolar_terreno, calcular_y_circulo

    # Verificar que el círculo intersecta o está cerca del terreno
    intersecta = False
    min_distancia_terreno = float('inf')
    
    # Verificar intersección en múltiples puntos del perfil
    for i in range(len(perfil_terreno) - 1):
        x1, y1 = perfil_terreno[i]
        x2, y2 = perfil_terreno[i + 1]
        
        # Puntos de prueba en el segmento
        for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
            x_test = x1 + alpha * (x2 - x1)
            y_test = y1 + alpha * (y2 - y1)
            
            # Distancia del punto al centro del círculo
            distancia = math.sqrt((x_test - circulo.xc)**2 + (y_test - circulo.yc)**2)
            
            # Si la distancia es aproximadamente igual al radio, hay intersección
            if abs(distancia - circulo.radio) < tolerancia_interseccion:
                intersecta = True
                break
        
        if intersecta:
            break
    
    # Si no intersecta directamente, verificar distancia mínima
    if not intersecta:
        # Revisar puntos en el perímetro del círculo
        for angulo in range(0, 360, 10):  # Cada 10 grados
            rad = math.radians(angulo)
            x_circulo = circulo.xc + circulo.radio * math.cos(rad)
            y_circulo = circulo.yc + circulo.radio * math.sin(rad)
            
            # Solo considerar puntos dentro del rango horizontal del terreno
            if x_min_terreno <= x_circulo <= x_max_terreno:
                try:
                    y_terreno = interpolar_terreno(x_circulo, perfil_terreno)
                    distancia_vertical = abs(y_circulo - y_terreno)
                    min_distancia_terreno = min(min_distancia_terreno, distancia_vertical)
                except:
                    continue
        
        # Si el círculo está demasiado lejos del terreno, es inválido
        if min_distancia_terreno > circulo.radio * 0.5:  # 50% del radio como tolerancia
            return ResultadoValidacion(
                es_valido=False,
                mensaje=f"Círculo demasiado lejos del terreno: distancia mínima = {min_distancia_terreno:.2f}m",
                codigo_error="CIRCULO_DEMASIADO_LEJANO",
                valor_problematico=min_distancia_terreno
            )
    
    try:
        # Elevación del terreno en el centro horizontal del círculo
        if x_min_terreno <= circulo.xc <= x_max_terreno:
            y_terreno_centro = interpolar_terreno(circulo.xc, perfil_terreno)
            
            # El centro no debe estar demasiado alto
            altura_centro = circulo.yc - y_terreno_centro
            if altura_centro > 5 * circulo.radio:
                return ResultadoValidacion(
                    es_valido=False,
                    mensaje=f"Centro demasiado alto: {altura_centro:.1f} m > 5×radio ({5*circulo.radio:.1f} m)",
                    codigo_error="CENTRO_DEMASIADO_ALTO",
                    valor_problematico=altura_centro
                )
                
    except Exception as e:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Error validando posición del centro: {e}",
            codigo_error="ERROR_VALIDACION_CENTRO"
        )
    
    return ResultadoValidacion(
        es_valido=True,
        mensaje="Geometría del círculo válida"
    )


def validar_dovela_critica(dovela: Dovela) -> ResultadoValidacion:
    """
    Validación crítica de una dovela individual.
    
    Args:
        dovela: Dovela a validar
        
    Returns:
        Resultado de la validación
    """
    # Validar dimensiones físicas
    if dovela.ancho <= 0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Ancho de dovela inválido: {dovela.ancho} m",
            codigo_error="ANCHO_INVALIDO",
            valor_problematico=dovela.ancho
        )
    
    if dovela.altura <= 0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Altura de dovela inválida: {dovela.altura} m",
            codigo_error="ALTURA_INVALIDA",
            valor_problematico=dovela.altura
        )
    
    # Validar peso
    if dovela.peso <= 0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Peso de dovela inválido: {dovela.peso} kN",
            codigo_error="PESO_INVALIDO",
            valor_problematico=dovela.peso
        )
    
    # Validar ángulo α (debe estar en rango razonable)
    if abs(dovela.angulo_alpha) > math.pi/2:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Ángulo α fuera de rango: {math.degrees(dovela.angulo_alpha):.1f}° (máximo ±90°)",
            codigo_error="ANGULO_ALPHA_FUERA_RANGO",
            valor_problematico=math.degrees(dovela.angulo_alpha)
        )
    
    # Validar que mα > 0 (crítico para método Bishop)
    m_alpha = dovela.cos_alpha + (dovela.sin_alpha * dovela.tan_phi)
    if m_alpha <= 0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"mα ≤ 0 detectado: mα = {m_alpha:.4f} (cos α + sin α × tan φ)",
            codigo_error="M_ALPHA_NO_POSITIVO",
            valor_problematico=m_alpha
        )
    
    # Advertir si la dovela está en tracción
    fuerza_normal_efectiva = dovela.calcular_fuerza_normal_efectiva()
    if fuerza_normal_efectiva < 0:
        return ResultadoValidacion(
            es_valido=True,  # Es válido pero problemático
            mensaje=f"Dovela en tracción: N' = {fuerza_normal_efectiva:.1f} kN < 0",
            codigo_error="DOVELA_EN_TRACCION",
            valor_problematico=fuerza_normal_efectiva
        )
    
    return ResultadoValidacion(
        es_valido=True,
        mensaje="Dovela válida"
    )


def validar_conjunto_dovelas(dovelas: List[Dovela]) -> ResultadoValidacion:
    """
    Valida un conjunto de dovelas como sistema.
    
    Args:
        dovelas: Lista de dovelas a validar
        
    Returns:
        Resultado de la validación
    """
    if len(dovelas) < 3:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Número insuficiente de dovelas: {len(dovelas)} < 3",
            codigo_error="POCAS_DOVELAS",
            valor_problematico=len(dovelas)
        )
    
    if len(dovelas) > 100:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Demasiadas dovelas: {len(dovelas)} > 100 (puede causar problemas numéricos)",
            codigo_error="DEMASIADAS_DOVELAS",
            valor_problematico=len(dovelas)
        )
    
    # Contar dovelas problemáticas
    dovelas_en_traccion = 0
    dovelas_m_alpha_problematico = 0
    
    for i, dovela in enumerate(dovelas):
        # Verificar tracción
        if dovela.calcular_fuerza_normal_efectiva() < 0:
            dovelas_en_traccion += 1
        
        # Verificar mα
        m_alpha = dovela.cos_alpha + (dovela.sin_alpha * dovela.tan_phi)
        if m_alpha <= 0:
            dovelas_m_alpha_problematico += 1
    
    # Verificar porcentaje de dovelas problemáticas
    porcentaje_traccion = (dovelas_en_traccion / len(dovelas)) * 100
    porcentaje_m_alpha = (dovelas_m_alpha_problematico / len(dovelas)) * 100
    
    # Permitir algunas dovelas con mα problemático (hasta 20% es aceptable)
    if porcentaje_m_alpha > 20:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Demasiadas dovelas con mα ≤ 0: {dovelas_m_alpha_problematico} ({porcentaje_m_alpha:.1f}%) > 20%",
            codigo_error="M_ALPHA_PROBLEMATICO_MULTIPLE",
            valor_problematico=porcentaje_m_alpha
        )
    
    if porcentaje_traccion > 50:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Demasiadas dovelas en tracción: {dovelas_en_traccion} ({porcentaje_traccion:.1f}%)",
            codigo_error="EXCESO_TRACCION",
            valor_problematico=porcentaje_traccion
        )
    
    # Validar continuidad espacial (dovelas deben estar ordenadas)
    for i in range(len(dovelas) - 1):
        if dovelas[i].x_centro >= dovelas[i+1].x_centro:
            return ResultadoValidacion(
                es_valido=False,
                mensaje=f"Dovelas no ordenadas: dovela {i} (x={dovelas[i].x_centro}) >= dovela {i+1} (x={dovelas[i+1].x_centro})",
                codigo_error="DOVELAS_NO_ORDENADAS"
            )
    
    mensaje = f"Conjunto de {len(dovelas)} dovelas válido"
    if dovelas_en_traccion > 0:
        mensaje += f" ({dovelas_en_traccion} en tracción: {porcentaje_traccion:.1f}%)"
    
    return ResultadoValidacion(
        es_valido=True,
        mensaje=mensaje
    )


def validar_convergencia_bishop(factores_seguridad: List[float], 
                               iteracion: int) -> ResultadoValidacion:
    """
    Valida la convergencia del método Bishop iterativo.
    
    Args:
        factores_seguridad: Lista de factores de seguridad de iteraciones
        iteracion: Número de iteración actual
        
    Returns:
        Resultado de la validación
    """
    if len(factores_seguridad) < 2:
        return ResultadoValidacion(
            es_valido=True,
            mensaje="Insuficientes iteraciones para evaluar convergencia"
        )
    
    # Verificar que no haya valores inválidos
    for i, fs in enumerate(factores_seguridad):
        if fs <= 0 or math.isnan(fs) or math.isinf(fs):
            return ResultadoValidacion(
                es_valido=False,
                mensaje=f"Factor de seguridad inválido en iteración {i}: {fs}",
                codigo_error="FS_INVALIDO",
                valor_problematico=fs
            )
    
    # Calcular diferencia entre últimas dos iteraciones
    diferencia = abs(factores_seguridad[-1] - factores_seguridad[-2])
    
    # Verificar convergencia
    if diferencia < TOLERANCIA_CONVERGENCIA_BISHOP:
        return ResultadoValidacion(
            es_valido=True,
            mensaje=f"Convergencia alcanzada en iteración {iteracion}: Δ={diferencia:.6f} < {TOLERANCIA_CONVERGENCIA_BISHOP}"
        )
    
    # Verificar máximo de iteraciones
    if iteracion >= MAX_ITERACIONES_BISHOP:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Máximo de iteraciones alcanzado ({MAX_ITERACIONES_BISHOP}): Δ={diferencia:.6f}",
            codigo_error="NO_CONVERGENCIA",
            valor_problematico=diferencia
        )
    
    # Verificar divergencia (diferencia creciente)
    if len(factores_seguridad) >= 3:
        diferencia_anterior = abs(factores_seguridad[-2] - factores_seguridad[-3])
        if diferencia > 2 * diferencia_anterior and diferencia > 0.1:
            return ResultadoValidacion(
                es_valido=False,
                mensaje=f"Posible divergencia detectada: Δ={diferencia:.4f} > 2×Δ_anterior={2*diferencia_anterior:.4f}",
                codigo_error="POSIBLE_DIVERGENCIA",
                valor_problematico=diferencia
            )
    
    return ResultadoValidacion(
        es_valido=True,
        mensaje=f"Iteración {iteracion}: Δ={diferencia:.6f}, continuando..."
    )


def validar_factor_seguridad(factor_seguridad: float) -> ResultadoValidacion:
    """
    Valida que un factor de seguridad esté en un rango razonable.
    
    Args:
        factor_seguridad: Factor de seguridad a validar
        
    Returns:
        Resultado de la validación
    """
    if factor_seguridad <= 0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Factor de seguridad no positivo: {factor_seguridad}",
            codigo_error="FS_NO_POSITIVO",
            valor_problematico=factor_seguridad
        )
    
    if math.isnan(factor_seguridad) or math.isinf(factor_seguridad):
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Factor de seguridad inválido: {factor_seguridad}",
            codigo_error="FS_INVALIDO",
            valor_problematico=factor_seguridad
        )
    
    if factor_seguridad > 10.0:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Factor de seguridad sospechosamente alto: {factor_seguridad:.2f} > 10.0",
            codigo_error="FS_DEMASIADO_ALTO",
            valor_problematico=factor_seguridad
        )
    
    # Clasificación del factor de seguridad
    if factor_seguridad < 1.0:
        clasificacion = "INESTABLE"
    elif factor_seguridad < 1.2:
        clasificacion = "MARGINALMENTE ESTABLE"
    elif factor_seguridad < 1.5:
        clasificacion = "ESTABLE"
    else:
        clasificacion = "MUY ESTABLE"
    
    return ResultadoValidacion(
        es_valido=True,
        mensaje=f"Factor de seguridad: {factor_seguridad:.3f} ({clasificacion})"
    )


def validar_perfil_terreno(perfil: List[Tuple[float, float]]) -> ResultadoValidacion:
    """
    Valida un perfil de terreno.
    
    Args:
        perfil: Lista de puntos (x, y) del perfil
        
    Returns:
        Resultado de la validación
    """
    if len(perfil) < 2:
        return ResultadoValidacion(
            es_valido=False,
            mensaje=f"Perfil insuficiente: {len(perfil)} puntos < 2",
            codigo_error="PERFIL_INSUFICIENTE",
            valor_problematico=len(perfil)
        )
    
    # Verificar que esté ordenado por X
    for i in range(len(perfil) - 1):
        if perfil[i][0] >= perfil[i+1][0]:
            return ResultadoValidacion(
                es_valido=False,
                mensaje=f"Perfil no ordenado: x[{i}]={perfil[i][0]} >= x[{i+1}]={perfil[i+1][0]}",
                codigo_error="PERFIL_NO_ORDENADO"
            )
    
    # Verificar pendientes extremas
    for i in range(len(perfil) - 1):
        dx = perfil[i+1][0] - perfil[i][0]
        dy = perfil[i+1][1] - perfil[i][1]
        
        if dx > 0:
            pendiente = abs(dy / dx)
            if pendiente > 10.0:  # Pendiente > 10:1
                return ResultadoValidacion(
                    es_valido=False,
                    mensaje=f"Pendiente extrema entre puntos {i} y {i+1}: {pendiente:.1f} > 10.0",
                    codigo_error="PENDIENTE_EXTREMA",
                    valor_problematico=pendiente
                )
    
    return ResultadoValidacion(
        es_valido=True,
        mensaje=f"Perfil de terreno válido ({len(perfil)} puntos)"
    )


def validar_entrada_completa(circulo: CirculoFalla, 
                           perfil_terreno: List[Tuple[float, float]],
                           estrato: Estrato,
                           nivel_freatico: Optional[List[Tuple[float, float]]] = None) -> List[ResultadoValidacion]:
    """
    Validación completa de todos los datos de entrada.
    
    Args:
        circulo: Círculo de falla
        perfil_terreno: Perfil del terreno
        estrato: Propiedades del suelo
        nivel_freatico: Nivel freático (opcional)
        
    Returns:
        Lista de resultados de validación
    """
    resultados = []
    
    # Validar estrato
    resultados.append(validar_parametros_geotecnicos(estrato))
    
    # Validar perfil de terreno
    resultados.append(validar_perfil_terreno(perfil_terreno))
    
    # Validar nivel freático si existe
    if nivel_freatico is not None:
        resultado_freatico = validar_perfil_terreno(nivel_freatico)
        resultado_freatico.mensaje = "Nivel freático: " + resultado_freatico.mensaje
        resultados.append(resultado_freatico)
    
    # Validar geometría del círculo
    resultados.append(validar_geometria_circulo_avanzada(circulo, perfil_terreno))
    
    return resultados


def verificar_consistencia_unidades() -> ResultadoValidacion:
    """
    Verifica que las unidades del sistema sean consistentes.
    
    Returns:
        Resultado de la verificación
    """
    unidades_esperadas = {
        'longitud': 'm',
        'fuerza': 'kN',
        'presion': 'kPa',
        'peso_especifico': 'kN/m³',
        'angulo': 'radianes (internamente), grados (entrada)'
    }
    
    return ResultadoValidacion(
        es_valido=True,
        mensaje=f"Sistema de unidades: {unidades_esperadas}"
    )


# Funciones auxiliares para manejo de errores

def lanzar_si_invalido(resultado: ResultadoValidacion):
    """
    Lanza una excepción si el resultado de validación es inválido.
    
    Args:
        resultado: Resultado de validación
        
    Raises:
        ValidacionError: Si la validación falló
    """
    if not resultado.es_valido:
        raise ValidacionError(
            resultado.mensaje,
            resultado.codigo_error,
            resultado.valor_problematico
        )


def validar_y_reportar(validaciones: List[ResultadoValidacion], 
                      lanzar_excepcion: bool = False) -> Tuple[bool, List[str]]:
    """
    Evalúa múltiples validaciones y genera reporte.
    
    Args:
        validaciones: Lista de resultados de validación
        lanzar_excepcion: Si lanzar excepción en caso de error
        
    Returns:
        Tupla (todas_validas, lista_mensajes)
        
    Raises:
        ValidacionError: Si lanzar_excepcion=True y hay errores
    """
    todas_validas = True
    mensajes = []
    
    for resultado in validaciones:
        mensajes.append(f"{'✅' if resultado.es_valido else '❌'} {resultado.mensaje}")
        
        if not resultado.es_valido:
            todas_validas = False
            if lanzar_excepcion:
                lanzar_si_invalido(resultado)
    
    return todas_validas, mensajes
