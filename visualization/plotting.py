"""
Módulo de visualización para análisis de estabilidad de taludes.

Este módulo proporciona funciones para crear gráficos profesionales de:
- Perfiles de terreno y círculos de falla
- Dovelas y fuerzas
- Resultados de análisis (Fellenius y Bishop)
- Comparaciones entre métodos
- Niveles freáticos

Autor: Sistema de Análisis de Estabilidad de Taludes
Fecha: 2024
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass

# Importar modelos y resultados
from data.models import CirculoFalla, Dovela
from core.fellenius import ResultadoFellenius
from core.bishop import ResultadoBishop


@dataclass
class ConfiguracionGrafico:
    """Configuración para personalizar gráficos."""
    figsize: Tuple[float, float] = (12, 8)
    dpi: int = 100
    estilo_grid: bool = True
    color_terreno: str = '#8B4513'
    color_circulo: str = '#FF4444'
    color_dovelas: str = '#87CEEB'
    color_agua: str = '#4169E1'
    color_fuerzas: str = '#FF6347'
    titulo_fontsize: int = 14
    etiquetas_fontsize: int = 12
    leyenda_fontsize: int = 10


def configurar_estilo_grafico():
    """Configura el estilo general de los gráficos."""
    plt.style.use('default')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['font.size'] = 10


def graficar_perfil_basico(perfil_terreno: List[Tuple[float, float]], 
                          circulo: CirculoFalla,
                          titulo: str = "Perfil de Terreno y Círculo de Falla",
                          config: Optional[ConfiguracionGrafico] = None) -> plt.Figure:
    """
    Gráfico básico de perfil de terreno con círculo de falla.
    
    Args:
        perfil_terreno: Lista de puntos (x, y) del perfil
        circulo: Círculo de falla
        titulo: Título del gráfico
        config: Configuración de estilo
        
    Returns:
        Figura de matplotlib
    """
    if config is None:
        config = ConfiguracionGrafico()
    
    configurar_estilo_grafico()
    fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)
    
    # Extraer coordenadas
    x_coords = [p[0] for p in perfil_terreno]
    y_coords = [p[1] for p in perfil_terreno]
    
    # Graficar perfil de terreno
    ax.fill_between(x_coords, y_coords, alpha=0.7, color=config.color_terreno, 
                    label='Terreno', linewidth=2)
    ax.plot(x_coords, y_coords, color='black', linewidth=2)
    
    # Graficar círculo de falla
    circulo_patch = patches.Circle((circulo.xc, circulo.yc), circulo.radio, 
                                  fill=False, color=config.color_circulo, 
                                  linewidth=3, label='Círculo de falla')
    ax.add_patch(circulo_patch)
    
    # Marcar centro del círculo
    ax.plot(circulo.xc, circulo.yc, 'o', color=config.color_circulo, 
            markersize=8, label='Centro círculo')
    
    # Configurar ejes
    ax.set_xlabel('Distancia (m)', fontsize=config.etiquetas_fontsize)
    ax.set_ylabel('Elevación (m)', fontsize=config.etiquetas_fontsize)
    ax.set_title(titulo, fontsize=config.titulo_fontsize, fontweight='bold')
    ax.legend(fontsize=config.leyenda_fontsize)
    ax.grid(config.estilo_grid, alpha=0.3)
    ax.set_aspect('equal')
    
    # Ajustar límites
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    margen = 0.1 * max(x_max - x_min, y_max - y_min)
    
    ax.set_xlim(x_min - margen, x_max + margen)
    ax.set_ylim(y_min - margen, y_max + margen)
    
    plt.tight_layout()
    return fig


def graficar_dovelas(perfil_terreno: List[Tuple[float, float]], 
                    circulo: CirculoFalla,
                    dovelas: List[Dovela],
                    titulo: str = "Análisis por Dovelas",
                    mostrar_fuerzas: bool = False,
                    config: Optional[ConfiguracionGrafico] = None) -> plt.Figure:
    """
    Gráfico detallado mostrando dovelas individuales.
    
    Args:
        perfil_terreno: Lista de puntos del perfil
        circulo: Círculo de falla
        dovelas: Lista de dovelas
        titulo: Título del gráfico
        mostrar_fuerzas: Si mostrar vectores de fuerza
        config: Configuración de estilo
        
    Returns:
        Figura de matplotlib
    """
    if config is None:
        config = ConfiguracionGrafico()
    
    fig = graficar_perfil_basico(perfil_terreno, circulo, titulo, config)
    ax = fig.gca()
    
    # Graficar dovelas
    for i, dovela in enumerate(dovelas):
        # Calcular límites de la dovela
        x_izq = dovela.x_centro - dovela.ancho / 2
        x_der = dovela.x_centro + dovela.ancho / 2
        
        # Encontrar elevación del terreno en el centro
        y_terreno = _interpolar_elevacion(perfil_terreno, dovela.x_centro)
        
        # Encontrar intersección con círculo
        y_circulo = _calcular_y_circulo(circulo, dovela.x_centro)
        
        if y_circulo is not None and y_terreno is not None:
            # Dibujar dovela como rectángulo
            altura_dovela = y_terreno - y_circulo
            rect = patches.Rectangle((x_izq, y_circulo), dovela.ancho, altura_dovela,
                                   linewidth=1, edgecolor='black', 
                                   facecolor=config.color_dovelas, alpha=0.6)
            ax.add_patch(rect)
            
            # Etiquetar dovela
            ax.text(dovela.x_centro, y_circulo + altura_dovela/2, f'{i+1}',
                   ha='center', va='center', fontsize=8, fontweight='bold')
            
            # Mostrar fuerzas si se solicita
            if mostrar_fuerzas:
                _dibujar_fuerzas_dovela(ax, dovela, y_terreno, y_circulo, config)
    
    return fig


def graficar_resultado_fellenius(perfil_terreno: List[Tuple[float, float]], 
                                circulo: CirculoFalla,
                                resultado: ResultadoFellenius,
                                config: Optional[ConfiguracionGrafico] = None) -> plt.Figure:
    """
    Gráfico completo del análisis de Fellenius.
    
    Args:
        perfil_terreno: Lista de puntos del perfil
        circulo: Círculo de falla
        resultado: Resultado del análisis de Fellenius
        config: Configuración de estilo
        
    Returns:
        Figura de matplotlib
    """
    if config is None:
        config = ConfiguracionGrafico()
    
    titulo = f"Análisis de Fellenius - Factor de Seguridad: {resultado.factor_seguridad:.3f}"
    
    fig = graficar_dovelas(perfil_terreno, circulo, resultado.dovelas, titulo, config=config)
    ax = fig.gca()
    
    # Agregar información del resultado
    info_text = f"""Método: Fellenius (Directo)
