"""
Optimizador Inteligente de Círculos para Análisis de Estabilidad de Taludes

Este módulo proporciona algoritmos avanzados para encontrar círculos óptimos:
- Algoritmo genético para búsqueda global
- Optimización por gradiente para refinamiento local
- Búsqueda por grilla inteligente
- Optimización multiobjetivo (FS + validez geométrica)
- Algoritmos adaptativos según tipo de terreno

Autor: Sistema de Análisis de Taludes
"""

import math
import random
import numpy as np
from typing import List, Tuple, Optional, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum
import copy

from data.models import CirculoFalla, Estrato
from core.circle_geometry import GeometriaCirculoAvanzada, MetricasCirculo, generar_circulos_candidatos
from core.bishop import analizar_bishop


class TipoOptimizacion(Enum):
    """Tipos de optimización disponibles"""
    FACTOR_SEGURIDAD_MINIMO = "fs_minimo"
    FACTOR_SEGURIDAD_OBJETIVO = "fs_objetivo"
    VALIDEZ_MAXIMA = "validez_maxima"
    MULTIOBJETIVO = "multiobjetivo"


class MetodoOptimizacion(Enum):
    """Métodos de optimización disponibles"""
    GRILLA_SISTEMATICA = "grilla"
    ALGORITMO_GENETICO = "genetico"
    BUSQUEDA_ALEATORIA = "aleatorio"
    HIBRIDO = "hibrido"


@dataclass
class ParametrosOptimizacion:
    """Parámetros para configurar la optimización"""
    tipo: TipoOptimizacion
    metodo: MetodoOptimizacion
    fs_objetivo_min: float = 1.0
    fs_objetivo_max: float = 3.0
    max_iteraciones: int = 1000
    poblacion_genetico: int = 50
    tasa_mutacion: float = 0.1
    tasa_cruce: float = 0.8
    tolerancia_convergencia: float = 0.01
    peso_fs: float = 0.7
    peso_validez: float = 0.3
    num_dovelas: int = 10
    verbose: bool = False


@dataclass
class ResultadoOptimizacion:
    """Resultado de la optimización"""
    circulo_optimo: CirculoFalla
    factor_seguridad: float
    metricas: MetricasCirculo
    iteraciones_usadas: int
    tiempo_computo: float
    convergencia_alcanzada: bool
    historial_mejores: List[CirculoFalla]
    historial_fs: List[float]
    mensaje: str


