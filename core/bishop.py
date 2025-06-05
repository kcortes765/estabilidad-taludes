"""
Implementación del método de Bishop Modificado para análisis de estabilidad de taludes.

El método de Bishop Modificado es un método iterativo que considera el equilibrio
de fuerzas y momentos, proporcionando resultados más precisos que Fellenius.

Ecuación principal:
Fs = Σ[c'·ΔL + (W - u·ΔL)·tan(φ')] / [Σ(W·sin(α)) · mα]

Donde mα = cos(α) + sin(α)·tan(φ')/Fs

El método requiere iteración hasta convergencia (|Fs_nuevo - Fs_anterior| < tolerancia)
"""

import math
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass

from data.models import Estrato, Dovela, CirculoFalla
from data.constants import TOLERANCIA_CONVERGENCIA_BISHOP, MAX_ITERACIONES_BISHOP
from data.validation import (
    validar_entrada_completa, validar_conjunto_dovelas, 
    validar_convergencia_bishop, validar_factor_seguridad,
    lanzar_si_invalido, ValidacionError
)
from core.geometry import crear_dovelas


@dataclass
class ResultadoBishop:
    """
    Resultado del análisis por método de Bishop Modificado.
    
    Attributes:
        factor_seguridad: Factor de seguridad final convergido
        iteraciones: Número de iteraciones hasta convergencia
        convergio: Si el método convergió exitosamente
        momento_resistente: Momento resistente total (kN·m)
        momento_actuante: Momento actuante total (kN·m)
        dovelas: Lista de dovelas analizadas
        fuerzas_resistentes: Fuerzas resistentes por dovela (kN)
        fuerzas_actuantes: Fuerzas actuantes por dovela (kN)
        factores_m_alpha: Factores mα por dovela
        historial_fs: Historial de factores de seguridad por iteración
        es_valido: Indica si el resultado es válido
        advertencias: Lista de advertencias del análisis
        detalles_calculo: Diccionario con detalles del cálculo
    """
    factor_seguridad: float
    iteraciones: int
    convergio: bool
    momento_resistente: float
    momento_actuante: float
    dovelas: List[Dovela]
    fuerzas_resistentes: List[float]
    fuerzas_actuantes: List[float]
    factores_m_alpha: List[float]
    historial_fs: List[float]
    es_valido: bool
    advertencias: List[str]
    detalles_calculo: Dict[str, Any]


def calcular_m_alpha(dovela: Dovela, factor_seguridad: float) -> float:
    """
    Calcula el factor mα para una dovela en el método de Bishop.
    
    mα = cos(α) + sin(α)·tan(φ')/Fs
    
    Args:
        dovela: Dovela a analizar
        factor_seguridad: Factor de seguridad actual
        
    Returns:
        Factor mα
        
    Raises:
        ValidacionError: Si mα ≤ 0 (condición crítica)
    """
    if factor_seguridad <= 0:
        raise ValidacionError(f"Factor de seguridad debe ser > 0: {factor_seguridad}")
    
    # Calcular mα
    m_alpha = dovela.cos_alpha + (dovela.sin_alpha * dovela.tan_phi) / factor_seguridad
    
    # Validación crítica: mα debe ser > 0
    if m_alpha <= 0:
        raise ValidacionError(
            f"mα ≤ 0 en dovela (x={dovela.x_centro:.1f}): mα={m_alpha:.4f}. "
            f"Esto indica que α={math.degrees(dovela.angulo_alpha):.1f}° es demasiado empinado "
            f"o Fs={factor_seguridad:.3f} es demasiado bajo para φ={math.degrees(math.atan(dovela.tan_phi)):.1f}°"
        )
    
    return m_alpha