Factor de Seguridad: {resultado.factor_seguridad:.3f}
Momento Resistente: {resultado.momento_resistente:.1f} kN·m
Momento Actuante: {resultado.momento_actuante:.1f} kN·m
Dovelas: {len(resultado.dovelas)}
Válido: {'Sí' if resultado.es_valido else 'No'}"""
    
    # Clasificación de estabilidad
    if resultado.factor_seguridad < 1.0:
        clasificacion = "INESTABLE"
        color_fs = 'red'
    elif resultado.factor_seguridad < 1.3:
        clasificacion = "MARGINALMENTE ESTABLE"
        color_fs = 'orange'
    elif resultado.factor_seguridad < 2.0:
        clasificacion = "ESTABLE"
        color_fs = 'green'
    else:
        clasificacion = "MUY ESTABLE"
        color_fs = 'darkgreen'
    
    info_text += f"\nClasificación: {clasificacion}"
    
    # Colocar texto informativo
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Destacar factor de seguridad
    ax.text(0.98, 0.02, f"Fs = {resultado.factor_seguridad:.3f}", 
            transform=ax.transAxes, fontsize=16, fontweight='bold',
            horizontalalignment='right', verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor=color_fs, alpha=0.7, edgecolor='black'))
    
    return fig


def graficar_resultado_bishop(perfil_terreno: List[Tuple[float, float]], 
                             circulo: CirculoFalla,
                             resultado: ResultadoBishop,
                             config: Optional[ConfiguracionGrafico] = None) -> plt.Figure:
    """
    Gráfico completo del análisis de Bishop.
    
    Args:
        perfil_terreno: Lista de puntos del perfil
        circulo: Círculo de falla
        resultado: Resultado del análisis de Bishop
        config: Configuración de estilo
        
    Returns:
        Figura de matplotlib
    """
    if config is None:
        config = ConfiguracionGrafico()
    
    titulo = f"Análisis de Bishop Modificado - Factor de Seguridad: {resultado.factor_seguridad:.3f}"
    
    fig = graficar_dovelas(perfil_terreno, circulo, resultado.dovelas, titulo, config=config)
    ax = fig.gca()
    
    # Agregar información del resultado
    info_text = f"""Método: Bishop Modificado (Iterativo)