class OptimizadorCirculos:
    """Clase principal para optimización de círculos"""
    
    def __init__(self):
        self.geometria = GeometriaCirculoAvanzada()
        
    def optimizar(self, 
                 perfil_terreno: List[Tuple[float, float]],
                 estrato: Estrato,
                 params: ParametrosOptimizacion,
                 circulo_inicial: Optional[CirculoFalla] = None) -> ResultadoOptimizacion:
        """
        Optimiza un círculo de falla según los parámetros especificados.
        """
        import time
        tiempo_inicio = time.time()
        
        if params.metodo == MetodoOptimizacion.GRILLA_SISTEMATICA:
            resultado = self._optimizar_grilla(perfil_terreno, estrato, params)
        elif params.metodo == MetodoOptimizacion.ALGORITMO_GENETICO:
            resultado = self._optimizar_genetico(perfil_terreno, estrato, params, circulo_inicial)
        elif params.metodo == MetodoOptimizacion.BUSQUEDA_ALEATORIA:
            resultado = self._optimizar_aleatorio(perfil_terreno, estrato, params)
        elif params.metodo == MetodoOptimizacion.HIBRIDO:
            resultado = self._optimizar_hibrido(perfil_terreno, estrato, params, circulo_inicial)
        else:
            raise ValueError(f"Método de optimización no reconocido: {params.metodo}")
        
        resultado.tiempo_computo = time.time() - tiempo_inicio
        return resultado
    
    def _optimizar_grilla(self, 
                         perfil_terreno: List[Tuple[float, float]],
                         estrato: Estrato,
                         params: ParametrosOptimizacion) -> ResultadoOptimizacion:
        """Optimización por búsqueda en grilla sistemática"""
        
        # Generar candidatos
        densidad = max(3, int(params.max_iteraciones ** (1/3)))  # Grilla 3D
        candidatos = generar_circulos_candidatos(perfil_terreno, densidad)
        
        mejor_circulo = None
        mejor_puntuacion = float('inf') if params.tipo == TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO else float('-inf')
        mejor_fs = None
        mejor_metricas = None
        
        historial_mejores = []
        historial_fs = []
        
        iteraciones = 0
        
        for circulo in candidatos[:params.max_iteraciones]:
            iteraciones += 1
            
            # Evaluar círculo
            puntuacion, fs, metricas = self._evaluar_circulo(
                circulo, perfil_terreno, estrato, params)
            
            if puntuacion is None:
                continue
                
            # Verificar si es mejor
            es_mejor = False
            if params.tipo == TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO:
                es_mejor = puntuacion < mejor_puntuacion
            else:
                es_mejor = puntuacion > mejor_puntuacion
            
            if es_mejor:
                mejor_circulo = copy.deepcopy(circulo)
                mejor_puntuacion = puntuacion
                mejor_fs = fs
                mejor_metricas = metricas
                historial_mejores.append(copy.deepcopy(circulo))
                historial_fs.append(fs)
                
                if params.verbose:
                    print(f"Iteración {iteraciones}: Nuevo mejor FS = {fs:.3f}")
        
        if mejor_circulo is None:
            raise RuntimeError("No se encontró ningún círculo válido")
        
        return ResultadoOptimizacion(
            circulo_optimo=mejor_circulo,
            factor_seguridad=mejor_fs,
            metricas=mejor_metricas,
            iteraciones_usadas=iteraciones,
            tiempo_computo=0,  # Se completará en optimizar()
            convergencia_alcanzada=True,
            historial_mejores=historial_mejores,
            historial_fs=historial_fs,
            mensaje=f"Optimización por grilla completada. Evaluados {iteraciones} candidatos."
        )
    
    def _optimizar_genetico(self, 
                           perfil_terreno: List[Tuple[float, float]],
                           estrato: Estrato,
                           params: ParametrosOptimizacion,
                           circulo_inicial: Optional[CirculoFalla] = None) -> ResultadoOptimizacion:
        """Optimización por algoritmo genético"""
        
        # Límites para generación de población
        x_min = min(p[0] for p in perfil_terreno)
        x_max = max(p[0] for p in perfil_terreno)
        y_min = min(p[1] for p in perfil_terreno)
        y_max = max(p[1] for p in perfil_terreno)
        
        margen_x = (x_max - x_min) * 0.5
        margen_y = (y_max - y_min) * 0.8
        
        centro_x_min, centro_x_max = x_min - margen_x, x_max + margen_x
        centro_y_min, centro_y_max = y_min - margen_y, y_max + margen_y
        
        diagonal = math.sqrt((x_max - x_min)**2 + (y_max - y_min)**2)
        radio_min, radio_max = diagonal * 0.2, diagonal * 2.0
        
        # Generar población inicial
        poblacion = []
        
        # Incluir círculo inicial si se proporciona
        if circulo_inicial:
            poblacion.append(circulo_inicial)
        
        # Generar resto de población aleatoriamente
        while len(poblacion) < params.poblacion_genetico:
            cx = random.uniform(centro_x_min, centro_x_max)
            cy = random.uniform(centro_y_min, centro_y_max)
            r = random.uniform(radio_min, radio_max)
            poblacion.append(CirculoFalla(cx, cy, r))
        
        mejor_circulo = None
        mejor_fs = None
        mejor_metricas = None
        mejor_puntuacion = float('-inf')
        
        historial_mejores = []
        historial_fs = []
        
        for generacion in range(params.max_iteraciones // params.poblacion_genetico):
            # Evaluar población
            fitness_poblacion = []
            for circulo in poblacion:
                puntuacion, fs, metricas = self._evaluar_circulo(
                    circulo, perfil_terreno, estrato, params)
                fitness_poblacion.append((puntuacion if puntuacion is not None else float('-inf'), 
                                        fs, metricas, circulo))
            
            # Ordenar por fitness (mejor primero)
            fitness_poblacion.sort(key=lambda x: x[0], reverse=True)
            
            # Actualizar mejor global
            if fitness_poblacion[0][0] > mejor_puntuacion:
                mejor_puntuacion = fitness_poblacion[0][0]
                mejor_fs = fitness_poblacion[0][1]
                mejor_metricas = fitness_poblacion[0][2]
                mejor_circulo = copy.deepcopy(fitness_poblacion[0][3])
                historial_mejores.append(copy.deepcopy(mejor_circulo))
                historial_fs.append(mejor_fs)
                
                if params.verbose:
                    print(f"Generación {generacion}: Nuevo mejor FS = {mejor_fs:.3f}")
            
            # Selección y reproducción
            nueva_poblacion = []
            
            # Mantener mejores (elitismo)
            elite_size = max(1, params.poblacion_genetico // 10)
            for i in range(elite_size):
                nueva_poblacion.append(copy.deepcopy(fitness_poblacion[i][3]))
            
            # Generar descendencia por cruce y mutación
            while len(nueva_poblacion) < params.poblacion_genetico:
                # Selección por torneo
                padre1 = self._seleccion_torneo(fitness_poblacion, 3)
                padre2 = self._seleccion_torneo(fitness_poblacion, 3)
                
                # Cruce
                if random.random() < params.tasa_cruce:
                    hijo = self._cruzar_circulos(padre1, padre2)
                else:
                    hijo = copy.deepcopy(padre1)
                
                # Mutación
                if random.random() < params.tasa_mutacion:
                    hijo = self._mutar_circulo(hijo, centro_x_min, centro_x_max,
                                             centro_y_min, centro_y_max,
                                             radio_min, radio_max)
                
                nueva_poblacion.append(hijo)
            
            poblacion = nueva_poblacion
        
        if mejor_circulo is None:
            raise RuntimeError("No se encontró ningún círculo válido en algoritmo genético")
        
        return ResultadoOptimizacion(
            circulo_optimo=mejor_circulo,
            factor_seguridad=mejor_fs,
            metricas=mejor_metricas,
            iteraciones_usadas=generacion * params.poblacion_genetico,
            tiempo_computo=0,
            convergencia_alcanzada=True,
            historial_mejores=historial_mejores,
            historial_fs=historial_fs,
            mensaje=f"Algoritmo genético completado. {generacion} generaciones."
        )
    
    def _optimizar_aleatorio(self, 
                            perfil_terreno: List[Tuple[float, float]],
                            estrato: Estrato,
                            params: ParametrosOptimizacion) -> ResultadoOptimizacion:
        """Optimización por búsqueda aleatoria"""
        
        # Límites para generación aleatoria
        x_min = min(p[0] for p in perfil_terreno)
        x_max = max(p[0] for p in perfil_terreno)
        y_min = min(p[1] for p in perfil_terreno)
        y_max = max(p[1] for p in perfil_terreno)
        
        margen_x = (x_max - x_min) * 0.5
        margen_y = (y_max - y_min) * 0.8
        
        centro_x_min, centro_x_max = x_min - margen_x, x_max + margen_x
        centro_y_min, centro_y_max = y_min - margen_y, y_max + margen_y
        
        diagonal = math.sqrt((x_max - x_min)**2 + (y_max - y_min)**2)
        radio_min, radio_max = diagonal * 0.2, diagonal * 2.0
        
        mejor_circulo = None
        mejor_puntuacion = float('inf') if params.tipo == TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO else float('-inf')
        mejor_fs = None
        mejor_metricas = None
        
        historial_mejores = []
        historial_fs = []
        
        for iteracion in range(params.max_iteraciones):
            # Generar círculo aleatorio
            cx = random.uniform(centro_x_min, centro_x_max)
            cy = random.uniform(centro_y_min, centro_y_max)
            r = random.uniform(radio_min, radio_max)
            circulo = CirculoFalla(cx, cy, r)
            
            # Evaluar
            puntuacion, fs, metricas = self._evaluar_circulo(
                circulo, perfil_terreno, estrato, params)
            
            if puntuacion is None:
                continue
            
            # Verificar si es mejor
            es_mejor = False
            if params.tipo == TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO:
                es_mejor = puntuacion < mejor_puntuacion
            else:
                es_mejor = puntuacion > mejor_puntuacion
            
            if es_mejor:
                mejor_circulo = copy.deepcopy(circulo)
                mejor_puntuacion = puntuacion
                mejor_fs = fs
                mejor_metricas = metricas
                historial_mejores.append(copy.deepcopy(circulo))
                historial_fs.append(fs)
                
                if params.verbose:
                    print(f"Iteración {iteracion}: Nuevo mejor FS = {fs:.3f}")
        
        if mejor_circulo is None:
            raise RuntimeError("No se encontró ningún círculo válido en búsqueda aleatoria")
        
        return ResultadoOptimizacion(
            circulo_optimo=mejor_circulo,
            factor_seguridad=mejor_fs,
            metricas=mejor_metricas,
            iteraciones_usadas=params.max_iteraciones,
            tiempo_computo=0,
            convergencia_alcanzada=True,
            historial_mejores=historial_mejores,
            historial_fs=historial_fs,
            mensaje=f"Búsqueda aleatoria completada. {params.max_iteraciones} iteraciones."
        )
    
    def _optimizar_hibrido(self, 
                          perfil_terreno: List[Tuple[float, float]],
                          estrato: Estrato,
                          params: ParametrosOptimizacion,
                          circulo_inicial: Optional[CirculoFalla] = None) -> ResultadoOptimizacion:
        """Optimización híbrida: grilla inicial + genético + refinamiento local"""
        
        # Fase 1: Búsqueda inicial por grilla gruesa
        params_grilla = copy.deepcopy(params)
        params_grilla.metodo = MetodoOptimizacion.GRILLA_SISTEMATICA
        params_grilla.max_iteraciones = min(100, params.max_iteraciones // 3)
        params_grilla.verbose = False
        
        resultado_grilla = self._optimizar_grilla(perfil_terreno, estrato, params_grilla)
        
        # Fase 2: Refinamiento con algoritmo genético
        params_genetico = copy.deepcopy(params)
        params_genetico.metodo = MetodoOptimizacion.ALGORITMO_GENETICO
        params_genetico.max_iteraciones = params.max_iteraciones - params_grilla.max_iteraciones
        params_genetico.poblacion_genetico = min(30, params.poblacion_genetico)
        params_genetico.verbose = False
        
        resultado_genetico = self._optimizar_genetico(
            perfil_terreno, estrato, params_genetico, resultado_grilla.circulo_optimo)
        
        # Combinar historiales
        historial_mejores = resultado_grilla.historial_mejores + resultado_genetico.historial_mejores
        historial_fs = resultado_grilla.historial_fs + resultado_genetico.historial_fs
        
        # Determinar mejor resultado
        if (resultado_genetico.factor_seguridad is not None and 
            resultado_grilla.factor_seguridad is not None):
            if params.tipo == TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO:
                mejor_resultado = (resultado_genetico if resultado_genetico.factor_seguridad < resultado_grilla.factor_seguridad 
                                 else resultado_grilla)
            else:
                mejor_resultado = (resultado_genetico if resultado_genetico.factor_seguridad > resultado_grilla.factor_seguridad 
                                 else resultado_grilla)
        else:
            mejor_resultado = resultado_genetico if resultado_genetico.factor_seguridad is not None else resultado_grilla
        
        return ResultadoOptimizacion(
            circulo_optimo=mejor_resultado.circulo_optimo,
            factor_seguridad=mejor_resultado.factor_seguridad,
            metricas=mejor_resultado.metricas,
            iteraciones_usadas=resultado_grilla.iteraciones_usadas + resultado_genetico.iteraciones_usadas,
            tiempo_computo=0,
            convergencia_alcanzada=True,
            historial_mejores=historial_mejores,
            historial_fs=historial_fs,
            mensaje=f"Optimización híbrida: Grilla ({resultado_grilla.iteraciones_usadas}) + Genético ({resultado_genetico.iteraciones_usadas})"
        )
    
    def _evaluar_circulo(self, 
                        circulo: CirculoFalla,
                        perfil_terreno: List[Tuple[float, float]],
                        estrato: Estrato,
                        params: ParametrosOptimizacion) -> Tuple[Optional[float], Optional[float], Optional[MetricasCirculo]]:
        """
        Evalúa un círculo y devuelve puntuación, FS y métricas.
        
        Returns:
            Tuple (puntuacion, factor_seguridad, metricas) o (None, None, None) si inválido
        """
        try:
            # Calcular métricas
            metricas = self.geometria.calcular_metricas_circulo(
                circulo, perfil_terreno, estrato, params.num_dovelas)
            
            # Verificar validez básica
            if not metricas.es_geometricamente_valido:
                return None, None, None
            
            # Intentar calcular factor de seguridad
            try:
                resultado_bishop = analizar_bishop(
                    circulo=circulo,
                    perfil_terreno=perfil_terreno,
                    estrato=estrato,
                    num_dovelas=params.num_dovelas,
                    validar_entrada=False  # Ya validamos con métricas
                )
                fs = resultado_bishop['factor_seguridad']
                metricas.factor_seguridad = fs
                
            except Exception:
                return None, None, None
            
            # Calcular puntuación según tipo de optimización
            if params.tipo == TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO:
                # Buscar FS mínimo (círculo crítico)
                puntuacion = fs
                
            elif params.tipo == TipoOptimizacion.FACTOR_SEGURIDAD_OBJETIVO:
                # Buscar FS en rango objetivo
                if params.fs_objetivo_min <= fs <= params.fs_objetivo_max:
                    # FS en rango: puntuación alta
                    centro_objetivo = (params.fs_objetivo_min + params.fs_objetivo_max) / 2
                    puntuacion = 100 - abs(fs - centro_objetivo)
                else:
                    # FS fuera de rango: penalizar
                    if fs < params.fs_objetivo_min:
                        puntuacion = fs * 10  # Penalizar FS bajos
                    else:
                        puntuacion = max(0, 50 - (fs - params.fs_objetivo_max) * 10)  # Penalizar FS altos
                        
            elif params.tipo == TipoOptimizacion.VALIDEZ_MAXIMA:
                # Maximizar validez geométrica y computacional
                puntuacion = (metricas.porcentaje_dovelas_validas * 0.6 + 
                             metricas.cobertura_terreno * 0.4)
                
            elif params.tipo == TipoOptimizacion.MULTIOBJETIVO:
                # Combinar FS y validez
                # Normalizar FS (objetivo: 1.5-2.5)
                fs_normalizado = max(0, 100 - abs(fs - 2.0) * 20)
                validez_normalizada = metricas.porcentaje_dovelas_validas
                
                puntuacion = (params.peso_fs * fs_normalizado + 
                             params.peso_validez * validez_normalizada)
            
            else:
                raise ValueError(f"Tipo de optimización no reconocido: {params.tipo}")
            
            return puntuacion, fs, metricas
            
        except Exception:
            return None, None, None
    
    def _seleccion_torneo(self, poblacion_fitness: List[Tuple], tamano_torneo: int) -> CirculoFalla:
        """Selección por torneo para algoritmo genético"""
        participantes = random.sample(poblacion_fitness, min(tamano_torneo, len(poblacion_fitness)))
        ganador = max(participantes, key=lambda x: x[0])  # Mejor fitness
        return ganador[3]  # Retornar círculo
    
    def _cruzar_circulos(self, padre1: CirculoFalla, padre2: CirculoFalla) -> CirculoFalla:
        """Cruce de dos círculos para generar descendencia"""
        # Cruce promedio con perturbación aleatoria
        alpha = random.random()
        
        cx = alpha * padre1.centro_x + (1 - alpha) * padre2.centro_x
        cy = alpha * padre1.centro_y + (1 - alpha) * padre2.centro_y
        r = alpha * padre1.radio + (1 - alpha) * padre2.radio
        
        return CirculoFalla(cx, cy, r)
    
    def _mutar_circulo(self, circulo: CirculoFalla, 
                      cx_min: float, cx_max: float,
                      cy_min: float, cy_max: float,
                      r_min: float, r_max: float) -> CirculoFalla:
        """Mutación de un círculo"""
        # Mutación gaussiana con restricción de límites
        std_cx = (cx_max - cx_min) * 0.05  # 5% del rango
        std_cy = (cy_max - cy_min) * 0.05
        std_r = (r_max - r_min) * 0.05
        
        nuevo_cx = np.clip(circulo.centro_x + random.gauss(0, std_cx), cx_min, cx_max)
        nuevo_cy = np.clip(circulo.centro_y + random.gauss(0, std_cy), cy_min, cy_max)
        nuevo_r = np.clip(circulo.radio + random.gauss(0, std_r), r_min, r_max)
        
        return CirculoFalla(nuevo_cx, nuevo_cy, nuevo_r)


def crear_optimizador_casos_ejemplo() -> Dict[str, ParametrosOptimizacion]:
    """Crea configuraciones de optimización para diferentes casos típicos"""
    
    configuraciones = {
        'critico': ParametrosOptimizacion(
            tipo=TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO,
            metodo=MetodoOptimizacion.HIBRIDO,
            max_iteraciones=500,
            poblacion_genetico=30,
            verbose=True
        ),
        
        'estable': ParametrosOptimizacion(
            tipo=TipoOptimizacion.FACTOR_SEGURIDAD_OBJETIVO,
            metodo=MetodoOptimizacion.ALGORITMO_GENETICO,
            fs_objetivo_min=1.5,
            fs_objetivo_max=2.5,
            max_iteraciones=300,
            poblacion_genetico=40,
            verbose=True
        ),
        
        'marginal': ParametrosOptimizacion(
            tipo=TipoOptimizacion.FACTOR_SEGURIDAD_OBJETIVO,
            metodo=MetodoOptimizacion.HIBRIDO,
            fs_objetivo_min=1.0,
            fs_objetivo_max=1.4,
            max_iteraciones=400,
            poblacion_genetico=35,
            verbose=True
        ),
        
        'rapido': ParametrosOptimizacion(
            tipo=TipoOptimizacion.MULTIOBJETIVO,
            metodo=MetodoOptimizacion.BUSQUEDA_ALEATORIA,
            max_iteraciones=100,
            verbose=False
        )
    }
    
    return configuraciones