def calcular_fuerza_resistente_bishop(dovela: Dovela, factor_seguridad: float) -> float:
    """
    Calcula la fuerza resistente de una dovela según Bishop Modificado.
    
    Fuerza resistente = [c'·ΔL + (W - u·ΔL)·tan(φ')] / mα
    
    Args:
        dovela: Dovela a analizar
        factor_seguridad: Factor de seguridad actual
        
    Returns:
        Fuerza resistente en kN
    """
    # Calcular mα
    m_alpha = calcular_m_alpha(dovela, factor_seguridad)
    
    # Componente de cohesión
    fuerza_cohesion = dovela.cohesion * dovela.longitud_arco
    
    # Fuerza normal total y presión de poros
    fuerza_normal_total = dovela.peso
    fuerza_poros = dovela.presion_poros * dovela.longitud_arco
    fuerza_normal_efectiva = fuerza_normal_total - fuerza_poros
    
    # Componente de fricción
    fuerza_friccion = fuerza_normal_efectiva * dovela.tan_phi
    
    # Fuerza resistente total dividida por mα
    fuerza_resistente = (fuerza_cohesion + fuerza_friccion) / m_alpha
    
    return max(0.0, fuerza_resistente)


def calcular_fuerza_actuante_bishop(dovela: Dovela) -> float:
    """
    Calcula la fuerza actuante de una dovela según Bishop.
    
    Fuerza actuante = W·sin(α) (igual que Fellenius)
    
    Args:
        dovela: Dovela a analizar
        
    Returns:
        Fuerza actuante en kN
    """
    return dovela.peso * dovela.sin_alpha


def iteracion_bishop(dovelas: List[Dovela], factor_seguridad_inicial: float) -> Tuple[float, List[float], List[float], List[float]]:
    """
    Realiza una iteración del método de Bishop.
    
    Args:
        dovelas: Lista de dovelas
        factor_seguridad_inicial: Factor de seguridad para esta iteración
        
    Returns:
        Tupla con (nuevo_fs, fuerzas_resistentes, fuerzas_actuantes, factores_m_alpha)
    """
    fuerzas_resistentes = []
    fuerzas_actuantes = []
    factores_m_alpha = []
    
    for dovela in dovelas:
        # Calcular mα para esta dovela
        m_alpha = calcular_m_alpha(dovela, factor_seguridad_inicial)
        factores_m_alpha.append(m_alpha)
        
        # Calcular fuerzas
        fuerza_r = calcular_fuerza_resistente_bishop(dovela, factor_seguridad_inicial)
        fuerza_a = calcular_fuerza_actuante_bishop(dovela)
        
        fuerzas_resistentes.append(fuerza_r)
        fuerzas_actuantes.append(fuerza_a)
    
    # Calcular nuevo factor de seguridad
    suma_resistentes = sum(fuerzas_resistentes)
    suma_actuantes = sum(fuerzas_actuantes)

    if suma_actuantes == 0:
        raise ValidacionError("Suma de fuerzas actuantes ≤ 0: superficie de falla inválida")

    nuevo_fs = suma_resistentes / abs(suma_actuantes)
    
    return nuevo_fs, fuerzas_resistentes, fuerzas_actuantes, factores_m_alpha


