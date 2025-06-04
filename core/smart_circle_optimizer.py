"""
Optimizador Ultra-Inteligente de Círculos con Límites Automáticos

Características avanzadas:
- Límites geométricos automáticos
- Múltiples algoritmos de optimización
- Validación en tiempo real
- Corrección automática de parámetros
- Algoritmos adaptativos
- Optimización multiobjetivo
- Predicción inteligente de zonas críticas
"""

import math
import random
import numpy as np
from typing import List, Tuple, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import copy

from data.models import CirculoFalla, Estrato
from core.circle_constraints import (LimitesGeometricos, CalculadorLimites, 
                                   aplicar_limites_inteligentes)
from core.circle_geometry import GeometriaCirculoAvanzada


class TipoOptimizacion(Enum):
    """Tipos de optimización disponibles"""
    MINIMO_FS = "minimo_fs"                    # Buscar FS mínimo (círculo crítico)
    OBJETIVO_FS = "objetivo_fs"                # Buscar FS específico
    MAXIMA_VALIDEZ = "maxima_validez"          # Maximizar validez geométrica
    MULTIOBJETIVO = "multiobjetivo"            # Combinar FS y validez
    ZONA_CRITICA = "zona_critica"              # Enfocarse en zonas críticas
    ADAPTATIVO = "adaptativo"                  # Cambiar estrategia dinámicamente


class AlgoritmoOptimizacion(Enum):
    """Algoritmos de optimización disponibles"""
    GENETICO_AVANZADO = "genetico_avanzado"    # Algoritmo genético mejorado
    GRADIENTE_NUMERICO = "gradiente_numerico"  # Descenso por gradiente
    ENJAMBRE_PARTICULAS = "enjambre_particulas" # PSO
    RECOCIDO_SIMULADO = "recocido_simulado"    # Simulated Annealing
    HIBRIDO_INTELIGENTE = "hibrido_inteligente" # Combinación adaptativa
    BUSQUEDA_TABU = "busqueda_tabu"            # Búsqueda tabú


@dataclass
class ConfiguracionOptimizacion:
    """Configuración completa para optimización"""
    # Tipo y algoritmo
    tipo_optimizacion: TipoOptimizacion = TipoOptimizacion.MINIMO_FS
    algoritmo: AlgoritmoOptimizacion = AlgoritmoOptimizacion.GENETICO_AVANZADO
    
    # Parámetros generales
    max_iteraciones: int = 100
    tolerancia_convergencia: float = 0.001
    tiempo_maximo_segundos: Optional[float] = None
    
    # Objetivos específicos
    fs_objetivo: float = 1.5
    tolerancia_fs: float = 0.1
    peso_fs: float = 0.7
    peso_validez: float = 0.3
    
    # Parámetros de algoritmos específicos
    tamaño_poblacion: int = 50
    tasa_mutacion: float = 0.1
    tasa_cruce: float = 0.8
    elite_porcentaje: float = 0.1
    
    # Configuraciones adaptativas
    usar_limites_inteligentes: bool = True
    corregir_automaticamente: bool = True
    estrategia_busqueda: str = "balanceada"  # "intensiva", "extensiva", "balanceada"
    
    # Criterios de parada avanzados
    max_generaciones_sin_mejora: int = 20
    diversidad_minima: float = 0.01


@dataclass
class ResultadoOptimizacion:
    """Resultado completo de optimización"""
    circulo_optimo: CirculoFalla
    factor_seguridad: float
    validez_geometrica: float
    iteraciones_utilizadas: int
    tiempo_transcurrido: float
    convergencia_alcanzada: bool
    
    # Historial de optimización
    historial_fs: List[float] = field(default_factory=list)
    historial_validez: List[float] = field(default_factory=list)
    historial_circulos: List[CirculoFalla] = field(default_factory=list)
    
    # Estadísticas
    mejor_fs_encontrado: float = 0.0
    peor_fs_encontrado: float = 0.0
    promedio_fs: float = 0.0
    desviacion_fs: float = 0.0
    
    # Información adicional
    limites_utilizados: Optional[LimitesGeometricos] = None
    configuracion_utilizada: Optional[ConfiguracionOptimizacion] = None
    mensaje_finalizacion: str = ""


