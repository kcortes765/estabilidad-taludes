"""
Geometría Avanzada de Círculos para Análisis de Estabilidad de Taludes

Este módulo proporciona herramientas completas para:
- Validación geométrica de círculos
- Cálculo de intersecciones con terreno
- Optimización de posición y radio
- Análisis de dovelas válidas
- Diagnóstico visual

Autor: Sistema de Análisis de Taludes
"""

import math
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

from data.models import CirculoFalla, Estrato
from core.geometry import crear_dovelas


class TipoValidacion(Enum):
    """Tipos de validación geométrica"""
    INTERSECCION_TERRENO = "interseccion_terreno"
    COBERTURA_SUFICIENTE = "cobertura_suficiente" 
    POSICION_CENTRO = "posicion_centro"
    RADIO_APROPIADO = "radio_apropiado"
    DOVELAS_VALIDAS = "dovelas_validas"
    FUERZAS_POSITIVAS = "fuerzas_positivas"


@dataclass
class ResultadoValidacionCirculo:
    """Resultado de validación de círculo"""
    es_valido: bool
    tipo: TipoValidacion
    mensaje: str
    valor_calculado: Optional[float] = None
    valor_minimo: Optional[float] = None
    valor_maximo: Optional[float] = None
    severidad: str = "INFO"  # INFO, WARNING, ERROR


@dataclass
class MetricasCirculo:
    """Métricas calculadas para un círculo"""
    centro_x: float
    centro_y: float
    radio: float
    longitud_interseccion: float
    cobertura_terreno: float
    num_dovelas_validas: int
    num_dovelas_total: int
    porcentaje_dovelas_validas: float
    suma_fuerzas_actuantes: float
    factor_seguridad: Optional[float] = None
    es_geometricamente_valido: bool = False
    es_computacionalmente_valido: bool = False