def analizar_bishop(circulo: CirculoFalla,
                   perfil_terreno: List[Tuple[float, float]],
                   estrato: Estrato,
                   nivel_freatico: Optional[List[Tuple[float, float]]] = None,
                   num_dovelas: int = 10,
                   factor_inicial: float = 1.0,
                   tolerancia: float = TOLERANCIA_CONVERGENCIA_BISHOP,
                   max_iteraciones: int = MAX_ITERACIONES_BISHOP,
                   validar_entrada: bool = True) -> ResultadoBishop:
    """
    Realiza el análisis de estabilidad usando el método de Bishop Modificado.
    
    Args:
        circulo: Círculo de falla a analizar
        perfil_terreno: Perfil del terreno [(x, y), ...]
        estrato: Propiedades del suelo
        nivel_freatico: Nivel freático opcional [(x, y), ...]
        num_dovelas: Número de dovelas para discretización
        factor_inicial: Factor de seguridad inicial para iteración
        tolerancia: Tolerancia de convergencia
        max_iteraciones: Máximo número de iteraciones
        validar_entrada: Si validar datos de entrada
        
    Returns:
        Resultado del análisis de Bishop
        
    Raises:
        ValidacionError: Si los datos de entrada son inválidos o no converge
    """
    advertencias = []
    detalles_calculo = {}
    
    # Validar entrada si se solicita
    if validar_entrada:
        validaciones = validar_entrada_completa(circulo, perfil_terreno, estrato, nivel_freatico)
        for validacion in validaciones:
            if not validacion.es_valido:
                raise ValidacionError(f"Validación falló: {validacion.mensaje}")
            elif validacion.codigo_error:
                advertencias.append(validacion.mensaje)
    
    # Crear dovelas
    try:
        dovelas = crear_dovelas(
            circulo=circulo,
            perfil_terreno=perfil_terreno,
            estrato=estrato,
            nivel_freatico=nivel_freatico,
            num_dovelas=num_dovelas
        )
    except Exception as e:
        raise ValidacionError(f"Error creando dovelas: {e}")
    
    # Validar conjunto de dovelas
    resultado_dovelas = validar_conjunto_dovelas(dovelas)
    if not resultado_dovelas.es_valido:
        raise ValidacionError(f"Conjunto de dovelas inválido: {resultado_dovelas.mensaje}")
    elif resultado_dovelas.codigo_error:
        advertencias.append(resultado_dovelas.mensaje)
    
    # Proceso iterativo de Bishop
    factor_seguridad = factor_inicial
    historial_fs = [factor_seguridad]
    convergio = False
    iteraciones = 0
    
    fuerzas_resistentes = []
    fuerzas_actuantes = []
    factores_m_alpha = []
    
    for iteracion in range(max_iteraciones):
        iteraciones = iteracion + 1
        
        try:
            # Realizar una iteración
            nuevo_fs, fuerzas_r, fuerzas_a, m_alphas = iteracion_bishop(dovelas, factor_seguridad)
            
            # Verificar convergencia
            diferencia = abs(nuevo_fs - factor_seguridad)
            
            # Actualizar para próxima iteración
            factor_seguridad = nuevo_fs
            historial_fs.append(factor_seguridad)
            fuerzas_resistentes = fuerzas_r
            fuerzas_actuantes = fuerzas_a
            factores_m_alpha = m_alphas
            
            # Verificar convergencia
            if diferencia < tolerancia:
                convergio = True
                break
                
            # Verificar divergencia
            if iteracion > 5 and len(historial_fs) >= 3:
                # Verificar si está oscilando
                ultimos_3 = historial_fs[-3:]
                if max(ultimos_3) - min(ultimos_3) > 0.5:
                    advertencias.append(f"Posible divergencia detectada en iteración {iteracion}")
                    
        except ValidacionError as e:
            if "mα ≤ 0" in str(e):
                raise ValidacionError(f"Convergencia imposible: {e}")
            else:
                raise
    
    # Verificar convergencia final
    if not convergio:
        raise ValidacionError(f"No convergió en {max_iteraciones} iteraciones. Última diferencia: {diferencia:.6f}")
    
    # Validar convergencia
    resultado_convergencia = validar_convergencia_bishop(
        historial_fs, iteraciones
    )
    if not resultado_convergencia.es_valido:
        raise ValidacionError(f"Convergencia inválida: {resultado_convergencia.mensaje}")
    
    # Calcular momentos totales
    momento_resistente = sum(fuerzas_resistentes) * circulo.radio
    suma_actuantes = sum(fuerzas_actuantes)
    momento_actuante = abs(suma_actuantes) * circulo.radio
    
    # Validar factor de seguridad final
    resultado_fs = validar_factor_seguridad(factor_seguridad)
    if not resultado_fs.es_valido:
        raise ValidacionError(f"Factor de seguridad final inválido: {resultado_fs.mensaje}")
    
    # Verificar dovelas problemáticas
    dovelas_problematicas = []
    dovelas_m_alpha_bajo = []
    
    for i, (dovela, m_alpha) in enumerate(zip(dovelas, factores_m_alpha)):
        # Verificar tracción
        if dovela.calcular_fuerza_normal_efectiva() < 0:
            dovelas_problematicas.append(i)
            advertencias.append(f"Dovela {i} en tracción: N' = {dovela.calcular_fuerza_normal_efectiva():.1f} kN")
        
        # Verificar mα bajo
        if m_alpha < 0.1:
            dovelas_m_alpha_bajo.append(i)
            advertencias.append(f"Dovela {i} con mα bajo: {m_alpha:.3f}")
    
    # Agregar detalles del cálculo
    detalles_calculo.update({
        'num_dovelas': len(dovelas),
        'dovelas_en_traccion': len(dovelas_problematicas),
        'dovelas_m_alpha_bajo': len(dovelas_m_alpha_bajo),
        'porcentaje_traccion': (len(dovelas_problematicas) / len(dovelas)) * 100,
        'suma_fuerzas_resistentes': sum(fuerzas_resistentes),
        'suma_fuerzas_actuantes': abs(sum(fuerzas_actuantes)),
        'radio_circulo': circulo.radio,
        'centro_circulo': (circulo.xc, circulo.yc),
        'factor_inicial': factor_inicial,
        'tolerancia_usada': tolerancia,
        'diferencia_final': diferencia,
        'metodo': 'Bishop Modificado',
        'es_iterativo': True
    })
    
    # Verificar estabilidad
    es_valido = True
    if factor_seguridad < 0.5:
        advertencias.append("Factor de seguridad muy bajo: posible error en datos")
        es_valido = False
    elif len(dovelas_problematicas) > len(dovelas) // 2:
        advertencias.append(f"Muchas dovelas en tracción ({len(dovelas_problematicas)}/{len(dovelas)})")
    elif len(dovelas_m_alpha_bajo) > len(dovelas) // 3:
        advertencias.append(f"Muchas dovelas con mα bajo ({len(dovelas_m_alpha_bajo)}/{len(dovelas)})")
    
    return ResultadoBishop(
        factor_seguridad=factor_seguridad,
        iteraciones=iteraciones,
        convergio=convergio,
        momento_resistente=momento_resistente,
        momento_actuante=momento_actuante,
        dovelas=dovelas,
        fuerzas_resistentes=fuerzas_resistentes,
        fuerzas_actuantes=fuerzas_actuantes,
        factores_m_alpha=factores_m_alpha,
        historial_fs=historial_fs,
        es_valido=es_valido,
        advertencias=advertencias,
        detalles_calculo=detalles_calculo
    )