class OptimizadorUltraInteligente:
    """Optimizador ultra-inteligente con límites automáticos"""
    
    def __init__(self):
        self.calculador_limites = CalculadorLimites()
        self.geometria_avanzada = GeometriaCirculoAvanzada()
        
        # Cache para evaluaciones
        self._cache_evaluaciones = {}
        self._contador_evaluaciones = 0
        
        # Configuración adaptativa
        self.historico_rendimiento = {}
        self.estrategias_exitosas = []
    
    def optimizar(self,
                 perfil_terreno: List[Tuple[float, float]],
                 estrato: Estrato,
                 config: ConfiguracionOptimizacion) -> ResultadoOptimizacion:
        """
        Optimización principal con configuración completa
        """
        import time
        inicio = time.time()
        
        # 1. Calcular límites inteligentes automáticamente
        if config.usar_limites_inteligentes:
            limites = aplicar_limites_inteligentes(perfil_terreno, "talud_empinado", config.fs_objetivo)
        else:
            limites = self.calculador_limites.calcular_limites_automaticos(perfil_terreno, config.fs_objetivo)
        
        # 2. Inicializar población según estrategia
        poblacion_inicial = self._generar_poblacion_inteligente(limites, config)
        
        # 3. Ejecutar algoritmo específico
        resultado = self._ejecutar_algoritmo(poblacion_inicial, perfil_terreno, estrato, limites, config)
        
        # 4. Post-procesamiento y validación final
        resultado.tiempo_transcurrido = time.time() - inicio
        resultado.limites_utilizadas = limites
        resultado.configuracion_utilizada = config
        
        # 5. Validación final y corrección si es necesaria
        if config.corregir_automaticamente:
            resultado.circulo_optimo = self._validar_y_corregir_final(
                resultado.circulo_optimo, limites, perfil_terreno, estrato)
        
        return resultado
    
    def _generar_poblacion_inteligente(self, 
                                     limites: LimitesGeometricos,
                                     config: ConfiguracionOptimizacion) -> List[CirculoFalla]:
        """
        Genera población inicial inteligente basada en límites y estrategia
        """
        poblacion = []
        
        # Estrategia balanceada: mix de distribuciones
        if config.estrategia_busqueda == "balanceada":
            # 40% distribución uniforme
            poblacion.extend(self.calculador_limites.generar_circulos_dentro_limites(
                limites, int(config.tamaño_poblacion * 0.4), "uniforme"))
            
            # 30% distribución gaussiana (centrada)
            poblacion.extend(self.calculador_limites.generar_circulos_dentro_limites(
                limites, int(config.tamaño_poblacion * 0.3), "gaussiana"))
            
            # 30% distribución crítica (radios grandes, centros cercanos)
            poblacion.extend(self.calculador_limites.generar_circulos_dentro_limites(
                limites, int(config.tamaño_poblacion * 0.3), "critico"))
        
        elif config.estrategia_busqueda == "intensiva":
            # Concentrar búsqueda en zonas prometedoras
            poblacion.extend(self.calculador_limites.generar_circulos_dentro_limites(
                limites, config.tamaño_poblacion, "critico"))
        
        else:  # "extensiva"
            # Explorar todo el espacio uniformemente
            poblacion.extend(self.calculador_limites.generar_circulos_dentro_limites(
                limites, config.tamaño_poblacion, "uniforme"))
        
        # Asegurar tamaño exacto
        while len(poblacion) < config.tamaño_poblacion:
            poblacion.append(self.calculador_limites.generar_circulos_dentro_limites(limites, 1, "uniforme")[0])
        
        return poblacion[:config.tamaño_poblacion]
    
    def _ejecutar_algoritmo(self,
                          poblacion_inicial: List[CirculoFalla],
                          perfil_terreno: List[Tuple[float, float]],
                          estrato: Estrato,
                          limites: LimitesGeometricos,
                          config: ConfiguracionOptimizacion) -> ResultadoOptimizacion:
        """
        Ejecuta el algoritmo específico seleccionado
        """
        if config.algoritmo == AlgoritmoOptimizacion.GENETICO_AVANZADO:
            return self._algoritmo_genetico_avanzado(poblacion_inicial, perfil_terreno, estrato, limites, config)
        
        elif config.algoritmo == AlgoritmoOptimizacion.GRADIENTE_NUMERICO:
            return self._algoritmo_gradiente_numerico(poblacion_inicial, perfil_terreno, estrato, limites, config)
        
        elif config.algoritmo == AlgoritmoOptimizacion.ENJAMBRE_PARTICULAS:
            return self._algoritmo_enjambre_particulas(poblacion_inicial, perfil_terreno, estrato, limites, config)
        
        elif config.algoritmo == AlgoritmoOptimizacion.RECOCIDO_SIMULADO:
            return self._algoritmo_recocido_simulado(poblacion_inicial, perfil_terreno, estrato, limites, config)
        
        elif config.algoritmo == AlgoritmoOptimizacion.HIBRIDO_INTELIGENTE:
            return self._algoritmo_hibrido_inteligente(poblacion_inicial, perfil_terreno, estrato, limites, config)
        
        else:  # BUSQUEDA_TABU
            return self._algoritmo_busqueda_tabu(poblacion_inicial, perfil_terreno, estrato, limites, config)
    
    def _algoritmo_genetico_avanzado(self,
                                   poblacion: List[CirculoFalla],
                                   perfil_terreno: List[Tuple[float, float]],
                                   estrato: Estrato,
                                   limites: LimitesGeometricos,
                                   config: ConfiguracionOptimizacion) -> ResultadoOptimizacion:
        """
        Algoritmo genético avanzado con elitismo y adaptación
        """
        resultado = ResultadoOptimizacion(
            circulo_optimo=poblacion[0],
            factor_seguridad=0.0,
            validez_geometrica=0.0,
            iteraciones_utilizadas=0,
            tiempo_transcurrido=0.0,
            convergencia_alcanzada=False
        )
        
        mejor_fitness = float('-inf')
        generaciones_sin_mejora = 0
        
        for generacion in range(config.max_iteraciones):
            # Evaluar población
            fitness_poblacion = []
            for circulo in poblacion:
                fitness = self._evaluar_fitness(circulo, perfil_terreno, estrato, config)
                fitness_poblacion.append(fitness)
            
            # Encontrar mejor individuo
            mejor_idx = max(range(len(fitness_poblacion)), key=lambda i: fitness_poblacion[i])
            fitness_actual = fitness_poblacion[mejor_idx]
            
            # Verificar mejora
            if fitness_actual > mejor_fitness + config.tolerancia_convergencia:
                mejor_fitness = fitness_actual
                resultado.circulo_optimo = copy.deepcopy(poblacion[mejor_idx])
                generaciones_sin_mejora = 0
            else:
                generaciones_sin_mejora += 1
            
            # Registrar historial
            resultado.historial_fs.append(self._calcular_fs_circulo(resultado.circulo_optimo, perfil_terreno, estrato))
            resultado.historial_circulos.append(copy.deepcopy(resultado.circulo_optimo))
            
            # Criterio de parada temprana
            if generaciones_sin_mejora >= config.max_generaciones_sin_mejora:
                resultado.convergencia_alcanzada = True
                break
            
            # Selección por torneo
            nueva_poblacion = self._seleccion_torneo(poblacion, fitness_poblacion, config)
            
            # Cruce y mutación
            nueva_poblacion = self._aplicar_cruce_avanzado(nueva_poblacion, limites, config)
            nueva_poblacion = self._aplicar_mutacion_adaptativa(nueva_poblacion, limites, config, generacion)
            
            # Elitismo: preservar mejores individuos
            num_elite = int(config.tamaño_poblacion * config.elite_porcentaje)
            elite_indices = sorted(range(len(fitness_poblacion)), key=lambda i: fitness_poblacion[i], reverse=True)[:num_elite]
            
            for i, idx in enumerate(elite_indices):
                if i < len(nueva_poblacion):
                    nueva_poblacion[i] = copy.deepcopy(poblacion[idx])
            
            poblacion = nueva_poblacion
            resultado.iteraciones_utilizadas = generacion + 1
        
        # Calcular estadísticas finales
        resultado.factor_seguridad = self._calcular_fs_circulo(resultado.circulo_optimo, perfil_terreno, estrato)
        resultado.validez_geometrica = self._calcular_validez_geometrica(resultado.circulo_optimo, perfil_terreno, estrato)
        
        if resultado.historial_fs:
            resultado.mejor_fs_encontrado = min(resultado.historial_fs)
            resultado.peor_fs_encontrado = max(resultado.historial_fs)
            resultado.promedio_fs = sum(resultado.historial_fs) / len(resultado.historial_fs)
        
        resultado.mensaje_finalizacion = f"Algoritmo genético completado en {resultado.iteraciones_utilizadas} generaciones"
        
        return resultado
    
    def _evaluar_fitness(self,
                        circulo: CirculoFalla,
                        perfil_terreno: List[Tuple[float, float]],
                        estrato: Estrato,
                        config: ConfiguracionOptimizacion) -> float:
        """
        Evalúa fitness de un círculo según el tipo de optimización
        """
        # Usar cache para evitar recálculos
        cache_key = (circulo.centro_x, circulo.centro_y, circulo.radio)
        if cache_key in self._cache_evaluaciones:
            return self._cache_evaluaciones[cache_key]
        
        try:
            fs = self._calcular_fs_circulo(circulo, perfil_terreno, estrato)
            validez = self._calcular_validez_geometrica(circulo, perfil_terreno, estrato)
            
            # Penalizar FS inválidos
            if fs <= 0 or fs > 50:
                fitness = -1000
            elif config.tipo_optimizacion == TipoOptimizacion.MINIMO_FS:
                fitness = -fs  # Minimizar FS (fitness mayor = FS menor)
            elif config.tipo_optimizacion == TipoOptimizacion.OBJETIVO_FS:
                # Maximizar proximidad al objetivo
                diferencia = abs(fs - config.fs_objetivo)
                fitness = -diferencia if diferencia <= config.tolerancia_fs else -diferencia * 10
            elif config.tipo_optimizacion == TipoOptimizacion.MAXIMA_VALIDEZ:
                fitness = validez
            elif config.tipo_optimizacion == TipoOptimizacion.MULTIOBJETIVO:
                # Combinar FS y validez
                fs_normalizado = max(0, min(1, (3.0 - fs) / 2.0))  # Normalizar FS [1,3] -> [1,0]
                validez_normalizada = validez / 100.0
                fitness = config.peso_fs * fs_normalizado + config.peso_validez * validez_normalizada
            else:
                fitness = -fs  # Por defecto minimizar FS
            
            # Bonus por validez geométrica alta
            if validez > 80:
                fitness += 0.1
            elif validez < 50:
                fitness -= 0.2
            
        except Exception:
            fitness = -1000  # Penalizar errores severamente
        
        # Guardar en cache
        self._cache_evaluaciones[cache_key] = fitness
        self._contador_evaluaciones += 1
        
        return fitness
    
    def _calcular_fs_circulo(self,
                           circulo: CirculoFalla,
                           perfil_terreno: List[Tuple[float, float]],
                           estrato: Estrato) -> float:
        """Calcula factor de seguridad de un círculo"""
        try:
            from core.bishop import analizar_bishop
            resultado = analizar_bishop(circulo, perfil_terreno, estrato, 10, validar_entrada=False)
            return resultado['factor_seguridad']
        except:
            return 0.0
    
    def _calcular_validez_geometrica(self,
                                   circulo: CirculoFalla,
                                   perfil_terreno: List[Tuple[float, float]],
                                   estrato: Estrato) -> float:
        """Calcula validez geométrica de un círculo"""
        try:
            metricas = self.geometria_avanzada.calcular_metricas_circulo(circulo, perfil_terreno, estrato, 10)
            return metricas.porcentaje_dovelas_validas
        except:
            return 0.0
    
    def _seleccion_torneo(self,
                         poblacion: List[CirculoFalla],
                         fitness: List[float],
                         config: ConfiguracionOptimizacion) -> List[CirculoFalla]:
        """Selección por torneo con tamaño variable"""
        nueva_poblacion = []
        tamaño_torneo = max(2, int(config.tamaño_poblacion * 0.1))
        
        for _ in range(config.tamaño_poblacion):
            # Seleccionar competidores aleatoriamente
            competidores = random.sample(range(len(poblacion)), tamaño_torneo)
            ganador = max(competidores, key=lambda i: fitness[i])
            nueva_poblacion.append(copy.deepcopy(poblacion[ganador]))
        
        return nueva_poblacion
    
    def _aplicar_cruce_avanzado(self,
                              poblacion: List[CirculoFalla],
                              limites: LimitesGeometricos,
                              config: ConfiguracionOptimizacion) -> List[CirculoFalla]:
        """Aplica cruce avanzado con múltiples estrategias"""
        nueva_poblacion = []
        
        for i in range(0, len(poblacion) - 1, 2):
            padre1 = poblacion[i]
            padre2 = poblacion[i + 1]
            
            if random.random() < config.tasa_cruce:
                # Cruce aritmético con factor aleatorio
                alpha = random.uniform(0.3, 0.7)
                
                hijo1_cx = alpha * padre1.centro_x + (1 - alpha) * padre2.centro_x
                hijo1_cy = alpha * padre1.centro_y + (1 - alpha) * padre2.centro_y
                hijo1_r = alpha * padre1.radio + (1 - alpha) * padre2.radio
                
                hijo2_cx = (1 - alpha) * padre1.centro_x + alpha * padre2.centro_x
                hijo2_cy = (1 - alpha) * padre1.centro_y + alpha * padre2.centro_y
                hijo2_r = (1 - alpha) * padre1.radio + alpha * padre2.radio
                
                # Asegurar que estén dentro de límites
                hijo1 = CirculoFalla(
                    max(limites.centro_x_min, min(hijo1_cx, limites.centro_x_max)),
                    max(limites.centro_y_min, min(hijo1_cy, limites.centro_y_max)),
                    max(limites.radio_min, min(hijo1_r, limites.radio_max))
                )
                
                hijo2 = CirculoFalla(
                    max(limites.centro_x_min, min(hijo2_cx, limites.centro_x_max)),
                    max(limites.centro_y_min, min(hijo2_cy, limites.centro_y_max)),
                    max(limites.radio_min, min(hijo2_r, limites.radio_max))
                )
                
                nueva_poblacion.extend([hijo1, hijo2])
            else:
                nueva_poblacion.extend([copy.deepcopy(padre1), copy.deepcopy(padre2)])
        
        # Si la población es impar, agregar el último individuo
        if len(poblacion) % 2 == 1:
            nueva_poblacion.append(copy.deepcopy(poblacion[-1]))
        
        return nueva_poblacion[:len(poblacion)]
    
    def _aplicar_mutacion_adaptativa(self,
                                   poblacion: List[CirculoFalla],
                                   limites: LimitesGeometricos,
                                   config: ConfiguracionOptimizacion,
                                   generacion: int) -> List[CirculoFalla]:
        """Aplica mutación adaptativa que disminuye con las generaciones"""
        # Tasa de mutación adaptativa
        tasa_adaptativa = config.tasa_mutacion * (1 - generacion / config.max_iteraciones)
        
        for circulo in poblacion:
            if random.random() < tasa_adaptativa:
                # Determinar magnitud de mutación (disminuye con generaciones)
                magnitud = 0.1 * (1 - generacion / config.max_iteraciones)
                
                # Mutar parámetros
                if random.random() < 0.33:  # Mutar centro X
                    rango_x = limites.centro_x_max - limites.centro_x_min
                    delta_x = random.gauss(0, rango_x * magnitud)
                    circulo.centro_x = max(limites.centro_x_min, 
                                         min(circulo.centro_x + delta_x, limites.centro_x_max))
                
                if random.random() < 0.33:  # Mutar centro Y
                    rango_y = limites.centro_y_max - limites.centro_y_min
                    delta_y = random.gauss(0, rango_y * magnitud)
                    circulo.centro_y = max(limites.centro_y_min, 
                                         min(circulo.centro_y + delta_y, limites.centro_y_max))
                
                if random.random() < 0.33:  # Mutar radio
                    rango_r = limites.radio_max - limites.radio_min
                    delta_r = random.gauss(0, rango_r * magnitud)
                    circulo.radio = max(limites.radio_min, 
                                      min(circulo.radio + delta_r, limites.radio_max))
        
        return poblacion
    
    def _validar_y_corregir_final(self,
                                circulo: CirculoFalla,
                                limites: LimitesGeometricos,
                                perfil_terreno: List[Tuple[float, float]],
                                estrato: Estrato) -> CirculoFalla:
        """Validación y corrección final del círculo óptimo"""
        validacion = self.calculador_limites.validar_y_corregir_circulo(circulo, limites, True)
        
        if validacion.circulo_corregido:
            return validacion.circulo_corregido
        else:
            return circulo
    
    # Implementaciones simplificadas de otros algoritmos
    def _algoritmo_gradiente_numerico(self, poblacion, perfil_terreno, estrato, limites, config):
        """Implementación simplificada - usar algoritmo genético por ahora"""
        return self._algoritmo_genetico_avanzado(poblacion, perfil_terreno, estrato, limites, config)
    
    def _algoritmo_enjambre_particulas(self, poblacion, perfil_terreno, estrato, limites, config):
        """Implementación simplificada - usar algoritmo genético por ahora"""
        return self._algoritmo_genetico_avanzado(poblacion, perfil_terreno, estrato, limites, config)
    
    def _algoritmo_recocido_simulado(self, poblacion, perfil_terreno, estrato, limites, config):
        """Implementación simplificada - usar algoritmo genético por ahora"""
        return self._algoritmo_genetico_avanzado(poblacion, perfil_terreno, estrato, limites, config)
    
    def _algoritmo_hibrido_inteligente(self, poblacion, perfil_terreno, estrato, limites, config):
        """Implementación simplificada - usar algoritmo genético por ahora"""
        return self._algoritmo_genetico_avanzado(poblacion, perfil_terreno, estrato, limites, config)
    
    def _algoritmo_busqueda_tabu(self, poblacion, perfil_terreno, estrato, limites, config):
        """Implementación simplificada - usar algoritmo genético por ahora"""
        return self._algoritmo_genetico_avanzado(poblacion, perfil_terreno, estrato, limites, config)


# Funciones de conveniencia
def optimizar_circulo_inteligente(perfil_terreno: List[Tuple[float, float]],
                                estrato: Estrato,
                                tipo_optimizacion: str = "minimo_fs",
                                fs_objetivo: float = 1.5) -> ResultadoOptimizacion:
    """
    Función de conveniencia para optimización rápida
    """
    config = ConfiguracionOptimizacion(
        tipo_optimizacion=TipoOptimizacion(tipo_optimizacion),
        fs_objetivo=fs_objetivo,
        max_iteraciones=50,
        tamaño_poblacion=30
    )
    
    optimizador = OptimizadorUltraInteligente()
    return optimizador.optimizar(perfil_terreno, estrato, config)


def buscar_circulo_critico_rapido(perfil_terreno: List[Tuple[float, float]],
                                 estrato: Estrato) -> CirculoFalla:
    """
    Búsqueda rápida del círculo más crítico
    """
    resultado = optimizar_circulo_inteligente(perfil_terreno, estrato, "minimo_fs")
    return resultado.circulo_optimo
