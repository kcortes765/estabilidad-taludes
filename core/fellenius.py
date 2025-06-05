"""
Implementación del método de Fellenius para análisis de estabilidad de taludes.

El método de Fellenius (también conocido como método sueco o método ordinario) 
es un método de equilibrio límite que asume que las fuerzas entre dovelas son nulas.
Es un método directo (no iterativo) que proporciona una solución conservadora.

Ecuación principal:
Fs = Σ[c'·ΔL + (W·cos(α) - u·ΔL)·tan(φ')] / Σ[W·sin(α)]

Donde:
- c': cohesión efectiva
- ΔL: longitud del arco de la dovela
- W: peso de la dovela
- α: ángulo de la tangente al círculo en el centro de la dovela
- u: presión de poros
- φ': ángulo de fricción efectiva
"""

import math
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass

from data.models import Estrato, Dovela, CirculoFalla
from data.validation import (
    validar_entrada_completa, validar_conjunto_dovelas, 
    validar_factor_seguridad, lanzar_si_invalido, ValidacionError
)
from core.geometry import crear_dovelas


@dataclass
class ResultadoFellenius:
    """
    Resultado del análisis por método de Fellenius.
    
    Attributes:
        factor_seguridad: Factor de seguridad calculado
        momento_resistente: Momento resistente total (kN·m)
        momento_actuante: Momento actuante total (kN·m)
        dovelas: Lista de dovelas analizadas
        fuerzas_resistentes: Fuerzas resistentes por dovela (kN)
        fuerzas_actuantes: Fuerzas actuantes por dovela (kN)
        es_valido: Indica si el resultado es válido
        advertencias: Lista de advertencias del análisis
        detalles_calculo: Diccionario con detalles del cálculo
    """
    factor_seguridad: float
    momento_resistente: float
    momento_actuante: float
    dovelas: List[Dovela]
    fuerzas_resistentes: List[float]
    fuerzas_actuantes: List[float]
    es_valido: bool
    advertencias: List[str]
    detalles_calculo: Dict[str, Any]


def calcular_fuerza_resistente_dovela(dovela: Dovela) -> float:
    """
    Calcula la fuerza resistente de una dovela según Fellenius.
    
    Fuerza resistente = c'·ΔL + (W·cos(α) - u·ΔL)·tan(φ')
    
    Args:
        dovela: Dovela a analizar
        
    Returns:
        Fuerza resistente en kN
        
    Raises:
        ValidacionError: Si la dovela no es válida
    """
    from data.validation import validar_dovela_critica
    
    # Validar dovela
    resultado_validacion = validar_dovela_critica(dovela)
    if not resultado_validacion.es_valido:
        raise ValidacionError(f"Dovela inválida: {resultado_validacion.mensaje}")
    
    # Componente de cohesión
    fuerza_cohesion = dovela.cohesion * dovela.longitud_arco
    
    # Fuerza normal efectiva
    fuerza_normal = dovela.peso * dovela.cos_alpha
    fuerza_poros = dovela.presion_poros * dovela.longitud_arco
    fuerza_normal_efectiva = fuerza_normal - fuerza_poros
    
    # Componente de fricción
    fuerza_friccion = fuerza_normal_efectiva * dovela.tan_phi
    
    # Fuerza resistente total
    fuerza_resistente = fuerza_cohesion + fuerza_friccion
    
    return max(0.0, fuerza_resistente)  # No puede ser negativa


def calcular_fuerza_actuante_dovela(dovela: Dovela) -> float:
    """
    Calcula la fuerza actuante de una dovela según Fellenius.
    
    Fuerza actuante = W·sin(α)
    
    Args:
        dovela: Dovela a analizar
        
    Returns:
        Fuerza actuante en kN
    """
    return dovela.peso * dovela.sin_alpha