def generar_reporte_bishop(resultado: ResultadoBishop) -> str:
    """
    Genera un reporte detallado del análisis de Bishop.
    
    Args:
        resultado: Resultado del análisis
        
    Returns:
        Reporte en formato texto
    """
    reporte = []
    reporte.append("=" * 60)
    reporte.append("ANÁLISIS DE ESTABILIDAD - MÉTODO DE BISHOP MODIFICADO")
    reporte.append("=" * 60)
    
    # Resultados principales
    reporte.append(f"\n📊 RESULTADOS PRINCIPALES:")
    reporte.append(f"   Factor de Seguridad: {resultado.factor_seguridad:.3f}")
    
    # Clasificación
    if resultado.factor_seguridad < 1.0:
        clasificacion = "INESTABLE ⚠️"
    elif resultado.factor_seguridad < 1.2:
        clasificacion = "MARGINALMENTE ESTABLE ⚡"
    elif resultado.factor_seguridad < 1.5:
        clasificacion = "ESTABLE ✅"
    else:
        clasificacion = "MUY ESTABLE 🛡️"
    
    reporte.append(f"   Clasificación: {clasificacion}")
    
    # Convergencia
    reporte.append(f"\n🔄 CONVERGENCIA:")
    reporte.append(f"   Convergió: {'SÍ' if resultado.convergio else 'NO'}")
    reporte.append(f"   Iteraciones: {resultado.iteraciones}")
    reporte.append(f"   Tolerancia: {resultado.detalles_calculo['tolerancia_usada']:.6f}")
    reporte.append(f"   Diferencia final: {resultado.detalles_calculo['diferencia_final']:.6f}")
    
    # Momentos
    reporte.append(f"\n🔄 EQUILIBRIO DE MOMENTOS:")
    reporte.append(f"   Momento Resistente: {resultado.momento_resistente:.1f} kN·m")
    reporte.append(f"   Momento Actuante: {resultado.momento_actuante:.1f} kN·m")
    reporte.append(f"   Radio del círculo: {resultado.detalles_calculo['radio_circulo']:.1f} m")
    
    # Fuerzas
    reporte.append(f"\n⚖️ EQUILIBRIO DE FUERZAS:")
    reporte.append(f"   Σ Fuerzas Resistentes: {resultado.detalles_calculo['suma_fuerzas_resistentes']:.1f} kN")
    reporte.append(f"   Σ Fuerzas Actuantes: {resultado.detalles_calculo['suma_fuerzas_actuantes']:.1f} kN")
    
    # Detalles de dovelas
    reporte.append(f"\n🧱 ANÁLISIS DE DOVELAS:")
    reporte.append(f"   Número de dovelas: {resultado.detalles_calculo['num_dovelas']}")
    reporte.append(f"   Dovelas en tracción: {resultado.detalles_calculo['dovelas_en_traccion']}")
    reporte.append(f"   Dovelas con mα bajo: {resultado.detalles_calculo['dovelas_m_alpha_bajo']}")
    reporte.append(f"   Porcentaje en tracción: {resultado.detalles_calculo['porcentaje_traccion']:.1f}%")
    
    # Historial de convergencia
    reporte.append(f"\n📈 HISTORIAL DE CONVERGENCIA:")
    reporte.append("   Iter |   Fs   | Diferencia")
    reporte.append("   -----|--------|----------")
    for i, fs in enumerate(resultado.historial_fs):
        if i == 0:
            diff_str = "  inicial"
        else:
            diff = abs(fs - resultado.historial_fs[i-1])
            diff_str = f"{diff:8.6f}"
        reporte.append(f"   {i:4d} | {fs:6.3f} | {diff_str}")
        if i >= 10:  # Limitar a primeras 10 iteraciones para reporte
            reporte.append("   ...  |  ...   |    ...")
            break
    
    # Advertencias
    if resultado.advertencias:
        reporte.append(f"\n⚠️ ADVERTENCIAS:")
        for i, advertencia in enumerate(resultado.advertencias, 1):
            reporte.append(f"   {i}. {advertencia}")
    
    # Validez del resultado
    reporte.append(f"\n✅ VALIDEZ DEL RESULTADO: {'VÁLIDO' if resultado.es_valido else 'INVÁLIDO'}")
    
    reporte.append("\n" + "=" * 60)
    reporte.append("Método: Bishop Modificado - Análisis iterativo")
    reporte.append("Considera equilibrio de fuerzas y momentos")
    reporte.append("=" * 60)
    
    return "\n".join(reporte)