Factor de Seguridad: {resultado.factor_seguridad:.3f}
Iteraciones: {resultado.iteraciones}
Convergió: {'Sí' if resultado.convergio else 'No'}
Dovelas: {len(resultado.dovelas)}
Válido: {'Sí' if resultado.es_valido else 'No'}"""
    
    # Clasificación de estabilidad
    if resultado.factor_seguridad < 1.0:
        clasificacion = "INESTABLE"
        color_fs = 'red'
    elif resultado.factor_seguridad < 1.3:
        clasificacion = "MARGINALMENTE ESTABLE"
        color_fs = 'orange'
    elif resultado.factor_seguridad < 2.0:
        clasificacion = "ESTABLE"
        color_fs = 'green'
    else:
        clasificacion = "MUY ESTABLE"
        color_fs = 'darkgreen'
    
    info_text += f"\nClasificación: {clasificacion}"
    
    # Agregar información de convergencia
    if hasattr(resultado, 'historial_fs') and len(resultado.historial_fs) > 1:
        info_text += f"\nConvergencia: {resultado.historial_fs[-2]:.3f} → {resultado.historial_fs[-1]:.3f}"
    
    # Colocar texto informativo
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Destacar factor de seguridad
    ax.text(0.98, 0.02, f"Fs = {resultado.factor_seguridad:.3f}", 
            transform=ax.transAxes, fontsize=16, fontweight='bold',
            horizontalalignment='right', verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor=color_fs, alpha=0.7, edgecolor='black'))
    
    return fig


def graficar_comparacion_metodos(perfil_terreno: List[Tuple[float, float]], 
                                circulo: CirculoFalla,
                                resultado_fellenius: ResultadoFellenius,
                                resultado_bishop: ResultadoBishop,
                                config: Optional[ConfiguracionGrafico] = None) -> plt.Figure:
    """
    Gráfico comparativo entre métodos de Fellenius y Bishop.
    
    Args:
        perfil_terreno: Lista de puntos del perfil
        circulo: Círculo de falla
        resultado_fellenius: Resultado de Fellenius
        resultado_bishop: Resultado de Bishop
        config: Configuración de estilo
        
    Returns:
        Figura de matplotlib
    """
    if config is None:
        config = ConfiguracionGrafico()
    
    configurar_estilo_grafico()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=config.dpi)
    
    # Gráfico de Fellenius
    _graficar_en_subplot(ax1, perfil_terreno, circulo, resultado_fellenius.dovelas, 
                        f"Fellenius - Fs = {resultado_fellenius.factor_seguridad:.3f}", config)
    
    # Gráfico de Bishop
    _graficar_en_subplot(ax2, perfil_terreno, circulo, resultado_bishop.dovelas, 
                        f"Bishop - Fs = {resultado_bishop.factor_seguridad:.3f}", config)
    
    # Calcular diferencia
    diferencia = ((resultado_bishop.factor_seguridad - resultado_fellenius.factor_seguridad) / 
                  resultado_fellenius.factor_seguridad) * 100
    
    # Título general
    fig.suptitle(f'Comparación de Métodos - Diferencia: {diferencia:+.1f}%', 
                fontsize=16, fontweight='bold')
    
    # Tabla comparativa
    tabla_text = f"""
COMPARACIÓN DE RESULTADOS

                    Fellenius    Bishop
Factor Seguridad:   {resultado_fellenius.factor_seguridad:.3f}       {resultado_bishop.factor_seguridad:.3f}
Método:             Directo      Iterativo
Iteraciones:        1            {resultado_bishop.iteraciones}
Conservador:        {'Más' if resultado_fellenius.factor_seguridad < resultado_bishop.factor_seguridad else 'Menos'}          {'Menos' if resultado_fellenius.factor_seguridad < resultado_bishop.factor_seguridad else 'Más'}