def analizar_fellenius(circulo: CirculoFalla,
                      perfil_terreno: List[Tuple[float, float]],
                      estrato: Estrato,
                      nivel_freatico: Optional[List[Tuple[float, float]]] = None,
                      num_dovelas: int = 10,
                      validar_entrada: bool = True) -> ResultadoFellenius:
    """
    Realiza el análisis de estabilidad usando el método de Fellenius.
    
    Args:
        circulo: Círculo de falla a analizar
        perfil_terreno: Perfil del terreno [(x, y), ...]
        estrato: Propiedades del suelo
        nivel_freatico: Nivel freático opcional [(x, y), ...]
        num_dovelas: Número de dovelas para discretización
        validar_entrada: Si validar datos de entrada
        
    Returns:
        Resultado del análisis de Fellenius
        
    Raises:
        ValidacionError: Si los datos de entrada son inválidos
    """
    advertencias = []
    detalles_calculo = {}
    
    # Validar entrada si se solicita
    if validar_entrada:
        validaciones = validar_entrada_completa(circulo, perfil_terreno, estrato, nivel_freatico)
        for validacion in validaciones:
            if not validacion.es_valido:
                raise ValidacionError(f"Validación falló: {validacion.mensaje}")
            elif validacion.codigo_error:  # Advertencias
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
    
    # Calcular fuerzas por dovela
    fuerzas_resistentes = []
    fuerzas_actuantes = []
    dovelas_problematicas = []
    
    for i, dovela in enumerate(dovelas):
        try:
            # Fuerza resistente
            fuerza_r = calcular_fuerza_resistente_dovela(dovela)
            fuerzas_resistentes.append(fuerza_r)
            
            # Fuerza actuante
            fuerza_a = calcular_fuerza_actuante_dovela(dovela)
            fuerzas_actuantes.append(fuerza_a)
            
            # Verificar dovelas problemáticas
            if dovela.calcular_fuerza_normal_efectiva() < 0:
                dovelas_problematicas.append(i)
                advertencias.append(f"Dovela {i} en tracción: N' = {dovela.calcular_fuerza_normal_efectiva():.1f} kN")
            
        except Exception as e:
            raise ValidacionError(f"Error calculando fuerzas en dovela {i}: {e}")
    
    # Calcular momentos totales
    momento_resistente = sum(fuerzas_resistentes) * circulo.radio
    suma_actuantes = sum(fuerzas_actuantes)
    if suma_actuantes == 0:
        raise ValidacionError("Momento actuante ≤ 0: superficie de falla inválida")
    momento_actuante = abs(suma_actuantes) * circulo.radio

    # Calcular factor de seguridad
    
    factor_seguridad = momento_resistente / momento_actuante
    
    # Validar factor de seguridad
    resultado_fs = validar_factor_seguridad(factor_seguridad)
    if not resultado_fs.es_valido:
        raise ValidacionError(f"Factor de seguridad inválido: {resultado_fs.mensaje}")
    
    # Agregar detalles del cálculo
    detalles_calculo.update({
        'num_dovelas': len(dovelas),
        'dovelas_en_traccion': len(dovelas_problematicas),
        'porcentaje_traccion': (len(dovelas_problematicas) / len(dovelas)) * 100,
        'suma_fuerzas_resistentes': sum(fuerzas_resistentes),
        'suma_fuerzas_actuantes': abs(sum(fuerzas_actuantes)),
        'radio_circulo': circulo.radio,
        'centro_circulo': (circulo.xc, circulo.yc),
        'metodo': 'Fellenius',
        'es_iterativo': False
    })
    
    # Verificar estabilidad
    es_valido = True
    if factor_seguridad < 0.5:
        advertencias.append("Factor de seguridad muy bajo: posible error en datos")
        es_valido = False
    elif len(dovelas_problematicas) > len(dovelas) // 2:
        advertencias.append(f"Muchas dovelas en tracción ({len(dovelas_problematicas)}/{len(dovelas)})")
    
    return ResultadoFellenius(
        factor_seguridad=factor_seguridad,
        momento_resistente=momento_resistente,
        momento_actuante=momento_actuante,
        dovelas=dovelas,
        fuerzas_resistentes=fuerzas_resistentes,
        fuerzas_actuantes=fuerzas_actuantes,
        es_valido=es_valido,
        advertencias=advertencias,
        detalles_calculo=detalles_calculo
    )


def generar_reporte_fellenius(resultado: ResultadoFellenius) -> str:
    """
    Genera un reporte detallado del análisis de Fellenius.
    
    Args:
        resultado: Resultado del análisis
        
    Returns:
        Reporte en formato texto
    """
    reporte = []
    reporte.append("=" * 60)
    reporte.append("ANÁLISIS DE ESTABILIDAD - MÉTODO DE FELLENIUS")
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
    reporte.append(f"   Porcentaje en tracción: {resultado.detalles_calculo['porcentaje_traccion']:.1f}%")
    
    # Advertencias
    if resultado.advertencias:
        reporte.append(f"\n⚠️ ADVERTENCIAS:")
        for i, advertencia in enumerate(resultado.advertencias, 1):
            reporte.append(f"   {i}. {advertencia}")
    
    # Validez del resultado
    reporte.append(f"\n✅ VALIDEZ DEL RESULTADO: {'VÁLIDO' if resultado.es_valido else 'INVÁLIDO'}")
    
    # Tabla de dovelas (primeras 5 y últimas 5 si hay muchas)
    reporte.append(f"\n📋 DETALLE DE DOVELAS:")
    reporte.append("   Dovela |   X    | Peso  | α(°)  | F.Res | F.Act")
    reporte.append("   -------|--------|-------|-------|-------|-------")
    
    num_dovelas = len(resultado.dovelas)
    if num_dovelas <= 10:
        # Mostrar todas las dovelas
        indices = range(num_dovelas)
    else:
        # Mostrar primeras 5 y últimas 5
        indices = list(range(5)) + list(range(num_dovelas-5, num_dovelas))
    
    for i in indices:
        if i == 5 and num_dovelas > 10:
            reporte.append("   ...    |  ...   | ...   | ...   | ...   | ...")
        
        dovela = resultado.dovelas[i]
        x = dovela.x_centro
        peso = dovela.peso
        alpha_grados = math.degrees(dovela.angulo_alpha)
        f_res = resultado.fuerzas_resistentes[i]
        f_act = resultado.fuerzas_actuantes[i]
        
        reporte.append(f"   {i+1:6d} | {x:6.1f} | {peso:5.0f} | {alpha_grados:5.1f} | {f_res:5.1f} | {f_act:5.1f}")
    
    reporte.append("\n" + "=" * 60)
    reporte.append("Método: Fellenius (Sueco) - Análisis directo")
    reporte.append("Asume fuerzas entre dovelas = 0")
    reporte.append("=" * 60)
    
    return "\n".join(reporte)