# Funciones auxiliares para casos comunes

def bishop_talud_homogeneo(altura: float,
                          angulo_talud: float,
                          cohesion: float,
                          phi_grados: float,
                          gamma: float,
                          factor_radio: float = 1.5,
                          num_dovelas: int = 10,
                          factor_inicial: float = 1.0,
                          validar_entrada: bool = True) -> ResultadoBishop:
    """
    Análisis de Bishop para un talud homogéneo simple.
    
    Args:
        altura: Altura del talud (m)
        angulo_talud: Ángulo del talud en grados
        cohesion: Cohesión del suelo (kPa)
        phi_grados: Ángulo de fricción (grados)
        gamma: Peso específico (kN/m³)
        factor_radio: Factor para calcular radio
        num_dovelas: Número de dovelas
        factor_inicial: Factor de seguridad inicial
        validar_entrada: Si validar datos de entrada
        
    Returns:
        Resultado del análisis
    """
    from core.geometry import crear_perfil_simple
    
    # Crear geometría simple con extensión adecuada
    longitud_base = altura / math.tan(math.radians(angulo_talud))
    perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
    
    # Círculo de falla más realista
    radio = factor_radio * altura
    xc = longitud_base * 0.3  # Centro más hacia atrás
    yc = altura * 1.1  # Centro más alto
    circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
    
    # Estrato homogéneo
    estrato = Estrato(cohesion=cohesion, phi_grados=phi_grados, gamma=gamma, nombre="Homogéneo")
    
    return analizar_bishop(circulo, perfil, estrato, num_dovelas=num_dovelas, 
                          factor_inicial=factor_inicial, validar_entrada=validar_entrada)