class GeometriaCirculoAvanzada:
    """Clase principal para manejo avanzado de geometría de círculos"""
    
    def __init__(self, tolerancia_interseccion: float = 0.1):
        self.tolerancia_interseccion = tolerancia_interseccion
        
    def calcular_intersecciones_circulo_terreno(self, 
                                               circulo: CirculoFalla, 
                                               perfil_terreno: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Calcula todas las intersecciones entre el círculo y el perfil del terreno.
        
        Returns:
            Lista de puntos de intersección (x, y)
        """
        intersecciones = []
        
        for i in range(len(perfil_terreno) - 1):
            p1 = perfil_terreno[i]
            p2 = perfil_terreno[i + 1]
            
            # Calcular intersecciones del segmento con el círculo
            puntos_interseccion = self._interseccion_segmento_circulo(p1, p2, circulo)
            intersecciones.extend(puntos_interseccion)
            
        return intersecciones
    
    def _interseccion_segmento_circulo(self, 
                                      p1: Tuple[float, float], 
                                      p2: Tuple[float, float],
                                      circulo: CirculoFalla) -> List[Tuple[float, float]]:
        """Calcula intersección entre segmento de línea y círculo"""
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = circulo.centro_x, circulo.centro_y
        r = circulo.radio
        
        # Convertir a ecuación paramétrica
        dx = x2 - x1
        dy = y2 - y1
        
        # Coeficientes de la ecuación cuadrática
        a = dx*dx + dy*dy
        b = 2 * (dx*(x1 - cx) + dy*(y1 - cy))
        c = (x1 - cx)**2 + (y1 - cy)**2 - r**2
        
        discriminante = b*b - 4*a*c
        
        if discriminante < 0:
            return []  # No hay intersección
            
        intersecciones = []
        sqrt_disc = math.sqrt(discriminante)
        
        for signo in [-1, 1]:
            t = (-b + signo * sqrt_disc) / (2*a)
            
            # Verificar que esté dentro del segmento (0 <= t <= 1)
            if 0 <= t <= 1:
                x_int = x1 + t * dx
                y_int = y1 + t * dy
                intersecciones.append((x_int, y_int))
                
        return intersecciones
    
    def calcular_longitud_arco_terreno(self, 
                                      circulo: CirculoFalla, 
                                      perfil_terreno: List[Tuple[float, float]]) -> float:
        """
        Calcula la longitud del arco del círculo que está por debajo del terreno.
        """
        intersecciones = self.calcular_intersecciones_circulo_terreno(circulo, perfil_terreno)
        
        if len(intersecciones) < 2:
            return 0.0
            
        # Tomar las intersecciones más extremas
        intersecciones.sort(key=lambda p: p[0])  # Ordenar por x
        p1 = intersecciones[0]
        p2 = intersecciones[-1]
        
        # Calcular ángulos desde el centro del círculo
        angulo1 = math.atan2(p1[1] - circulo.centro_y, p1[0] - circulo.centro_x)
        angulo2 = math.atan2(p2[1] - circulo.centro_y, p2[0] - circulo.centro_x)
        
        # Calcular diferencia de ángulos (considerar wrapping)
        diff_angulo = abs(angulo2 - angulo1)
        if diff_angulo > math.pi:
            diff_angulo = 2 * math.pi - diff_angulo
            
        # Longitud del arco = radio * ángulo
        return circulo.radio * diff_angulo
    
    def validar_circulo_completo(self, 
                                circulo: CirculoFalla,
                                perfil_terreno: List[Tuple[float, float]],
                                estrato: Estrato,
                                num_dovelas: int = 10) -> List[ResultadoValidacionCirculo]:
        """
        Validación completa de un círculo de falla.
        
        Returns:
            Lista de resultados de validación
        """
        resultados = []
        
        # 1. Validar intersección con terreno
        intersecciones = self.calcular_intersecciones_circulo_terreno(circulo, perfil_terreno)
        
        resultado_interseccion = ResultadoValidacionCirculo(
            es_valido=len(intersecciones) >= 2,
            tipo=TipoValidacion.INTERSECCION_TERRENO,
            mensaje=f"Intersecciones encontradas: {len(intersecciones)}",
            valor_calculado=len(intersecciones),
            valor_minimo=2,
            severidad="ERROR" if len(intersecciones) < 2 else "INFO"
        )
        resultados.append(resultado_interseccion)
        
        # 2. Validar cobertura suficiente
        longitud_arco = self.calcular_longitud_arco_terreno(circulo, perfil_terreno)
        cobertura_minima = circulo.radio * 0.5  # Al menos 50% del radio como arco
        
        resultado_cobertura = ResultadoValidacionCirculo(
            es_valido=longitud_arco >= cobertura_minima,
            tipo=TipoValidacion.COBERTURA_SUFICIENTE,
            mensaje=f"Longitud arco: {longitud_arco:.2f}m (mín: {cobertura_minima:.2f}m)",
            valor_calculado=longitud_arco,
            valor_minimo=cobertura_minima,
            severidad="WARNING" if longitud_arco < cobertura_minima else "INFO"
        )
        resultados.append(resultado_cobertura)
        
        # 3. Validar posición del centro
        terreno_x_min = min(p[0] for p in perfil_terreno)
        terreno_x_max = max(p[0] for p in perfil_terreno)
        terreno_y_max = max(p[1] for p in perfil_terreno)
        
        centro_valido = (terreno_x_min <= circulo.centro_x <= terreno_x_max and 
                        circulo.centro_y >= 0 and 
                        circulo.centro_y <= terreno_y_max + circulo.radio)
        
        resultado_centro = ResultadoValidacionCirculo(
            es_valido=centro_valido,
            tipo=TipoValidacion.POSICION_CENTRO,
            mensaje=f"Centro ({circulo.centro_x:.1f}, {circulo.centro_y:.1f}) dentro de rango válido",
            severidad="ERROR" if not centro_valido else "INFO"
        )
        resultados.append(resultado_centro)
        
        # 4. Validar radio apropiado
        distancia_terreno = math.sqrt((circulo.centro_x - terreno_x_min)**2 + 
                                     (circulo.centro_y - terreno_y_max)**2)
        radio_minimo = distancia_terreno * 0.5
        radio_maximo = distancia_terreno * 3.0
        
        radio_valido = radio_minimo <= circulo.radio <= radio_maximo
        
        resultado_radio = ResultadoValidacionCirculo(
            es_valido=radio_valido,
            tipo=TipoValidacion.RADIO_APROPIADO,
            mensaje=f"Radio {circulo.radio:.1f}m (rango: {radio_minimo:.1f}-{radio_maximo:.1f}m)",
            valor_calculado=circulo.radio,
            valor_minimo=radio_minimo,
            valor_maximo=radio_maximo,
            severidad="WARNING" if not radio_valido else "INFO"
        )
        resultados.append(resultado_radio)
        
        # 5. Intentar crear dovelas y validar
        try:
            dovelas = crear_dovelas(circulo, perfil_terreno, estrato, num_dovelas)
            num_validas = len(dovelas)
            porcentaje_validas = (num_validas / num_dovelas) * 100
            
            resultado_dovelas = ResultadoValidacionCirculo(
                es_valido=porcentaje_validas >= 70,  # Al menos 70% válidas
                tipo=TipoValidacion.DOVELAS_VALIDAS,
                mensaje=f"Dovelas válidas: {num_validas}/{num_dovelas} ({porcentaje_validas:.1f}%)",
                valor_calculado=porcentaje_validas,
                valor_minimo=70,
                severidad="ERROR" if porcentaje_validas < 70 else "INFO"
            )
            resultados.append(resultado_dovelas)
            
        except Exception as e:
            resultado_dovelas = ResultadoValidacionCirculo(
                es_valido=False,
                tipo=TipoValidacion.DOVELAS_VALIDAS,
                mensaje=f"Error creando dovelas: {str(e)}",
                severidad="ERROR"
            )
            resultados.append(resultado_dovelas)
        
        return resultados
    
    def calcular_metricas_circulo(self, 
                                 circulo: CirculoFalla,
                                 perfil_terreno: List[Tuple[float, float]],
                                 estrato: Estrato,
                                 num_dovelas: int = 10) -> MetricasCirculo:
        """
        Calcula métricas completas para un círculo.
        """
        # Validaciones
        validaciones = self.validar_circulo_completo(circulo, perfil_terreno, estrato, num_dovelas)
        
        # Métricas geométricas
        longitud_interseccion = self.calcular_longitud_arco_terreno(circulo, perfil_terreno)
        cobertura_terreno = longitud_interseccion / (2 * math.pi * circulo.radio) * 100
        
        # Métricas de dovelas
        num_dovelas_validas = 0
        suma_fuerzas_actuantes = 0
        factor_seguridad = None
        
        try:
            dovelas = crear_dovelas(circulo, perfil_terreno, estrato, num_dovelas)
            num_dovelas_validas = len(dovelas)
            
            # Calcular suma de fuerzas actuantes
            for dovela in dovelas:
                suma_fuerzas_actuantes += dovela.peso * math.sin(math.radians(dovela.angulo_base))
                
        except Exception:
            pass
        
        porcentaje_dovelas_validas = (num_dovelas_validas / num_dovelas) * 100
        
        # Validez geométrica y computacional
        es_geometricamente_valido = all(v.es_valido for v in validaciones 
                                       if v.tipo in [TipoValidacion.INTERSECCION_TERRENO, 
                                                    TipoValidacion.POSICION_CENTRO])
        
        es_computacionalmente_valido = all(v.es_valido for v in validaciones 
                                          if v.tipo in [TipoValidacion.DOVELAS_VALIDAS])
        
        return MetricasCirculo(
            centro_x=circulo.centro_x,
            centro_y=circulo.centro_y,
            radio=circulo.radio,
            longitud_interseccion=longitud_interseccion,
            cobertura_terreno=cobertura_terreno,
            num_dovelas_validas=num_dovelas_validas,
            num_dovelas_total=num_dovelas,
            porcentaje_dovelas_validas=porcentaje_dovelas_validas,
            suma_fuerzas_actuantes=suma_fuerzas_actuantes,
            factor_seguridad=factor_seguridad,
            es_geometricamente_valido=es_geometricamente_valido,
            es_computacionalmente_valido=es_computacionalmente_valido
        )


def generar_circulos_candidatos(perfil_terreno: List[Tuple[float, float]], 
                               densidad: int = 5) -> List[CirculoFalla]:
    """
    Genera una grilla de círculos candidatos para optimización.
    
    Args:
        perfil_terreno: Perfil del terreno
        densidad: Número de puntos por dimensión en la grilla
        
    Returns:
        Lista de círculos candidatos
    """
    # Calcular límites del terreno
    x_min = min(p[0] for p in perfil_terreno)
    x_max = max(p[0] for p in perfil_terreno)
    y_min = min(p[1] for p in perfil_terreno)
    y_max = max(p[1] for p in perfil_terreno)
    
    # Expandir área de búsqueda
    margen_x = (x_max - x_min) * 0.3
    margen_y = (y_max - y_min) * 0.5
    
    # Rangos para centro
    centros_x = np.linspace(x_min - margen_x, x_max + margen_x, densidad)
    centros_y = np.linspace(y_max, y_max + margen_y, densidad)
    
    # Rangos para radio
    diagonal_terreno = math.sqrt((x_max - x_min)**2 + (y_max - y_min)**2)
    radios = np.linspace(diagonal_terreno * 0.3, diagonal_terreno * 1.5, densidad)
    
    circulos = []
    for cx in centros_x:
        for cy in centros_y:
            for r in radios:
                circulos.append(CirculoFalla(cx, cy, r))
                
    return circulos