def comparar_con_factor_teorico(resultado: ResultadoFellenius, 
                               factor_teorico: float,
                               tolerancia: float = 0.1) -> Dict[str, Any]:
    """
    Compara el resultado con un factor de seguridad teórico esperado.
    
    Args:
        resultado: Resultado del análisis
        factor_teorico: Factor de seguridad esperado
        tolerancia: Tolerancia para la comparación
        
    Returns:
        Diccionario con la comparación
    """
    diferencia = abs(resultado.factor_seguridad - factor_teorico)
    diferencia_relativa = diferencia / factor_teorico * 100
    
    es_consistente = diferencia <= tolerancia
    
    return {
        'factor_calculado': resultado.factor_seguridad,
        'factor_teorico': factor_teorico,
        'diferencia_absoluta': diferencia,
        'diferencia_relativa_pct': diferencia_relativa,
        'tolerancia': tolerancia,
        'es_consistente': es_consistente,
        'mensaje': f"Diferencia: {diferencia:.3f} ({diferencia_relativa:.1f}%) - {'✅ CONSISTENTE' if es_consistente else '❌ INCONSISTENTE'}"
    }


# Funciones auxiliares para casos comunes

def fellenius_talud_homogeneo(altura: float,
                             angulo_talud: float,
                             cohesion: float,
                             phi_grados: float,
                             gamma: float,
                             factor_radio: float = 1.5,
                             num_dovelas: int = 10) -> ResultadoFellenius:
    """
    Análisis de Fellenius para un talud homogéneo simple.
    
    Args:
        altura: Altura del talud (m)
        angulo_talud: Ángulo del talud en grados
        cohesion: Cohesión del suelo (kPa)
        phi_grados: Ángulo de fricción (grados)
        gamma: Peso específico (kN/m³)
        factor_radio: Factor para calcular radio (radio = factor_radio * altura)
        num_dovelas: Número de dovelas
        
    Returns:
        Resultado del análisis
    """
    from core.geometry import crear_perfil_simple
    
    # Crear geometría simple
    longitud_base = altura / math.tan(math.radians(angulo_talud))
    perfil = crear_perfil_simple(0.0, altura, longitud_base * 2, 0.0, 20)
    
    # Círculo de falla
    radio = factor_radio * altura
    xc = longitud_base * 0.7  # Centro hacia atrás del pie del talud
    yc = altura * 0.8  # Centro arriba del terreno
    circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
    
    # Estrato homogéneo
    estrato = Estrato(cohesion=cohesion, phi_grados=phi_grados, gamma=gamma, nombre="Homogéneo")
    
    return analizar_fellenius(circulo, perfil, estrato, num_dovelas=num_dovelas)


def fellenius_con_nivel_freatico(altura: float,
                                angulo_talud: float,
                                cohesion: float,
                                phi_grados: float,
                                gamma: float,
                                gamma_sat: float,
                                profundidad_freatico: float,
                                factor_radio: float = 1.5,
                                num_dovelas: int = 10) -> ResultadoFellenius:
    """
    Análisis de Fellenius con nivel freático.
    
    Args:
        altura: Altura del talud (m)
        angulo_talud: Ángulo del talud en grados
        cohesion: Cohesión del suelo (kPa)
        phi_grados: Ángulo de fricción (grados)
        gamma: Peso específico natural (kN/m³)
        gamma_sat: Peso específico saturado (kN/m³)
        profundidad_freatico: Profundidad del nivel freático desde la superficie (m)
        factor_radio: Factor para calcular radio
        num_dovelas: Número de dovelas
        
    Returns:
        Resultado del análisis
    """
    from core.geometry import crear_perfil_simple, crear_nivel_freatico_horizontal
    
    # Crear geometría
    longitud_base = altura / math.tan(math.radians(angulo_talud))
    perfil = crear_perfil_simple(0.0, altura, longitud_base * 2, 0.0, 20)
    
    # Nivel freático
    nivel_freatico = crear_nivel_freatico_horizontal(
        x_inicio=0.0,
        x_fin=longitud_base * 2,
        elevacion=altura - profundidad_freatico,
        num_puntos=10,
    )
    
    # Círculo de falla
    radio = factor_radio * altura
    xc = longitud_base * 0.7
    yc = altura * 0.8
    circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
    
    # Estrato con peso específico saturado
    estrato = Estrato(
        cohesion=cohesion, 
        phi_grados=phi_grados, 
        gamma=gamma,
        gamma_sat=gamma_sat,
        nombre="Con nivel freático"
    )
    
    return analizar_fellenius(
        circulo, perfil, estrato, 
        nivel_freatico=nivel_freatico, 
        num_dovelas=num_dovelas
    )