def bishop_con_nivel_freatico(altura: float,
                             angulo_talud: float,
                             cohesion: float,
                             phi_grados: float,
                             gamma: float,
                             altura_nivel_freatico: float,
                             factor_radio: float = 1.5,
                             num_dovelas: int = 10,
                             factor_inicial: float = 1.0,
                             validar_entrada: bool = True) -> ResultadoBishop:
    """
    Análisis de Bishop con nivel freático horizontal.
    
    Args:
        altura: Altura del talud (m)
        angulo_talud: Ángulo del talud en grados
        cohesion: Cohesión del suelo (kPa)
        phi_grados: Ángulo de fricción (grados)
        gamma: Peso específico (kN/m³)
        altura_nivel_freatico: Altura del nivel freático (m)
        factor_radio: Factor para calcular radio
        num_dovelas: Número de dovelas
        factor_inicial: Factor de seguridad inicial
        validar_entrada: Si validar datos de entrada
        
    Returns:
        Resultado del análisis
    """
    from core.geometry import crear_perfil_simple, crear_nivel_freatico_horizontal
    
    # Crear geometría con extensión adecuada
    longitud_base = altura / math.tan(math.radians(angulo_talud))
    perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
    
    # Nivel freático
    nivel_freatico = crear_nivel_freatico_horizontal(0.0, longitud_base * 3, altura_nivel_freatico)
    
    # Círculo de falla más realista
    radio = factor_radio * altura
    xc = longitud_base * 0.3  # Centro más hacia atrás
    yc = altura * 1.1  # Centro más alto
    circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
    
    # Estrato homogéneo
    estrato = Estrato(cohesion=cohesion, phi_grados=phi_grados, gamma=gamma, nombre="Con NF")
    
    return analizar_bishop(circulo, perfil, estrato, nivel_freatico=nivel_freatico,
                          num_dovelas=num_dovelas, factor_inicial=factor_inicial,
                          validar_entrada=validar_entrada)


