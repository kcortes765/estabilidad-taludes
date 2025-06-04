"""
Sistema de Visualización Ultra-Avanzado para Círculos y Taludes

Gráficos profesionales con:
- Visualización de límites geométricos
- Representación 3D del talud
- Animaciones de optimización
- Gráficos interactivos
- Zonas de validez visual
- Mapas de calor de estabilidad
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Polygon, Rectangle
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
import math

from data.models import CirculoFalla, Estrato
from core.circle_constraints import LimitesGeometricos, CalculadorLimites


class VisualizadorAvanzado:
    """Visualizador ultra-avanzado para círculos y taludes"""
    
    def __init__(self):
        # Configuración de colores profesionales
        self.colores = {
            'talud': '#8B4513',           # Marrón tierra
            'circulo_valido': '#2E8B57',   # Verde válido
            'circulo_invalido': '#DC143C', # Rojo inválido
            'circulo_marginal': '#FF8C00', # Naranja marginal
            'limites': '#4169E1',         # Azul límites
            'zona_permitida': '#E6F3FF',  # Azul claro zona
            'zona_prohibida': '#FFE6E6',  # Rojo claro zona
            'dovelas': '#32CD32',         # Verde dovelas
            'fuerzas': '#FF6347',         # Rojo fuerzas
            'agua': '#87CEEB',            # Azul agua
            'grid': '#D3D3D3'             # Gris grid
        }
        
        # Configuración de estilos
        plt.style.use('default')
        plt.rcParams.update({
            'figure.figsize': (14, 10),
            'figure.dpi': 100,
            'font.size': 10,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'legend.fontsize': 10,
            'grid.alpha': 0.3
        })
    
    def plot_talud_con_limites(self, 
                              perfil_terreno: List[Tuple[float, float]],
                              limites: LimitesGeometricos,
                              circulo: Optional[CirculoFalla] = None,
                              mostrar_zonas: bool = True,
                              titulo: str = "Talud con Límites Geométricos") -> plt.Figure:
        """
        Visualiza el talud con límites geométricos y zonas de validez
        """
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        
        # 1. Dibujar talud
        x_terreno = [p[0] for p in perfil_terreno]
        y_terreno = [p[1] for p in perfil_terreno]
        
        ax.fill_between(x_terreno, y_terreno, min(y_terreno) - 2, 
                       color=self.colores['talud'], alpha=0.7, label='Talud')
        ax.plot(x_terreno, y_terreno, color='black', linewidth=2, label='Perfil terreno')
        
        # 2. Mostrar zonas de validez si se solicita
        if mostrar_zonas:
            self._dibujar_zonas_validez(ax, limites)
        
        # 3. Dibujar límites del centro
        self._dibujar_limites_centro(ax, limites)
        
        # 4. Dibujar círculo si se proporciona
        if circulo:
            self._dibujar_circulo_con_validacion(ax, circulo, limites)
        
        # 5. Añadir información de límites
        self._añadir_info_limites(ax, limites)
        
        # Configuración del gráfico
        ax.set_xlim(limites.centro_x_min - 5, limites.centro_x_max + 5)
        ax.set_ylim(min(y_terreno) - 3, limites.centro_y_max + 5)
        ax.set_xlabel('Distancia (m)', fontsize=12)
        ax.set_ylabel('Elevación (m)', fontsize=12)
        ax.set_title(titulo, fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        ax.set_aspect('equal')
        
        plt.tight_layout()
        return fig
    
    def plot_mapa_calor_estabilidad(self,
                                   perfil_terreno: List[Tuple[float, float]],
                                   estrato: Estrato,
                                   limites: LimitesGeometricos,
                                   resolucion: int = 50) -> plt.Figure:
        """
        Crea un mapa de calor mostrando zonas de estabilidad
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        
        # Crear grilla de puntos para evaluar
        x_range = np.linspace(limites.centro_x_min, limites.centro_x_max, resolucion)
        y_range = np.linspace(limites.centro_y_min, limites.centro_y_max, resolucion)
        r_range = np.linspace(limites.radio_min, limites.radio_max, 20)
        
        # Matrices para almacenar resultados
        fs_grid = np.zeros((len(y_range), len(x_range)))
        validez_grid = np.zeros((len(y_range), len(x_range)))
        
        from core.bishop import analizar_bishop
        from core.circle_geometry import GeometriaCirculoAvanzada
        
        geom = GeometriaCirculoAvanzada()
        
        # Evaluar cada punto de la grilla
        for i, y in enumerate(y_range):
            for j, x in enumerate(x_range):
                mejores_fs = []
                validez_promedio = 0
                
                # Probar diferentes radios en cada punto
                for r in r_range[:5]:  # Limitar para velocidad
                    try:
                        circulo = CirculoFalla(x, y, r)
                        
                        # Calcular métricas
                        metricas = geom.calcular_metricas_circulo(circulo, perfil_terreno, estrato, 10)
                        
                        if metricas.es_geometricamente_valido:
                            try:
                                resultado = analizar_bishop(circulo, perfil_terreno, estrato, 10, validar_entrada=False)
                                fs = resultado['factor_seguridad']
                                if 0.5 <= fs <= 10:  # FS razonable
                                    mejores_fs.append(fs)
                                    validez_promedio += metricas.porcentaje_dovelas_validas
                            except:
                                pass
                    except:
                        pass
                
                # Asignar valores a la grilla
                if mejores_fs:
                    fs_grid[i, j] = min(mejores_fs)  # FS mínimo (más crítico)
                    validez_grid[i, j] = validez_promedio / len(mejores_fs)
                else:
                    fs_grid[i, j] = np.nan
                    validez_grid[i, j] = 0
        
        # Mapa de calor de Factor de Seguridad
        im1 = ax1.imshow(fs_grid, extent=[limites.centro_x_min, limites.centro_x_max,
                                         limites.centro_y_min, limites.centro_y_max],
                        origin='lower', cmap='RdYlGn', vmin=0.5, vmax=3.0)
        
        # Dibujar talud en mapa de FS
        x_terreno = [p[0] for p in perfil_terreno]
        y_terreno = [p[1] for p in perfil_terreno]
        ax1.plot(x_terreno, y_terreno, 'k-', linewidth=3, label='Perfil terreno')
        
        ax1.set_title('Mapa de Factor de Seguridad', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Centro X (m)')
        ax1.set_ylabel('Centro Y (m)')
        cbar1 = plt.colorbar(im1, ax=ax1)
        cbar1.set_label('Factor de Seguridad')
        ax1.legend()
        
        # Mapa de calor de Validez
        im2 = ax2.imshow(validez_grid, extent=[limites.centro_x_min, limites.centro_x_max,
                                              limites.centro_y_min, limites.centro_y_max],
                        origin='lower', cmap='Blues', vmin=0, vmax=100)
        
        # Dibujar talud en mapa de validez
        ax2.plot(x_terreno, y_terreno, 'k-', linewidth=3, label='Perfil terreno')
        
        ax2.set_title('Mapa de Validez Geométrica', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Centro X (m)')
        ax2.set_ylabel('Centro Y (m)')
        cbar2 = plt.colorbar(im2, ax=ax2)
        cbar2.set_label('Porcentaje de Validez (%)')
        ax2.legend()
        
        plt.tight_layout()
        return fig
    
    def plot_analisis_3d_talud(self,
                              perfil_terreno: List[Tuple[float, float]],
                              circulo: CirculoFalla,
                              estrato: Estrato) -> plt.Figure:
        """
        Visualización 3D del talud y círculo de falla
        """
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Crear superficie del talud (extruir perfil)
        x_terreno = np.array([p[0] for p in perfil_terreno])
        y_terreno = np.array([p[1] for p in perfil_terreno])
        
        # Extruir en dirección Z (perpendicular al talud)
        z_width = 20  # Ancho del talud en 3D
        Z = np.linspace(-z_width/2, z_width/2, 20)
        X, Z = np.meshgrid(x_terreno, Z)
        Y = np.tile(y_terreno, (len(Z), 1))
        
        # Dibujar superficie del talud
        ax.plot_surface(X, Y, Z, alpha=0.6, color=self.colores['talud'])
        
        # Dibujar círculo de falla en 3D (como cilindro)
        theta = np.linspace(0, 2*np.pi, 50)
        z_circle = np.linspace(-z_width/2, z_width/2, 10)
        
        # Coordenadas del círculo
        x_circle = circulo.centro_x + circulo.radio * np.cos(theta)
        y_circle = circulo.centro_y + circulo.radio * np.sin(theta)
        
        # Crear superficie cilíndrica
        THETA, Z_CIR = np.meshgrid(theta, z_circle)
        X_CIR = circulo.centro_x + circulo.radio * np.cos(THETA)
        Y_CIR = circulo.centro_y + circulo.radio * np.sin(THETA)
        Z_CIR = Z_CIR
        
        ax.plot_surface(X_CIR, Y_CIR, Z_CIR, alpha=0.3, color=self.colores['circulo_valido'])
        
        # Configurar ejes
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Vista 3D: Talud y Círculo de Falla', fontsize=16, fontweight='bold')
        
        return fig
    
    def plot_dashboard_completo_avanzado(self,
                                       perfil_terreno: List[Tuple[float, float]],
                                       circulo: CirculoFalla,
                                       estrato: Estrato,
                                       limites: LimitesGeometricos) -> plt.Figure:
        """
        Dashboard completo ultra-avanzado con múltiples paneles
        """
        fig = plt.figure(figsize=(20, 16))
        
        # Layout: 3x3 grid
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Panel 1: Talud con límites (grande)
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        self._plot_talud_principal(ax1, perfil_terreno, circulo, limites)
        
        # Panel 2: Métricas y validaciones
        ax2 = fig.add_subplot(gs[0, 2])
        self._plot_metricas_texto(ax2, circulo, perfil_terreno, estrato, limites)
        
        # Panel 3: Distribución de dovelas
        ax3 = fig.add_subplot(gs[1, 2])
        self._plot_distribucion_dovelas(ax3, circulo, perfil_terreno, estrato)
        
        # Panel 4: Análisis de fuerzas
        ax4 = fig.add_subplot(gs[2, 0])
        self._plot_analisis_fuerzas(ax4, circulo, perfil_terreno, estrato)
        
        # Panel 5: Sensibilidad de parámetros
        ax5 = fig.add_subplot(gs[2, 1])
        self._plot_sensibilidad_parametros(ax5, circulo, perfil_terreno, estrato)
        
        # Panel 6: Recomendaciones
        ax6 = fig.add_subplot(gs[2, 2])
        self._plot_recomendaciones(ax6, circulo, limites)
        
        fig.suptitle('Dashboard Ultra-Avanzado de Análisis de Círculos', 
                    fontsize=18, fontweight='bold')
        
        return fig
    
    def _dibujar_zonas_validez(self, ax, limites: LimitesGeometricos):
        """Dibuja zonas de validez visual"""
        # Zona permitida para el centro
        zona_centro = Rectangle(
            (limites.centro_x_min, limites.centro_y_min),
            limites.centro_x_max - limites.centro_x_min,
            limites.centro_y_max - limites.centro_y_min,
            facecolor=self.colores['zona_permitida'],
            alpha=0.3,
            label='Zona permitida centro'
        )
        ax.add_patch(zona_centro)
    
    def _dibujar_limites_centro(self, ax, limites: LimitesGeometricos):
        """Dibuja límites del centro del círculo"""
        # Líneas de límites
        ax.axvline(limites.centro_x_min, color=self.colores['limites'], 
                  linestyle='--', alpha=0.7, label='Límites centro')
        ax.axvline(limites.centro_x_max, color=self.colores['limites'], linestyle='--', alpha=0.7)
        ax.axhline(limites.centro_y_min, color=self.colores['limites'], linestyle='--', alpha=0.7)
        ax.axhline(limites.centro_y_max, color=self.colores['limites'], linestyle='--', alpha=0.7)
        
        # Anotaciones
        ax.annotate(f'X_min: {limites.centro_x_min:.1f}', 
                   xy=(limites.centro_x_min, limites.centro_y_max), 
                   xytext=(5, 5), textcoords='offset points', fontsize=9)
        ax.annotate(f'X_max: {limites.centro_x_max:.1f}', 
                   xy=(limites.centro_x_max, limites.centro_y_max), 
                   xytext=(-50, 5), textcoords='offset points', fontsize=9)
    
    def _dibujar_circulo_con_validacion(self, ax, circulo: CirculoFalla, limites: LimitesGeometricos):
        """Dibuja círculo con código de colores según validación"""
        calculador = CalculadorLimites()
        validacion = calculador.validar_y_corregir_circulo(circulo, limites, False)
        
        # Color según validez
        if validacion.es_valido:
            color = self.colores['circulo_valido']
            label = 'Círculo VÁLIDO'
        else:
            color = self.colores['circulo_invalido']
            label = 'Círculo INVÁLIDO'
        
        # Dibujar círculo
        circle = Circle((circulo.centro_x, circulo.centro_y), circulo.radio, 
                       fill=False, color=color, linewidth=3, label=label)
        ax.add_patch(circle)
        
        # Marcar centro
        ax.plot(circulo.centro_x, circulo.centro_y, 'o', color=color, markersize=8)
        
        # Mostrar violaciones si existen
        if validacion.violaciones:
            for i, violacion in enumerate(validacion.violaciones[:3]):  # Máximo 3
                ax.text(circulo.centro_x, circulo.centro_y - circulo.radio - (i+1)*2,
                       f"⚠️ {violacion}", fontsize=8, ha='center', color='red')
    
    def _añadir_info_limites(self, ax, limites: LimitesGeometricos):
        """Añade información detallada de límites"""
        info_text = f"""LÍMITES GEOMÉTRICOS:
Radio: {limites.radio_min:.1f} - {limites.radio_max:.1f} m
Ancho talud: {limites.ancho_talud:.1f} m
Altura talud: {limites.altura_talud:.1f} m
Pendiente: {limites.pendiente_talud:.1f}°"""
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
               verticalalignment='top', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def _plot_talud_principal(self, ax, perfil_terreno, circulo, limites):
        """Panel principal del talud"""
        # Reutilizar lógica del método principal
        x_terreno = [p[0] for p in perfil_terreno]
        y_terreno = [p[1] for p in perfil_terreno]
        
        ax.fill_between(x_terreno, y_terreno, min(y_terreno) - 2, 
                       color=self.colores['talud'], alpha=0.7)
        ax.plot(x_terreno, y_terreno, 'k-', linewidth=2)
        
        self._dibujar_zonas_validez(ax, limites)
        self._dibujar_limites_centro(ax, limites)
        self._dibujar_circulo_con_validacion(ax, circulo, limites)
        
        ax.set_title('Vista Principal: Talud y Círculo', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
    
    def _plot_metricas_texto(self, ax, circulo, perfil_terreno, estrato, limites):
        """Panel de métricas y validaciones"""
        ax.axis('off')
        
        from core.circle_geometry import GeometriaCirculoAvanzada
        geom = GeometriaCirculoAvanzada()
        
        try:
            metricas = geom.calcular_metricas_circulo(circulo, perfil_terreno, estrato, 10)
            
            metrics_text = f"""MÉTRICAS DEL CÍRCULO:
            
✅ Dovelas válidas: {metricas.num_dovelas_validas}/{metricas.num_dovelas_total}
📊 Validez: {metricas.porcentaje_dovelas_validas:.1f}%
📏 Longitud arco: {metricas.longitud_arco:.2f} m
🌊 Cobertura: {metricas.cobertura_terreno:.1f}%
⚖️ Fuerzas: {metricas.suma_fuerzas_actuantes:.1f} N

PARÁMETROS:
📍 Centro: ({circulo.centro_x:.1f}, {circulo.centro_y:.1f})
📐 Radio: {circulo.radio:.1f} m

FACTOR SEGURIDAD:
🎯 FS: {metricas.factor_seguridad:.3f}"""
            
        except Exception as e:
            metrics_text = f"Error calculando métricas:\n{str(e)}"
        
        ax.text(0.05, 0.95, metrics_text, transform=ax.transAxes,
               verticalalignment='top', fontsize=9, family='monospace',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    def _plot_distribucion_dovelas(self, ax, circulo, perfil_terreno, estrato):
        """Panel de distribución de dovelas"""
        # Simplificado para demostración
        from core.geometry import crear_dovelas
        
        try:
            dovelas = crear_dovelas(circulo, perfil_terreno, 10)
            anchos = [d.ancho for d in dovelas if d.ancho > 0]
            
            if anchos:
                ax.hist(anchos, bins=8, color=self.colores['dovelas'], alpha=0.7)
                ax.set_title('Distribución Anchos Dovelas', fontsize=10)
                ax.set_xlabel('Ancho (m)')
                ax.set_ylabel('Frecuencia')
            else:
                ax.text(0.5, 0.5, 'Sin dovelas\nvválidas', ha='center', va='center', 
                       transform=ax.transAxes)
        except Exception as e:
            ax.text(0.5, 0.5, f'Error:\n{str(e)}', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=8)
    
    def _plot_analisis_fuerzas(self, ax, circulo, perfil_terreno, estrato):
        """Panel de análisis de fuerzas"""
        ax.text(0.5, 0.5, 'Análisis de Fuerzas\n(En desarrollo)', 
               ha='center', va='center', transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    def _plot_sensibilidad_parametros(self, ax, circulo, perfil_terreno, estrato):
        """Panel de sensibilidad de parámetros"""
        ax.text(0.5, 0.5, 'Análisis de Sensibilidad\n(En desarrollo)', 
               ha='center', va='center', transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='orange', alpha=0.3))
    
    def _plot_recomendaciones(self, ax, circulo, limites):
        """Panel de recomendaciones"""
        calculador = CalculadorLimites()
        validacion = calculador.validar_y_corregir_circulo(circulo, limites, True)
        
        ax.axis('off')
        
        if validacion.es_valido:
            reco_text = "✅ CÍRCULO VÁLIDO\n\nTodas las validaciones\npasaron correctamente."
            color = 'lightgreen'
        else:
            reco_text = "❌ CÍRCULO INVÁLIDO\n\nSugerencias:\n"
            for sug in validacion.sugerencias[:3]:
                reco_text += f"• {sug}\n"
            color = 'lightcoral'
        
        ax.text(0.05, 0.95, reco_text, transform=ax.transAxes,
               verticalalignment='top', fontsize=9,
               bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))
