"""
Visualización Avanzada de Círculos para Análisis de Estabilidad de Taludes

Este módulo proporciona herramientas completas de visualización:
- Gráficos de círculos con terreno
- Diagnóstico visual de dovelas
- Comparación de múltiples círculos
- Animaciones de optimización
- Dashboards interactivos

Autor: Sistema de Análisis de Taludes
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
from typing import List, Tuple, Optional, Dict, Any
from matplotlib.colors import LinearSegmentedColormap

from data.models import CirculoFalla, Estrato, Dovela
from core.circle_geometry import GeometriaCirculoAvanzada, MetricasCirculo
from core.geometry import crear_dovelas


class VisualizadorCirculos:
    """Clase principal para visualización avanzada de círculos"""
    
    def __init__(self, figsize: Tuple[float, float] = (12, 8)):
        self.figsize = figsize
        self.geometria = GeometriaCirculoAvanzada()
        
        # Configuración de colores
        self.colores = {
            'terreno': '#8B4513',
            'circulo_valido': '#2E8B57',
            'circulo_invalido': '#DC143C',
            'circulo_warning': '#FF8C00',
            'dovela_valida': '#4169E1',
            'dovela_invalida': '#FF4500',
            'interseccion': '#FF1493',
            'centro': '#000000'
        }
        
    def plot_circulo_basico(self, 
                           circulo: CirculoFalla,
                           perfil_terreno: List[Tuple[float, float]],
                           titulo: str = "Análisis de Círculo de Falla",
                           mostrar_intersecciones: bool = True,
                           mostrar_centro: bool = True) -> plt.Figure:
        """
        Gráfico básico de círculo con terreno.
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Dibujar terreno
        terreno_x = [p[0] for p in perfil_terreno]
        terreno_y = [p[1] for p in perfil_terreno]
        ax.fill_between(terreno_x, terreno_y, alpha=0.7, color=self.colores['terreno'], 
                       label='Terreno')
        ax.plot(terreno_x, terreno_y, 'k-', linewidth=2)
        
        # Dibujar círculo
        circulo_patch = patches.Circle(
            (circulo.centro_x, circulo.centro_y), 
            circulo.radio, 
            fill=False, 
            edgecolor=self.colores['circulo_valido'], 
            linewidth=2,
            label='Círculo de Falla'
        )
        ax.add_patch(circulo_patch)
        
        # Mostrar centro si se solicita
        if mostrar_centro:
            ax.plot(circulo.centro_x, circulo.centro_y, 'ko', markersize=8, 
                   label='Centro')
        
        # Mostrar intersecciones si se solicita
        if mostrar_intersecciones:
            intersecciones = self.geometria.calcular_intersecciones_circulo_terreno(
                circulo, perfil_terreno)
            if intersecciones:
                int_x = [p[0] for p in intersecciones]
                int_y = [p[1] for p in intersecciones]
                ax.plot(int_x, int_y, 'o', color=self.colores['interseccion'], 
                       markersize=8, label='Intersecciones')
        
        # Configuración de ejes
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlabel('Distancia (m)')
        ax.set_ylabel('Elevación (m)')
        ax.set_title(titulo)
        
        # Ajustar límites
        margen = circulo.radio * 0.2
        ax.set_xlim(circulo.centro_x - circulo.radio - margen, 
                   circulo.centro_x + circulo.radio + margen)
        ax.set_ylim(circulo.centro_y - circulo.radio - margen, 
                   circulo.centro_y + circulo.radio + margen)
        
        plt.tight_layout()
        return fig
    
    def plot_circulo_con_dovelas(self, 
                                circulo: CirculoFalla,
                                perfil_terreno: List[Tuple[float, float]],
                                estrato: Estrato,
                                num_dovelas: int = 10,
                                titulo: str = "Círculo con Dovelas") -> plt.Figure:
        """
        Visualiza círculo con dovelas coloreadas por validez.
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Dibujar terreno
        terreno_x = [p[0] for p in perfil_terreno]
        terreno_y = [p[1] for p in perfil_terreno]
        ax.fill_between(terreno_x, terreno_y, alpha=0.7, color=self.colores['terreno'])
        ax.plot(terreno_x, terreno_y, 'k-', linewidth=2)
        
        # Dibujar círculo
        circulo_patch = patches.Circle(
            (circulo.centro_x, circulo.centro_y), 
            circulo.radio, 
            fill=False, 
            edgecolor='black', 
            linewidth=1,
            alpha=0.5
        )
        ax.add_patch(circulo_patch)
        
        try:
            # Crear dovelas
            dovelas = crear_dovelas(circulo, perfil_terreno, estrato, num_dovelas)
            
            # Dibujar dovelas
            for i, dovela in enumerate(dovelas):
                # Determinar color basado en validez de dovela
                if hasattr(dovela, 'es_valida') and not dovela.es_valida:
                    color = self.colores['dovela_invalida']
                    alpha = 0.8
                else:
                    color = self.colores['dovela_valida']
                    alpha = 0.6
                
                # Dibujar rectángulo de dovela (simplificado)
                ancho_dovela = circulo.radio * 2 / num_dovelas
                x_centro = circulo.centro_x - circulo.radio + (i + 0.5) * ancho_dovela
                
                # Calcular altura aproximada de dovela
                y_terreno = np.interp(x_centro, terreno_x, terreno_y)
                y_circulo = circulo.centro_y - math.sqrt(circulo.radio**2 - (x_centro - circulo.centro_x)**2)
                altura_dovela = max(0, y_terreno - y_circulo)
                
                if altura_dovela > 0:
                    rect = patches.Rectangle(
                        (x_centro - ancho_dovela/2, y_circulo),
                        ancho_dovela, altura_dovela,
                        facecolor=color, alpha=alpha,
                        edgecolor='black', linewidth=0.5
                    )
                    ax.add_patch(rect)
                    
                    # Añadir número de dovela
                    ax.text(x_centro, y_circulo + altura_dovela/2, str(i+1),
                           ha='center', va='center', fontsize=8, fontweight='bold')
            
            # Información de dovelas
            num_validas = len(dovelas)
            porcentaje = (num_validas / num_dovelas) * 100
            ax.text(0.02, 0.98, f'Dovelas: {num_validas}/{num_dovelas} ({porcentaje:.1f}%)',
                   transform=ax.transAxes, fontsize=10, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                   verticalalignment='top')
                   
        except Exception as e:
            ax.text(0.02, 0.98, f'Error creando dovelas: {str(e)}',
                   transform=ax.transAxes, fontsize=10,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="red", alpha=0.8),
                   verticalalignment='top', color='white')
        
        # Configuración
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Distancia (m)')
        ax.set_ylabel('Elevación (m)')
        ax.set_title(titulo)
        
        plt.tight_layout()
        return fig
    
    def plot_diagnostico_completo(self, 
                                 circulo: CirculoFalla,
                                 perfil_terreno: List[Tuple[float, float]],
                                 estrato: Estrato,
                                 num_dovelas: int = 10) -> plt.Figure:
        """
        Dashboard completo de diagnóstico de círculo.
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Layout: 2x2 grid
        gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.3, wspace=0.3)
        
        # 1. Gráfico principal con dovelas
        ax1 = fig.add_subplot(gs[0, :])
        self._plot_circulo_principal(ax1, circulo, perfil_terreno, estrato, num_dovelas)
        
        # 2. Métricas de validación
        ax2 = fig.add_subplot(gs[1, 0])
        self._plot_metricas_validacion(ax2, circulo, perfil_terreno, estrato, num_dovelas)
        
        # 3. Información geométrica
        ax3 = fig.add_subplot(gs[1, 1])
        self._plot_info_geometrica(ax3, circulo, perfil_terreno)
        
        # 4. Recomendaciones
        ax4 = fig.add_subplot(gs[2, :])
        self._plot_recomendaciones(ax4, circulo, perfil_terreno, estrato, num_dovelas)
        
        fig.suptitle('Diagnóstico Completo de Círculo de Falla', fontsize=16, fontweight='bold')
        return fig
    
    def _plot_circulo_principal(self, ax, circulo, perfil_terreno, estrato, num_dovelas):
        """Subplot principal con círculo y dovelas"""
        # Dibujar terreno
        terreno_x = [p[0] for p in perfil_terreno]
        terreno_y = [p[1] for p in perfil_terreno]
        ax.fill_between(terreno_x, terreno_y, alpha=0.7, color=self.colores['terreno'])
        ax.plot(terreno_x, terreno_y, 'k-', linewidth=2)
        
        # Validar círculo
        validaciones = self.geometria.validar_circulo_completo(
            circulo, perfil_terreno, estrato, num_dovelas)
        
        # Determinar color del círculo basado en validación
        errores = [v for v in validaciones if not v.es_valido and v.severidad == "ERROR"]
        warnings = [v for v in validaciones if not v.es_valido and v.severidad == "WARNING"]
        
        if errores:
            color_circulo = self.colores['circulo_invalido']
            alpha_circulo = 0.8
        elif warnings:
            color_circulo = self.colores['circulo_warning']
            alpha_circulo = 0.8
        else:
            color_circulo = self.colores['circulo_valido']
            alpha_circulo = 0.6
        
        # Dibujar círculo
        circulo_patch = patches.Circle(
            (circulo.centro_x, circulo.centro_y), 
            circulo.radio, 
            fill=False, 
            edgecolor=color_circulo, 
            linewidth=3,
            alpha=alpha_circulo
        )
        ax.add_patch(circulo_patch)
        
        # Centro
        ax.plot(circulo.centro_x, circulo.centro_y, 'ko', markersize=8)
        
        # Intersecciones
        intersecciones = self.geometria.calcular_intersecciones_circulo_terreno(
            circulo, perfil_terreno)
        if intersecciones:
            int_x = [p[0] for p in intersecciones]
            int_y = [p[1] for p in intersecciones]
            ax.plot(int_x, int_y, 'o', color=self.colores['interseccion'], 
                   markersize=10, label=f'Intersecciones ({len(intersecciones)})')
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('Vista Principal - Círculo de Falla')
        ax.legend()
    
    def _plot_metricas_validacion(self, ax, circulo, perfil_terreno, estrato, num_dovelas):
        """Subplot con métricas de validación"""
        ax.axis('off')
        
        # Calcular métricas
        metricas = self.geometria.calcular_metricas_circulo(
            circulo, perfil_terreno, estrato, num_dovelas)
        
        # Texto de métricas
        texto_metricas = f"""
MÉTRICAS DE VALIDACIÓN

🎯 Geometría:
   • Centro: ({metricas.centro_x:.1f}, {metricas.centro_y:.1f})
   • Radio: {metricas.radio:.1f} m
   • Cobertura: {metricas.cobertura_terreno:.1f}%

🔧 Dovelas:
   • Válidas: {metricas.num_dovelas_validas}/{metricas.num_dovelas_total}
   • Porcentaje: {metricas.porcentaje_dovelas_validas:.1f}%
   • Fuerzas: {metricas.suma_fuerzas_actuantes:.1f} N

✅ Estado:
   • Geométrico: {'✓' if metricas.es_geometricamente_valido else '✗'}
   • Computacional: {'✓' if metricas.es_computacionalmente_valido else '✗'}
        """
        
        ax.text(0.05, 0.95, texto_metricas, transform=ax.transAxes,
               fontsize=10, fontfamily='monospace',
               verticalalignment='top',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    def _plot_info_geometrica(self, ax, circulo, perfil_terreno):
        """Subplot con información geométrica detallada"""
        ax.axis('off')
        
        # Calcular información geométrica
        intersecciones = self.geometria.calcular_intersecciones_circulo_terreno(
            circulo, perfil_terreno)
        longitud_arco = self.geometria.calcular_longitud_arco_terreno(
            circulo, perfil_terreno)
        
        # Límites del terreno
        x_min = min(p[0] for p in perfil_terreno)
        x_max = max(p[0] for p in perfil_terreno)
        y_min = min(p[1] for p in perfil_terreno)
        y_max = max(p[1] for p in perfil_terreno)
        
        texto_geometria = f"""
INFORMACIÓN GEOMÉTRICA

🌍 Terreno:
   • X: {x_min:.1f} → {x_max:.1f} m
   • Y: {y_min:.1f} → {y_max:.1f} m
   • Puntos: {len(perfil_terreno)}

⭕ Círculo vs Terreno:
   • Intersecciones: {len(intersecciones)}
   • Longitud arco: {longitud_arco:.2f} m
   • Circunferencia: {2*math.pi*circulo.radio:.2f} m

📐 Relaciones:
   • Distancia centro-terreno: {self._distancia_centro_terreno(circulo, perfil_terreno):.2f} m
   • Radio/Altura terreno: {circulo.radio/(y_max-y_min):.2f}
        """
        
        ax.text(0.05, 0.95, texto_geometria, transform=ax.transAxes,
               fontsize=10, fontfamily='monospace',
               verticalalignment='top',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    def _plot_recomendaciones(self, ax, circulo, perfil_terreno, estrato, num_dovelas):
        """Subplot con recomendaciones de mejora"""
        ax.axis('off')
        
        # Validaciones
        validaciones = self.geometria.validar_circulo_completo(
            circulo, perfil_terreno, estrato, num_dovelas)
        
        # Generar recomendaciones
        recomendaciones = []
        
        for validacion in validaciones:
            if not validacion.es_valido:
                if validacion.tipo.value == "interseccion_terreno":
                    recomendaciones.append("🔧 Ajustar posición del círculo para intersectar el terreno")
                elif validacion.tipo.value == "cobertura_suficiente":
                    recomendaciones.append("📏 Aumentar radio para mayor cobertura del terreno")
                elif validacion.tipo.value == "posicion_centro":
                    recomendaciones.append("📍 Mover centro a posición más apropiada")
                elif validacion.tipo.value == "radio_apropiado":
                    recomendaciones.append("⚙️ Ajustar radio a rango apropiado")
                elif validacion.tipo.value == "dovelas_validas":
                    recomendaciones.append("🔨 Modificar geometría para crear dovelas válidas")
        
        if not recomendaciones:
            recomendaciones.append("✅ Círculo válido - No se requieren ajustes")
        
        # Texto de recomendaciones
        texto_recom = "RECOMENDACIONES DE MEJORA\n\n" + "\n".join(recomendaciones)
        
        # Color de fondo basado en estado
        errores = [v for v in validaciones if not v.es_valido and v.severidad == "ERROR"]
        color_fondo = "lightcoral" if errores else "lightgreen"
        
        ax.text(0.05, 0.95, texto_recom, transform=ax.transAxes,
               fontsize=11, fontweight='bold',
               verticalalignment='top',
               bbox=dict(boxstyle="round,pad=0.5", facecolor=color_fondo, alpha=0.8))
    
    def _distancia_centro_terreno(self, circulo, perfil_terreno):
        """Calcula distancia mínima del centro al terreno"""
        distancia_min = float('inf')
        
        for punto in perfil_terreno:
            dist = math.sqrt((circulo.centro_x - punto[0])**2 + 
                           (circulo.centro_y - punto[1])**2)
            distancia_min = min(distancia_min, dist)
            
        return distancia_min
    
    def plot_comparacion_circulos(self, 
                                 circulos: List[CirculoFalla],
                                 perfil_terreno: List[Tuple[float, float]],
                                 nombres: Optional[List[str]] = None,
                                 titulo: str = "Comparación de Círculos") -> plt.Figure:
        """
        Compara múltiples círculos en un solo gráfico.
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Dibujar terreno
        terreno_x = [p[0] for p in perfil_terreno]
        terreno_y = [p[1] for p in perfil_terreno]
        ax.fill_between(terreno_x, terreno_y, alpha=0.7, color=self.colores['terreno'])
        ax.plot(terreno_x, terreno_y, 'k-', linewidth=2, label='Terreno')
        
        # Colores para múltiples círculos
        colores_multiples = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        
        if nombres is None:
            nombres = [f'Círculo {i+1}' for i in range(len(circulos))]
        
        # Dibujar cada círculo
        for i, circulo in enumerate(circulos):
            color = colores_multiples[i % len(colores_multiples)]
            
            # Círculo
            circulo_patch = patches.Circle(
                (circulo.centro_x, circulo.centro_y), 
                circulo.radio, 
                fill=False, 
                edgecolor=color, 
                linewidth=2,
                alpha=0.7,
                label=nombres[i]
            )
            ax.add_patch(circulo_patch)
            
            # Centro
            ax.plot(circulo.centro_x, circulo.centro_y, 'o', color=color, markersize=8)
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlabel('Distancia (m)')
        ax.set_ylabel('Elevación (m)')
        ax.set_title(titulo)
        
        plt.tight_layout()
        return fig


def demo_visualizacion_circulos():
    """Función de demostración de las capacidades de visualización"""
    # Crear terreno de ejemplo
    perfil_terreno = [
        (0, 10),
        (12, 10),
        (20, 0),
        (40, 0)
    ]
    
    # Crear estrato de ejemplo
    estrato = Estrato(cohesion=20, phi_grados=25, gamma=18)
    
    # Crear círculos de ejemplo
    circulo_bueno = CirculoFalla(16, 8, 12)
    circulo_malo = CirculoFalla(5, 5, 8)
    
    # Visualizador
    viz = VisualizadorCirculos()
    
    # Generar gráficos
    fig1 = viz.plot_circulo_basico(circulo_bueno, perfil_terreno, "Círculo Básico")
    fig2 = viz.plot_circulo_con_dovelas(circulo_bueno, perfil_terreno, estrato, 10, "Círculo con Dovelas")
    fig3 = viz.plot_diagnostico_completo(circulo_bueno, perfil_terreno, estrato, 10)
    fig4 = viz.plot_comparacion_circulos([circulo_bueno, circulo_malo], perfil_terreno, 
                                        ["Círculo Bueno", "Círculo Malo"], "Comparación")
    
    plt.show()


if __name__ == "__main__":
    demo_visualizacion_circulos()