def comparar_bishop_fellenius(circulo: CirculoFalla,
                             perfil_terreno: List[Tuple[float, float]],
                             estrato: Estrato,
                             nivel_freatico: Optional[List[Tuple[float, float]]] = None,
                             num_dovelas: int = 10,
                             factor_inicial: float = 1.0) -> Dict[str, Any]:
    """
    Compara los resultados de Bishop y Fellenius para el mismo caso.
    
    Args:
        circulo: Círculo de falla
        perfil_terreno: Perfil del terreno
        estrato: Propiedades del suelo
        nivel_freatico: Nivel freático opcional
        num_dovelas: Número de dovelas
        factor_inicial: Factor inicial para Bishop
        
    Returns:
        Diccionario con comparación de resultados
    """
    from core.fellenius import analizar_fellenius
    
    # Análisis con Bishop
    resultado_bishop = analizar_bishop(
        circulo=circulo,
        perfil_terreno=perfil_terreno,
        estrato=estrato,
        nivel_freatico=nivel_freatico,
        num_dovelas=num_dovelas,
        factor_inicial=factor_inicial
    )
    
    # Análisis con Fellenius
    resultado_fellenius = analizar_fellenius(
        circulo=circulo,
        perfil_terreno=perfil_terreno,
        estrato=estrato,
        nivel_freatico=nivel_freatico,
        num_dovelas=num_dovelas
    )
    
    # Calcular diferencias
    diferencia_fs = resultado_bishop.factor_seguridad - resultado_fellenius.factor_seguridad
    diferencia_porcentual = (diferencia_fs / resultado_fellenius.factor_seguridad) * 100
    
    # Determinar método más conservador
    mas_conservador = "Fellenius" if resultado_fellenius.factor_seguridad < resultado_bishop.factor_seguridad else "Bishop"
    
    return {
        'bishop': resultado_bishop,
        'fellenius': resultado_fellenius,
        'factor_seguridad_bishop': resultado_bishop.factor_seguridad,
        'factor_seguridad_fellenius': resultado_fellenius.factor_seguridad,
        'diferencia_absoluta': diferencia_fs,
        'diferencia_porcentual': diferencia_porcentual,
        'mas_conservador': mas_conservador,
        'iteraciones_bishop': resultado_bishop.iteraciones,
        'convergio_bishop': resultado_bishop.convergio,
        'dovelas_traccion_bishop': resultado_bishop.detalles_calculo['dovelas_en_traccion'],
        'dovelas_traccion_fellenius': resultado_fellenius.detalles_calculo['dovelas_en_traccion'],
        'momento_resistente_bishop': resultado_bishop.momento_resistente,
        'momento_resistente_fellenius': resultado_fellenius.momento_resistente,
        'momento_actuante_bishop': resultado_bishop.momento_actuante,
        'momento_actuante_fellenius': resultado_fellenius.momento_actuante,
        'recomendacion': _generar_recomendacion_comparacion(resultado_bishop, resultado_fellenius, diferencia_porcentual)
    }


def _generar_recomendacion_comparacion(bishop: ResultadoBishop, 
                                     fellenius, 
                                     diferencia_porcentual: float) -> str:
    """
    Genera recomendación basada en la comparación de métodos.
    
    Args:
        bishop: Resultado de Bishop
        fellenius: Resultado de Fellenius
        diferencia_porcentual: Diferencia porcentual entre métodos
        
    Returns:
        Recomendación textual
    """
    recomendaciones = []
    
    # Análisis de convergencia
    if not bishop.convergio:
        recomendaciones.append("⚠️ Bishop no convergió - usar Fellenius como referencia")
    elif bishop.iteraciones > 20:
        recomendaciones.append("⚡ Bishop requirió muchas iteraciones - verificar parámetros")
    
    # Análisis de diferencia
    if abs(diferencia_porcentual) < 5:
        recomendaciones.append("✅ Diferencia < 5% - ambos métodos son confiables")
    elif abs(diferencia_porcentual) < 15:
        recomendaciones.append("⚡ Diferencia moderada - preferir Bishop para mayor precisión")
    else:
        recomendaciones.append("⚠️ Gran diferencia - revisar geometría y parámetros")
    
    # Análisis de tracción
    traccion_bishop = bishop.detalles_calculo['dovelas_en_traccion']
    traccion_fellenius = fellenius.detalles_calculo['dovelas_en_traccion']
    
    if traccion_bishop > traccion_fellenius:
        recomendaciones.append("🔍 Bishop detecta más tracción - superficie de falla problemática")
    elif traccion_bishop < traccion_fellenius:
        recomendaciones.append("✅ Bishop maneja mejor las fuerzas entre dovelas")
    
    # Análisis de estabilidad
    if bishop.factor_seguridad < 1.0 and fellenius.factor_seguridad >= 1.0:
        recomendaciones.append("⚠️ Solo Bishop indica inestabilidad - análisis crítico necesario")
    elif bishop.factor_seguridad >= 1.0 and fellenius.factor_seguridad < 1.0:
        recomendaciones.append("⚠️ Solo Fellenius indica inestabilidad - verificar con Bishop")
    
    # Recomendación final
    if bishop.es_valido and fellenius.es_valido:
        if abs(diferencia_porcentual) < 10:
            recomendaciones.append("🎯 RECOMENDACIÓN: Usar Bishop como resultado principal")
        else:
            recomendaciones.append("🎯 RECOMENDACIÓN: Investigar causa de gran diferencia")
    elif bishop.es_valido:
        recomendaciones.append("🎯 RECOMENDACIÓN: Usar solo Bishop (Fellenius inválido)")
    elif fellenius.es_valido:
        recomendaciones.append("🎯 RECOMENDACIÓN: Usar solo Fellenius (Bishop inválido)")
    else:
        recomendaciones.append("🎯 RECOMENDACIÓN: Revisar completamente geometría y parámetros")
    
    return " | ".join(recomendaciones)