Diferencia: {diferencia:+.1f}%
Recomendación: {'Usar Bishop para diseño final' if abs(diferencia) > 5 else 'Ambos métodos son consistentes'}
"""
    
    fig.text(0.5, 0.02, tabla_text, ha='center', va='bottom', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    return fig


def graficar_con_nivel_freatico(perfil_terreno: List[Tuple[float, float]], 
                               circulo: CirculoFalla,
                               nivel_freatico: List[Tuple[float, float]],
                               dovelas: List[Dovela],
                               factor_seguridad: float,
                               metodo: str = "Análisis",
                               config: Optional[ConfiguracionGrafico] = None) -> plt.Figure:
    """
    Gráfico incluyendo nivel freático.
    
    Args:
        perfil_terreno: Lista de puntos del perfil
        circulo: Círculo de falla
        nivel_freatico: Lista de puntos del nivel freático
        dovelas: Lista de dovelas
        factor_seguridad: Factor de seguridad calculado
        metodo: Nombre del método usado
        config: Configuración de estilo
        
    Returns:
        Figura de matplotlib
    """
    if config is None:
        config = ConfiguracionGrafico()
    
    titulo = f"{metodo} con Nivel Freático - Fs = {factor_seguridad:.3f}"
    fig = graficar_dovelas(perfil_terreno, circulo, dovelas, titulo, config=config)
    ax = fig.gca()
    
    # Graficar nivel freático
    if nivel_freatico:
        x_nf = [p[0] for p in nivel_freatico]
        y_nf = [p[1] for p in nivel_freatico]
        ax.plot(x_nf, y_nf, color=config.color_agua, linewidth=3, 
                label='Nivel freático', linestyle='--')
        
        # Sombrear zona saturada
        x_coords = [p[0] for p in perfil_terreno]
        y_coords = [p[1] for p in perfil_terreno]
        
        # Crear área de agua
        x_agua = []
        y_agua = []
        for x in x_coords:
            y_terreno = _interpolar_elevacion(perfil_terreno, x)
            y_agua_nivel = _interpolar_elevacion(nivel_freatico, x)
            if y_agua_nivel is not None and y_terreno is not None and y_agua_nivel < y_terreno:
                x_agua.extend([x, x])
                y_agua.extend([y_agua_nivel, y_terreno])
        
        if x_agua:
            ax.fill_between(x_coords, [_interpolar_elevacion(nivel_freatico, x) or 0 for x in x_coords],
                           y_coords, where=[(_interpolar_elevacion(nivel_freatico, x) or 0) < y for x, y in zip(x_coords, y_coords)],
                           color=config.color_agua, alpha=0.3, label='Zona saturada')
    
    ax.legend(fontsize=config.leyenda_fontsize)
    return fig


def graficar_convergencia_bishop(historial_fs: List[float],
                                config: Optional[ConfiguracionGrafico] = None) -> plt.Figure:
    """
    Gráfico de convergencia del método de Bishop.
    
    Args:
        historial_fs: Lista de factores de seguridad por iteración
        config: Configuración de estilo
        
    Returns:
        Figura de matplotlib
    """
    if config is None:
        config = ConfiguracionGrafico()
    
    configurar_estilo_grafico()
    fig, ax = plt.subplots(figsize=(10, 6), dpi=config.dpi)
    
    iteraciones = list(range(1, len(historial_fs) + 1))
    
    ax.plot(iteraciones, historial_fs, 'o-', linewidth=2, markersize=8, 
            color='blue', label='Factor de Seguridad')
    
    # Línea de valor final
    ax.axhline(y=historial_fs[-1], color='red', linestyle='--', alpha=0.7,
               label=f'Valor final: {historial_fs[-1]:.3f}')
    
    ax.set_xlabel('Iteración', fontsize=config.etiquetas_fontsize)
    ax.set_ylabel('Factor de Seguridad', fontsize=config.etiquetas_fontsize)
    ax.set_title('Convergencia del Método de Bishop', fontsize=config.titulo_fontsize, fontweight='bold')
    ax.legend(fontsize=config.leyenda_fontsize)
    ax.grid(True, alpha=0.3)
    
    # Mostrar valores en cada punto
    for i, fs in enumerate(historial_fs):
        ax.annotate(f'{fs:.3f}', (i+1, fs), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontsize=9)
    
    plt.tight_layout()
    return fig


# Funciones auxiliares
def _interpolar_elevacion(perfil: List[Tuple[float, float]], x: float) -> Optional[float]:
    """Interpola la elevación en un punto x dado un perfil."""
    if not perfil:
        return None
    
    # Ordenar perfil por x
    perfil_ordenado = sorted(perfil, key=lambda p: p[0])
    
    # Casos extremos
    if x <= perfil_ordenado[0][0]:
        return perfil_ordenado[0][1]
    if x >= perfil_ordenado[-1][0]:
        return perfil_ordenado[-1][1]
    
    # Interpolación lineal
    for i in range(len(perfil_ordenado) - 1):
        x1, y1 = perfil_ordenado[i]
        x2, y2 = perfil_ordenado[i + 1]
        
        if x1 <= x <= x2:
            if x2 == x1:
                return y1
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    
    return None


def _calcular_y_circulo(circulo: CirculoFalla, x: float) -> Optional[float]:
    """Calcula la coordenada y inferior del círculo en x."""
    dx = x - circulo.xc
    if abs(dx) > circulo.radio:
        return None
    
    dy = math.sqrt(circulo.radio**2 - dx**2)
    return circulo.yc - dy  # Parte inferior del círculo


def _dibujar_fuerzas_dovela(ax, dovela: Dovela, y_terreno: float, y_circulo: float, config: ConfiguracionGrafico):
    """Dibuja vectores de fuerza para una dovela."""
    # Vector peso (hacia abajo)
    escala = 0.01  # Escala para visualización
    peso_visual = dovela.peso * escala
    
    ax.arrow(dovela.x_centro, y_terreno, 0, -peso_visual, 
             head_width=0.2, head_length=0.1, fc=config.color_fuerzas, ec=config.color_fuerzas)
    
    # Etiqueta del peso
    ax.text(dovela.x_centro + 0.3, y_terreno - peso_visual/2, f'W={dovela.peso:.0f}kN',
           fontsize=8, color=config.color_fuerzas)


def _graficar_en_subplot(ax, perfil_terreno: List[Tuple[float, float]], 
                        circulo: CirculoFalla, dovelas: List[Dovela], 
                        titulo: str, config: ConfiguracionGrafico):
    """Función auxiliar para graficar en un subplot."""
    # Extraer coordenadas
    x_coords = [p[0] for p in perfil_terreno]
    y_coords = [p[1] for p in perfil_terreno]
    
    # Graficar perfil de terreno
    ax.fill_between(x_coords, y_coords, alpha=0.7, color=config.color_terreno, 
                    label='Terreno', linewidth=2)
    ax.plot(x_coords, y_coords, color='black', linewidth=2)
    
    # Graficar círculo de falla
    circulo_patch = patches.Circle((circulo.xc, circulo.yc), circulo.radio, 
                                  fill=False, color=config.color_circulo, 
                                  linewidth=3, label='Círculo de falla')
    ax.add_patch(circulo_patch)
    
    # Graficar dovelas
    for i, dovela in enumerate(dovelas):
        x_izq = dovela.x_centro - dovela.ancho / 2
        x_der = dovela.x_centro + dovela.ancho / 2
        
        y_terreno = _interpolar_elevacion(perfil_terreno, dovela.x_centro)
        y_circulo = _calcular_y_circulo(circulo, dovela.x_centro)
        
        if y_circulo is not None and y_terreno is not None:
            altura_dovela = y_terreno - y_circulo
            rect = patches.Rectangle((x_izq, y_circulo), dovela.ancho, altura_dovela,
                                   linewidth=1, edgecolor='black', 
                                   facecolor=config.color_dovelas, alpha=0.6)
            ax.add_patch(rect)
    
    # Configurar subplot
    ax.set_xlabel('Distancia (m)')
    ax.set_ylabel('Elevación (m)')
    ax.set_title(titulo, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # Ajustar límites
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    margen = 0.1 * max(x_max - x_min, y_max - y_min)
    
    ax.set_xlim(x_min - margen, x_max + margen)
    ax.set_ylim(y_min - margen, y_max + margen)


def guardar_grafico(fig: plt.Figure, nombre_archivo: str, dpi: int = 300, formato: str = 'png'):
    """
    Guarda un gráfico en archivo.
    
    Args:
        fig: Figura de matplotlib
        nombre_archivo: Nombre del archivo (sin extensión)
        dpi: Resolución en DPI
        formato: Formato de archivo ('png', 'pdf', 'svg', 'jpg')
    """
    archivo_completo = f"{nombre_archivo}.{formato}"
    fig.savefig(archivo_completo, dpi=dpi, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"✅ Gráfico guardado: {archivo_completo}")


def mostrar_grafico(fig: plt.Figure):
    """Muestra un gráfico en pantalla."""
    plt.show()


def cerrar_graficos():
    """Cierra todas las figuras abiertas."""
    plt.close('all')