def generar_reporte_comparacion(comparacion: Dict[str, Any]) -> str:
    """
    Genera un reporte comparativo entre Bishop y Fellenius.
    
    Args:
        comparacion: Diccionario con resultados de comparación
        
    Returns:
        Reporte en formato texto
    """
    reporte = []
    reporte.append("=" * 70)
    reporte.append("COMPARACIÓN: BISHOP MODIFICADO vs FELLENIUS")
    reporte.append("=" * 70)
    
    # Resultados principales
    reporte.append(f"\n📊 FACTORES DE SEGURIDAD:")
    reporte.append(f"   Bishop Modificado: {comparacion['factor_seguridad_bishop']:.3f}")
    reporte.append(f"   Fellenius:         {comparacion['factor_seguridad_fellenius']:.3f}")
    reporte.append(f"   Diferencia:        {comparacion['diferencia_absoluta']:+.3f}")
    reporte.append(f"   Diferencia %:      {comparacion['diferencia_porcentual']:+.1f}%")
    reporte.append(f"   Más conservador:   {comparacion['mas_conservador']}")
    
    # Convergencia de Bishop
    reporte.append(f"\n🔄 CONVERGENCIA DE BISHOP:")
    reporte.append(f"   Convergió: {'SÍ' if comparacion['convergio_bishop'] else 'NO'}")
    reporte.append(f"   Iteraciones: {comparacion['iteraciones_bishop']}")
    
    # Momentos
    reporte.append(f"\n🔄 MOMENTOS RESISTENTES:")
    reporte.append(f"   Bishop:    {comparacion['momento_resistente_bishop']:.1f} kN·m")
    reporte.append(f"   Fellenius: {comparacion['momento_resistente_fellenius']:.1f} kN·m")
    
    reporte.append(f"\n🔄 MOMENTOS ACTUANTES:")
    reporte.append(f"   Bishop:    {comparacion['momento_actuante_bishop']:.1f} kN·m")
    reporte.append(f"   Fellenius: {comparacion['momento_actuante_fellenius']:.1f} kN·m")
    
    # Dovelas en tracción
    reporte.append(f"\n🧱 DOVELAS EN TRACCIÓN:")
    reporte.append(f"   Bishop:    {comparacion['dovelas_traccion_bishop']}")
    reporte.append(f"   Fellenius: {comparacion['dovelas_traccion_fellenius']}")
    
    # Recomendación
    reporte.append(f"\n💡 ANÁLISIS Y RECOMENDACIONES:")
    recomendaciones = comparacion['recomendacion'].split(' | ')
    for i, rec in enumerate(recomendaciones, 1):
        reporte.append(f"   {i}. {rec}")
    
    reporte.append("\n" + "=" * 70)
    reporte.append("NOTAS TÉCNICAS:")
    reporte.append("• Bishop es más preciso (considera fuerzas entre dovelas)")
    reporte.append("• Fellenius es más conservador (asume fuerzas nulas)")
    reporte.append("• Diferencias > 15% requieren revisión de parámetros")
    reporte.append("• Bishop requiere convergencia iterativa")
    reporte.append("=" * 70)
    
    return "\n".join(reporte)
