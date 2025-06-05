"""
Integración de matplotlib con la interfaz gráfica.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import customtkinter as ctk
import tkinter as tk
import numpy as np
from typing import Optional

from core.geometry import crear_perfil_simple
from data.models import CirculoFalla
from visualization.plotting import *
import math


class PlottingPanel(ctk.CTkFrame):
    """Panel principal de visualización con matplotlib integrado."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.current_perfil = None
        self.current_circulo = None
        self.current_bishop_result = None
        self.current_fellenius_result = None
        self.centro_seleccionado = None  # Para almacenar centro seleccionado
        self.modo_seleccion = False  # Estado de selección interactiva
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz del panel de plotting."""
        # Título
        title = ctk.CTkLabel(self, text="Visualización", 
                           font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=10)
        
        # Frame para controles
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # Botón para selección interactiva
        self.btn_seleccionar_centro = ctk.CTkButton(
            control_frame, 
            text="📍 Seleccionar Centro",
            command=self.toggle_modo_seleccion,
            width=150,
            fg_color="green"
        )
        self.btn_seleccionar_centro.pack(side="left", padx=5, pady=5)
        
        # Control de radio dinámico
        radio_frame = ctk.CTkFrame(control_frame)
        radio_frame.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(radio_frame, text="Radio:", font=ctk.CTkFont(size=12)).pack(side="left", padx=2)
        
        self.radio_entry = ctk.CTkEntry(radio_frame, width=60)
        self.radio_entry.pack(side="left", padx=2)
        self.radio_entry.insert(0, "10.0")
        self.radio_entry.bind("<KeyRelease>", self.on_radio_change)
        
        # Slider para radio
        self.radio_slider = ctk.CTkSlider(
            radio_frame, 
            from_=5, 
            to=50, 
            number_of_steps=45,
            command=self.on_radio_slider_change
        )
        self.radio_slider.pack(side="left", padx=5)
        self.radio_slider.set(10.0)
        
        # Label de instrucciones
        self.label_instrucciones = ctk.CTkLabel(
            control_frame,
            text="1️⃣ Configure geometría → 2️⃣ Seleccione centro → 3️⃣ Analice",
            font=ctk.CTkFont(size=12)
        )
        self.label_instrucciones.pack(side="left", padx=10, pady=5)
        
        # Notebook para diferentes tipos de gráficos
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tabs
        self.notebook.add("Geometría")
        self.notebook.add("Análisis")
        self.notebook.add("Comparación")
        self.notebook.add("Convergencia")
        
        # Configurar cada tab
        self.setup_geometry_tab()
        self.setup_analysis_tab()
        self.setup_comparison_tab()
        self.setup_convergence_tab()
        
    def setup_geometry_tab(self):
        """Configurar tab de geometría."""
        tab = self.notebook.tab("Geometría")
        
        # Frame para matplotlib
        plot_frame = tk.Frame(tab)
        plot_frame.pack(fill="both", expand=True)
        
        # Crear figura
        self.geom_fig = Figure(figsize=(8, 6), dpi=100)
        self.geom_ax = self.geom_fig.add_subplot(111)
        
        # Canvas
        self.geom_canvas = FigureCanvasTkAgg(self.geom_fig, plot_frame)
        self.geom_canvas.draw()
        self.geom_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Event handler para clics en el gráfico
        self.geom_canvas.mpl_connect('button_press_event', self.on_click_geometry)
        self.geom_canvas.mpl_connect('motion_notify_event', self.on_mouse_move_geometry)
        
        # Variables para círculo preview
        self.circulo_preview = None
        self.radio_actual = 10.0  # Radio por defecto
        
        # Toolbar
        toolbar_frame = tk.Frame(tab)
        toolbar_frame.pack(fill="x")
        self.geom_toolbar = NavigationToolbar2Tk(self.geom_canvas, toolbar_frame)
        self.geom_toolbar.update()
        
        # Inicializar con gráfico vacío
        self.plot_empty_geometry()
        
    def setup_analysis_tab(self):
        """Configurar tab de análisis."""
        tab = self.notebook.tab("Análisis")
        
        # Frame para matplotlib
        plot_frame = tk.Frame(tab)
        plot_frame.pack(fill="both", expand=True)
        
        # Crear figura
        self.analysis_fig = Figure(figsize=(8, 6), dpi=100)
        self.analysis_ax = self.analysis_fig.add_subplot(111)
        
        # Canvas
        self.analysis_canvas = FigureCanvasTkAgg(self.analysis_fig, plot_frame)
        self.analysis_canvas.draw()
        self.analysis_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Toolbar
        toolbar_frame = tk.Frame(tab)
        toolbar_frame.pack(fill="x")
        self.analysis_toolbar = NavigationToolbar2Tk(self.analysis_canvas, toolbar_frame)
        self.analysis_toolbar.update()
        
        # Inicializar con gráfico vacío
        self.plot_empty_analysis()
        
    def setup_comparison_tab(self):
        """Configurar tab de comparación."""
        tab = self.notebook.tab("Comparación")
        
        # Frame para matplotlib
        plot_frame = tk.Frame(tab)
        plot_frame.pack(fill="both", expand=True)
        
        # Crear figura
        self.comp_fig = Figure(figsize=(8, 6), dpi=100)
        self.comp_ax = self.comp_fig.add_subplot(111)
        
        # Canvas
        self.comp_canvas = FigureCanvasTkAgg(self.comp_fig, plot_frame)
        self.comp_canvas.draw()
        self.comp_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Toolbar
        toolbar_frame = tk.Frame(tab)
        toolbar_frame.pack(fill="x")
        self.comp_toolbar = NavigationToolbar2Tk(self.comp_canvas, toolbar_frame)
        self.comp_toolbar.update()
        
        # Inicializar con gráfico vacío
        self.plot_empty_comparison()
        
    def setup_convergence_tab(self):
        """Configurar tab de convergencia."""
        tab = self.notebook.tab("Convergencia")
        
        # Frame para matplotlib
        plot_frame = tk.Frame(tab)
        plot_frame.pack(fill="both", expand=True)
        
        # Crear figura
        self.conv_fig = Figure(figsize=(8, 6), dpi=100)
        self.conv_ax = self.conv_fig.add_subplot(111)
        
        # Canvas
        self.conv_canvas = FigureCanvasTkAgg(self.conv_fig, plot_frame)
        self.conv_canvas.draw()
        self.conv_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Toolbar
        toolbar_frame = tk.Frame(tab)
        toolbar_frame.pack(fill="x")
        self.conv_toolbar = NavigationToolbar2Tk(self.conv_canvas, toolbar_frame)
        self.conv_toolbar.update()
        
        # Inicializar con gráfico vacío
        self.plot_empty_convergence()
    
    def plot_empty_geometry(self):
        """Plotear geometría vacía."""
        self.geom_ax.clear()
        self.geom_ax.set_title("Geometría del Talud")
        self.geom_ax.set_xlabel("Distancia (m)")
        self.geom_ax.set_ylabel("Elevación (m)")
        self.geom_ax.grid(True, alpha=0.3)
        self.geom_ax.text(0.5, 0.5, "Configure los parámetros y presione 'Analizar'", 
                         transform=self.geom_ax.transAxes, ha='center', va='center',
                         fontsize=12, alpha=0.7)
        self.geom_fig.tight_layout()
        self.geom_canvas.draw()
    
    def plot_empty_analysis(self):
        """Plotear análisis vacío."""
        self.analysis_ax.clear()
        self.analysis_ax.set_title("Análisis de Estabilidad")
        self.analysis_ax.set_xlabel("Distancia (m)")
        self.analysis_ax.set_ylabel("Elevación (m)")
        self.analysis_ax.grid(True, alpha=0.3)
        self.analysis_ax.text(0.5, 0.5, "Ejecute el análisis para ver los resultados", 
                             transform=self.analysis_ax.transAxes, ha='center', va='center',
                             fontsize=12, alpha=0.7)
        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()
    
    def plot_empty_comparison(self):
        """Plotear comparación vacía."""
        self.comp_ax.clear()
        self.comp_ax.set_title("Comparación de Métodos")
        self.comp_ax.set_xlabel("Método")
        self.comp_ax.set_ylabel("Factor de Seguridad")
        self.comp_ax.grid(True, alpha=0.3)
        self.comp_ax.text(0.5, 0.5, "Ejecute ambos análisis para comparar", 
                         transform=self.comp_ax.transAxes, ha='center', va='center',
                         fontsize=12, alpha=0.7)
        self.comp_fig.tight_layout()
        self.comp_canvas.draw()
    
    def plot_empty_convergence(self):
        """Plotear convergencia vacía."""
        self.conv_ax.clear()
        self.conv_ax.set_title("Convergencia del Método Bishop")
        self.conv_ax.set_xlabel("Iteración")
        self.conv_ax.set_ylabel("Factor de Seguridad")
        self.conv_ax.grid(True, alpha=0.3)
        self.conv_ax.text(0.5, 0.5, "Ejecute análisis Bishop para ver convergencia", 
                         transform=self.conv_ax.transAxes, ha='center', va='center',
                         fontsize=12, alpha=0.7)
        self.conv_fig.tight_layout()
        self.conv_canvas.draw()
    
    def update_geometry(self, parameters):
        """Actualizar gráfico de geometría."""
        try:
            # Crear geometría
            altura = parameters['altura']
            angulo_talud = parameters['angulo_talud']
            
            # Calcular longitud base
            longitud_base = altura / math.tan(math.radians(angulo_talud))
            
            # Crear perfil
            perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
            
            # Crear círculo de falla (estimado)
            xc = longitud_base * 0.4
            yc = altura * 1.1
            radio = 1.5 * altura
            circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
            
            # Guardar para uso posterior
            self.current_perfil = perfil
            self.current_circulo = circulo
            
            # Plotear
            self.geom_ax.clear()
            
            # Perfil del talud
            x_perfil = [p.x for p in perfil.puntos]
            y_perfil = [p.y for p in perfil.puntos]
            self.geom_ax.plot(x_perfil, y_perfil, 'k-', linewidth=2, label='Perfil del talud')
            self.geom_ax.fill_between(x_perfil, y_perfil, alpha=0.3, color='brown', label='Suelo')
            
            # Círculo de falla
            theta = np.linspace(0, 2*np.pi, 100)
            x_circulo = circulo.xc + circulo.radio * np.cos(theta)
            y_circulo = circulo.yc + circulo.radio * np.sin(theta)
            self.geom_ax.plot(x_circulo, y_circulo, 'r--', linewidth=2, label='Superficie de falla')
            
            # Configurar gráfico
            self.geom_ax.set_xlabel('Distancia (m)')
            self.geom_ax.set_ylabel('Elevación (m)')
            self.geom_ax.set_title('Geometría del Talud')
            self.geom_ax.legend()
            self.geom_ax.grid(True, alpha=0.3)
            self.geom_ax.set_aspect('equal')
            
            # Actualizar
            self.geom_fig.tight_layout()
            self.geom_canvas.draw()
            
        except Exception as e:
            print(f"Error actualizando geometría: {e}")
            import traceback
            traceback.print_exc()
    
    def update_profile(self, perfil_terreno, estratos=None):
        """Actualizar visualización del perfil del terreno - VERSIÓN PROFESIONAL"""
        if not perfil_terreno:
            return
        
        # Guardar perfil actual
        self.current_perfil = perfil_terreno
        
        # Limpiar gráfico
        self.geom_ax.clear()
        
        # === CONFIGURACIÓN DEL GRÁFICO ===
        self.geom_ax.set_aspect('equal')
        self.geom_ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        self.geom_ax.set_xlabel('Distancia Horizontal (m)', fontsize=12, fontweight='bold')
        self.geom_ax.set_ylabel('Elevación (m)', fontsize=12, fontweight='bold')
        self.geom_ax.set_title('Perfil Geotécnico del Talud', fontsize=14, fontweight='bold')
        
        # === DIBUJAR PERFIL DEL TERRENO ===
        x_perfil = [p[0] for p in perfil_terreno]
        y_perfil = [p[1] for p in perfil_terreno]
        
        # Superficie del talud (línea gruesa negra)
        self.geom_ax.plot(x_perfil, y_perfil, 'k-', linewidth=4, label='Superficie del talud', zorder=3)
        
        # === DIBUJAR ESTRATOS GEOLÓGICOS ===
        if estratos and len(estratos) > 0:
            # Colores para diferentes estratos
            colores_estratos = ['sandybrown', 'tan', 'peru', 'saddlebrown', 'chocolate']
            
            for i, estrato in enumerate(estratos):
                color = colores_estratos[i % len(colores_estratos)]
                
                # Rellenar área del estrato
                y_base = min(y_perfil) - 2 - (i * 3)  # Cada estrato más abajo
                x_fill = x_perfil + [max(x_perfil), min(x_perfil)]
                y_fill = y_perfil + [y_base, y_base]
                
                self.geom_ax.fill(x_fill, y_fill, color=color, alpha=0.7, 
                                edgecolor='black', linewidth=1,
                                label=f'Estrato {i+1}: γ={estrato.peso_especifico:.1f} kN/m³')
        else:
            # Relleno básico del suelo
            y_base = min(y_perfil) - 5
            x_fill = x_perfil + [max(x_perfil), min(x_perfil)]
            y_fill = y_perfil + [y_base, y_base]
            self.geom_ax.fill(x_fill, y_fill, color='saddlebrown', alpha=0.7, 
                            edgecolor='black', linewidth=1, label='Suelo')
        
        # === INFORMACIÓN GEOMÉTRICA ===
        altura_talud = max(y_perfil) - min(y_perfil)
        longitud_base = max(x_perfil) - min(x_perfil)
        
        if altura_talud > 0 and longitud_base > 0:
            angulo_talud = math.degrees(math.atan(altura_talud / longitud_base))
            
            # Caja de información
            info_text = f"Altura: {altura_talud:.1f} m\nBase: {longitud_base:.1f} m\nÁngulo: {angulo_talud:.1f}°"
            self.geom_ax.text(0.02, 0.98, info_text, transform=self.geom_ax.transAxes,
                             fontsize=11, fontweight='bold', va='top', ha='left',
                             bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8, edgecolor='navy'),
                             color='darkblue')
        
        # === INSTRUCCIONES ===
        self.label_instrucciones.configure(text="✅ Perfil configurado → Presione 'Seleccionar Centro' para ubicar círculo")
        
        # === LEYENDA ===
        legend = self.geom_ax.legend(loc='upper right', fontsize=10, 
                                   fancybox=True, shadow=True, framealpha=0.9)
        legend.get_frame().set_facecolor('white')
        
        # === AJUSTAR LÍMITES ===
        margin_x = longitud_base * 0.2
        margin_y = altura_talud * 0.3
        self.geom_ax.set_xlim(min(x_perfil) - margin_x, max(x_perfil) + margin_x)
        self.geom_ax.set_ylim(min(y_perfil) - margin_y, max(y_perfil) + margin_y)
        
        # Actualizar canvas
        self.geom_canvas.draw()
    
    def update_analysis(
        self,
        perfil_terreno=None,
        circulo=None,
        dovelas=None,
        nivel_freatico=None,
        bishop_result=None,
        fellenius_result=None,
    ):
        """Actualizar visualización con resultados del análisis."""

        # Permitir actualización de estado interno desde parámetros opcionales
        if perfil_terreno is not None:
            self.current_perfil = perfil_terreno

        if circulo is not None:
            self.current_circulo = circulo

        if bishop_result is not None:
            self.current_bishop_result = bishop_result

        if fellenius_result is not None:
            self.current_fellenius_result = fellenius_result

        # Nivel freático asociado (si se provee)
        if bishop_result is not None and nivel_freatico is not None:
            bishop_result.nivel_freatico = nivel_freatico

        if not self.current_bishop_result:
            return
        
        # Limpiar gráfico
        self.geom_ax.clear()
        
        # === CONFIGURACIÓN DEL GRÁFICO ===
        self.geom_ax.set_aspect('equal')
        self.geom_ax.grid(True, alpha=0.3)
        self.geom_ax.set_xlabel('Distancia (m)', fontsize=12, fontweight='bold')
        self.geom_ax.set_ylabel('Elevación (m)', fontsize=12, fontweight='bold')
        self.geom_ax.set_title('Análisis de Estabilidad de Talud - Factor de Seguridad', 
                              fontsize=14, fontweight='bold')
        
        # === DIBUJAR PERFIL DEL TERRENO ===
        if self.current_perfil:
            x_perfil = [p[0] for p in self.current_perfil]
            y_perfil = [p[1] for p in self.current_perfil]
            
            # Superficie del talud (línea gruesa)
            self.geom_ax.plot(x_perfil, y_perfil, 'k-', linewidth=3, label='Superficie del talud')
            
            # Rellenar área del talud con color tierra
            x_fill = x_perfil + [max(x_perfil), min(x_perfil)]
            y_fill = y_perfil + [min(y_perfil)-5, min(y_perfil)-5]
            self.geom_ax.fill(x_fill, y_fill, color='saddlebrown', alpha=0.6, label='Suelo')
        
        # === DIBUJAR CÍRCULO DE FALLA ===
        if self.current_circulo:
            theta = np.linspace(0, 2*np.pi, 200)
            x_circulo = self.current_circulo.xc + self.current_circulo.radio * np.cos(theta)
            y_circulo = self.current_circulo.yc + self.current_circulo.radio * np.sin(theta)
            
            # Círculo de falla (azul grueso)
            self.geom_ax.plot(x_circulo, y_circulo, 'b-', linewidth=3, 
                            label=f'Círculo de falla (R={self.current_circulo.radio:.1f}m)')
            
            # Centro del círculo
            self.geom_ax.plot(self.current_circulo.xc, self.current_circulo.yc, 'ro', 
                            markersize=8, label=f'Centro ({self.current_circulo.xc:.1f}, {self.current_circulo.yc:.1f})')
        
        # === DIBUJAR DOVELAS NUMERADAS ===
        if hasattr(self.current_bishop_result, 'dovelas') and self.current_bishop_result.dovelas:
            for i, dovela in enumerate(self.current_bishop_result.dovelas):
                # Color alternante para dovelas
                color = 'lightblue' if i % 2 == 0 else 'lightcyan'
                alpha = 0.7
                
                # Dibujar dovela como rectángulo
                x_center = dovela.x_centro
                y_base = dovela.y_base
                y_top = dovela.y_superficie
                ancho = dovela.ancho_dovela
                
                # Rectángulo de la dovela
                rect_x = [x_center - ancho/2, x_center + ancho/2, 
                         x_center + ancho/2, x_center - ancho/2, x_center - ancho/2]
                rect_y = [y_base, y_base, y_top, y_top, y_base]
                
                self.geom_ax.fill(rect_x, rect_y, color=color, alpha=alpha, 
                                edgecolor='darkblue', linewidth=1)
                
                # Número de la dovela en el centro
                y_medio = (y_base + y_top) / 2
                self.geom_ax.text(x_center, y_medio, str(i+1), 
                                ha='center', va='center', fontweight='bold', 
                                fontsize=10, color='darkblue',
                                bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', alpha=0.8))
                
                # Líneas de división entre dovelas
                if i > 0:
                    self.geom_ax.axvline(x=x_center - ancho/2, color='darkblue', 
                                       linestyle='--', alpha=0.5, linewidth=1)
        
        # === INFORMACIÓN DEL FACTOR DE SEGURIDAD ===
        fs_text = f"FS Crítico = {self.current_bishop_result.factor_seguridad:.3f}"
        if self.current_bishop_result.factor_seguridad < 1.0:
            fs_color = 'red'
            fs_status = "INESTABLE"
        elif self.current_bishop_result.factor_seguridad < 1.5:
            fs_color = 'orange'
            fs_status = "MARGINALMENTE ESTABLE"
        else:
            fs_color = 'green'
            fs_status = "ESTABLE"
        
        # Caja de información prominente
        info_text = f"{fs_text}\nEstado: {fs_status}\nDovelas: {len(self.current_bishop_result.dovelas)}"
        self.geom_ax.text(0.02, 0.98, info_text, transform=self.geom_ax.transAxes,
                         fontsize=12, fontweight='bold', va='top', ha='left',
                         bbox=dict(boxstyle="round,pad=0.5", facecolor=fs_color, alpha=0.8, edgecolor='black'),
                         color='white')
        
        # === NIVEL FREÁTICO (si aplica) ===
        if hasattr(self.current_bishop_result, 'nivel_freatico') and self.current_bishop_result.nivel_freatico:
            y_freatico = self.current_bishop_result.nivel_freatico
            x_limits = self.geom_ax.get_xlim()
            self.geom_ax.axhline(y=y_freatico, color='cyan', linestyle='--', 
                               linewidth=2, alpha=0.7, label='Nivel freático')
        
        # === LEYENDA PROFESIONAL ===
        legend = self.geom_ax.legend(loc='upper right', fontsize=10, 
                                   fancybox=True, shadow=True, framealpha=0.9)
        legend.get_frame().set_facecolor('white')
        
        # === AJUSTAR LÍMITES Y DISEÑO ===
        self.geom_ax.margins(0.1)
        
        # Actualizar canvas
        self.geom_canvas.draw()
    
    def update_comparison(self):
        """Actualizar gráfico de comparación."""
        try:
            if not self.current_bishop_result and not self.current_fellenius_result:
                return
            
            self.comp_ax.clear()
            
            methods = []
            fs_values = []
            colors = []
            
            if self.current_bishop_result:
                methods.append('Bishop')
                fs_values.append(self.current_bishop_result.factor_seguridad)
                colors.append('blue')
            
            if self.current_fellenius_result:
                methods.append('Fellenius')
                fs_values.append(self.current_fellenius_result.factor_seguridad)
                colors.append('red')
            
            if methods:
                bars = self.comp_ax.bar(methods, fs_values, color=colors, alpha=0.7)
                
                # Añadir valores en las barras
                for bar, value in zip(bars, fs_values):
                    height = bar.get_height()
                    self.comp_ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                                     f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
                
                # Líneas de referencia
                self.comp_ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Fs = 1.0 (Límite)')
                self.comp_ax.axhline(y=1.3, color='orange', linestyle='--', alpha=0.5, label='Fs = 1.3 (Mínimo)')
                self.comp_ax.axhline(y=1.5, color='green', linestyle='--', alpha=0.5, label='Fs = 1.5 (Seguro)')
                
                self.comp_ax.set_title("Comparación de Métodos")
                self.comp_ax.set_ylabel("Factor de Seguridad")
                self.comp_ax.grid(True, alpha=0.3)
                self.comp_ax.legend()
                
                # Ajustar límites
                max_fs = max(fs_values)
                self.comp_ax.set_ylim(0, max_fs * 1.2)
            
            self.comp_fig.tight_layout()
            self.comp_canvas.draw()
            
        except Exception as e:
            self.comp_ax.clear()
            self.comp_ax.text(0.5, 0.5, f"Error: {str(e)}", 
                             transform=self.comp_ax.transAxes, ha='center', va='center',
                             fontsize=12, color='red')
            self.comp_canvas.draw()
    
    def update_convergence(self, convergence_history=None):
        """Actualizar gráfico de convergencia."""
        try:
            if not convergence_history:
                if self.current_bishop_result and hasattr(self.current_bishop_result, 'historial_convergencia'):
                    convergence_history = self.current_bishop_result.historial_convergencia
                else:
                    return
            
            self.conv_ax.clear()
            
            iterations = list(range(1, len(convergence_history) + 1))
            self.conv_ax.plot(iterations, convergence_history, 'bo-', linewidth=2, markersize=6)
            
            # Línea final
            final_fs = convergence_history[-1]
            self.conv_ax.axhline(y=final_fs, color='red', linestyle='--', alpha=0.7, 
                               label=f'Fs final = {final_fs:.3f}')
            
            self.conv_ax.set_title("Convergencia del Método Bishop")
            self.conv_ax.set_xlabel("Iteración")
            self.conv_ax.set_ylabel("Factor de Seguridad")
            self.conv_ax.grid(True, alpha=0.3)
            self.conv_ax.legend()
            
            # Añadir valores en los puntos
            for i, fs in enumerate(convergence_history):
                self.conv_ax.annotate(f'{fs:.3f}', (i+1, fs), textcoords="offset points", 
                                    xytext=(0,10), ha='center', fontsize=9)
            
            self.conv_fig.tight_layout()
            self.conv_canvas.draw()
            
        except Exception as e:
            self.conv_ax.clear()
            self.conv_ax.text(0.5, 0.5, f"Error: {str(e)}", 
                             transform=self.conv_ax.transAxes, ha='center', va='center',
                             fontsize=12, color='red')
            self.conv_canvas.draw()
    
    def clear_all_plots(self):
        """Limpiar todos los gráficos."""
        self.plot_empty_geometry()
        self.plot_empty_analysis()
        self.plot_empty_comparison()
        self.plot_empty_convergence()
        
        # Limpiar datos guardados
        self.current_perfil = None
        self.current_circulo = None
        self.current_bishop_result = None
        self.current_fellenius_result = None
    
    def export_plots(self, base_filename="analisis_talud"):
        """Exportar todos los gráficos."""
        try:
            # Geometría
            self.geom_fig.savefig(f"{base_filename}_geometria.png", dpi=300, bbox_inches='tight')
            
            # Análisis
            self.analysis_fig.savefig(f"{base_filename}_analisis.png", dpi=300, bbox_inches='tight')
            
            # Comparación
            self.comp_fig.savefig(f"{base_filename}_comparacion.png", dpi=300, bbox_inches='tight')
            
            # Convergencia
            self.conv_fig.savefig(f"{base_filename}_convergencia.png", dpi=300, bbox_inches='tight')
            
            return True
        except Exception as e:
            print(f"Error exportando gráficos: {e}")
            return False

    def update_plots(self, bishop_result=None, fellenius_result=None, parameters=None):
        """Actualizar todos los gráficos con nuevos resultados."""
        try:
            # Guardar resultados
            if bishop_result:
                self.current_bishop_result = bishop_result
            if fellenius_result:
                self.current_fellenius_result = fellenius_result
            
            # Actualizar geometría si hay parámetros
            if parameters:
                self.update_geometry(parameters)
            
            # Actualizar análisis
            self.update_analysis(bishop_result, fellenius_result)
            
            # Actualizar comparación
            self.update_comparison()
            
            # Actualizar convergencia si hay datos Bishop
            if bishop_result and hasattr(bishop_result, 'historial_convergencia'):
                self.update_convergence(bishop_result.historial_convergencia)
            
        except Exception as e:
            print(f"Error actualizando gráficos: {e}")
    
    def update_parametric_plot(self, parametric_data):
        """Actualizar gráfico con datos de análisis paramétrico."""
        try:
            # Cambiar a tab de comparación
            self.notebook.set("Comparación")
            
            self.comp_ax.clear()
            
            parameter = parametric_data['parameter']
            param_range = parametric_data['range']
            bishop_results = parametric_data['bishop_results']
            fellenius_results = parametric_data['fellenius_results']
            
            # Extraer factores de seguridad
            bishop_fs = [r.factor_seguridad for r in bishop_results]
            fellenius_fs = [r.factor_seguridad for r in fellenius_results]
            
            # Plotear líneas
            self.comp_ax.plot(param_range, bishop_fs, 'b-o', label='Bishop', linewidth=2, markersize=4)
            self.comp_ax.plot(param_range, fellenius_fs, 'r-s', label='Fellenius', linewidth=2, markersize=4)
            
            # Líneas de referencia
            self.comp_ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Fs = 1.0 (Límite)')
            self.comp_ax.axhline(y=1.3, color='orange', linestyle='--', alpha=0.5, label='Fs = 1.3 (Mínimo)')
            self.comp_ax.axhline(y=1.5, color='green', linestyle='--', alpha=0.5, label='Fs = 1.5 (Seguro)')
            
            # Configurar gráfico
            self.comp_ax.set_title(f"Análisis Paramétrico - {parameter}")
            self.comp_ax.set_xlabel(parameter)
            self.comp_ax.set_ylabel("Factor de Seguridad")
            self.comp_ax.grid(True, alpha=0.3)
            self.comp_ax.legend()
            
            self.comp_fig.tight_layout()
            self.comp_canvas.draw()
            
        except Exception as e:
            print(f"Error en análisis paramétrico: {e}")
            self.comp_ax.clear()
            self.comp_ax.text(0.5, 0.5, f"Error: {str(e)}", 
                             transform=self.comp_ax.transAxes, ha='center', va='center',
                             fontsize=12, color='red')
            self.comp_canvas.draw()

    def on_click_geometry(self, event):
        """Manejar clics en el gráfico de geometría para seleccionar centro del círculo"""
        if event.inaxes != self.geom_ax:
            return
            
        if event.button == 1 and self.modo_seleccion:  # Botón izquierdo en modo selección
            # Obtener coordenadas del clic
            x, y = event.xdata, event.ydata
            
            if x is None or y is None:
                return
                
            # Guardar centro seleccionado
            self.centro_seleccionado = (x, y)
            
            # Mostrar punto seleccionado en el gráfico
            self.mostrar_centro_seleccionado(x, y)
            
            # Actualizar campos en la GUI principal
            self.actualizar_campos_centro(x, y)
            
            # Mostrar mensaje de confirmación
            self.label_instrucciones.configure(text=f"Centro seleccionado: ({x:.2f}, {y:.2f})")
            
            # Desactivar modo selección
            self.toggle_modo_seleccion()
    
    def mostrar_centro_seleccionado(self, x, y):
        """Mostrar visualmente el centro seleccionado en el gráfico"""
        # Limpiar puntos anteriores
        if hasattr(self, 'punto_centro'):
            self.punto_centro.remove()
        
        # Dibujar nuevo punto
        self.punto_centro = self.geom_ax.plot(x, y, 'ro', markersize=10, 
                                            label=f'Centro ({x:.1f}, {y:.1f})', 
                                            markeredgecolor='white', markeredgewidth=2)[0]
        
        # Actualizar leyenda si existe
        if self.geom_ax.get_legend():
            self.geom_ax.legend()
        else:
            self.geom_ax.legend(loc='upper right')
            
        self.geom_canvas.draw()
    
    def actualizar_campos_centro(self, x, y):
        """Actualizar los campos de Centro X, Centro Y y Radio en la GUI principal"""
        try:
            # Buscar la app principal y actualizar campos
            if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'config_panel'):
                config_panel = self.parent.parent.config_panel
                
                # Actualizar centro X e Y
                if hasattr(config_panel, 'centro_x_entry') and hasattr(config_panel, 'centro_y_entry'):
                    config_panel.centro_x_entry.delete(0, 'end')
                    config_panel.centro_x_entry.insert(0, f"{x:.2f}")
                    
                    config_panel.centro_y_entry.delete(0, 'end')
                    config_panel.centro_y_entry.insert(0, f"{y:.2f}")
                
                # Actualizar radio si existe el campo
                if hasattr(config_panel, 'radio_entry'):
                    config_panel.radio_entry.delete(0, 'end')
                    config_panel.radio_entry.insert(0, f"{self.radio_actual:.2f}")
                    
                print(f"✅ Campos actualizados: Centro X={x:.2f}, Centro Y={y:.2f}, Radio={self.radio_actual:.2f}")
        except Exception as e:
            print(f"Error actualizando campos: {e}")
            
        # Limpiar círculo preview
        if hasattr(self, 'circulo_preview') and self.circulo_preview:
            self.circulo_preview.remove()
            self.circulo_preview = None
    
    def toggle_modo_seleccion(self):
        self.modo_seleccion = not self.modo_seleccion
        if self.modo_seleccion:
            self.btn_seleccionar_centro.configure(text="🎯 ACTIVO - Mueva mouse y haga clic", fg_color="blue")
            self.label_instrucciones.configure(text="👆 Mueva el mouse para ver preview → Clic para confirmar centro")
        else:
            self.btn_seleccionar_centro.configure(text="📍 Seleccionar Centro", fg_color="green")
            if not self.centro_seleccionado:
                self.label_instrucciones.configure(text="1️⃣ Configure geometría → 2️⃣ Seleccione centro → 3️⃣ Analice")
            
            # Limpiar preview al desactivar
            if hasattr(self, 'circulo_preview') and self.circulo_preview:
                self.circulo_preview.remove()
                self.circulo_preview = None
                self.geom_canvas.draw()
    
    def on_mouse_move_geometry(self, event):
        """Manejar movimiento del mouse en el gráfico de geometría"""
        if event.inaxes != self.geom_ax:
            return
        
        # Obtener coordenadas del mouse
        x, y = event.xdata, event.ydata
        
        if x is None or y is None:
            return
        
        # Mostrar preview del círculo
        if self.modo_seleccion:
            self.mostrar_circulo_preview(x, y)
    
    def mostrar_circulo_preview(self, x, y):
        """Mostrar preview del círculo en el gráfico"""
        try:
            # Limpiar círculo anterior
            if hasattr(self, 'circulo_preview') and self.circulo_preview:
                self.circulo_preview.remove()
            
            # Dibujar nuevo círculo
            theta = np.linspace(0, 2*np.pi, 100)
            x_circulo = x + self.radio_actual * np.cos(theta)
            y_circulo = y + self.radio_actual * np.sin(theta)
            
            self.circulo_preview = self.geom_ax.plot(x_circulo, y_circulo, 'g--', 
                                                   linewidth=2, alpha=0.7, 
                                                   label=f'Preview R={self.radio_actual:.1f}')[0]
            
            # Marcar centro
            if hasattr(self, 'centro_preview'):
                self.centro_preview.remove()
            self.centro_preview = self.geom_ax.plot(x, y, 'go', markersize=8, alpha=0.7)[0]
            
            # Actualizar sin redibujar todo (más eficiente)
            self.geom_canvas.draw_idle()
            
        except Exception as e:
            # Si hay error, no bloquear la interfaz
            pass
    
    def on_radio_change(self, event):
        try:
            self.radio_actual = float(self.radio_entry.get())
            self.radio_slider.set(self.radio_actual)
        except ValueError:
            pass
    
    def on_radio_slider_change(self, value):
        self.radio_actual = float(value)
        self.radio_entry.delete(0, 'end')
        self.radio_entry.insert(0, f"{self.radio_actual:.1f}")

    def show_slope_only(self, perfil_terreno, parameters):
        """Mostrar solo la geometría del talud sin círculo de falla."""
        try:
            # Limpiar el gráfico de geometría
            self.geom_ax.clear()
            
            # Extraer coordenadas del perfil
            if hasattr(perfil_terreno[0], 'x'):
                # Si son objetos Punto
                x_coords = [p.x for p in perfil_terreno]
                y_coords = [p.y for p in perfil_terreno]
            else:
                # Si son tuplas (x, y)
                x_coords = [p[0] for p in perfil_terreno]
                y_coords = [p[1] for p in perfil_terreno]
            
            # Dibujar el perfil del talud
            self.geom_ax.plot(x_coords, y_coords, 'b-', linewidth=3, label='Perfil del talud')
            self.geom_ax.fill_between(x_coords, y_coords, alpha=0.3, color='brown', label='Suelo')
            
            # Configurar el gráfico
            self.geom_ax.set_xlabel('Distancia (m)')
            self.geom_ax.set_ylabel('Altura (m)')
            self.geom_ax.set_title(f'Geometría del Talud - Altura: {parameters["altura"]:.1f}m, Ángulo: {parameters["angulo_talud"]:.1f}°')
            self.geom_ax.grid(True, alpha=0.3)
            self.geom_ax.legend()
            self.geom_ax.set_aspect('equal')
            
            # Ajustar límites para mejor visualización
            margin_x = (max(x_coords) - min(x_coords)) * 0.1
            margin_y = (max(y_coords) - min(y_coords)) * 0.1
            self.geom_ax.set_xlim(min(x_coords) - margin_x, max(x_coords) + margin_x)
            self.geom_ax.set_ylim(min(y_coords) - margin_y, max(y_coords) + margin_y)
            
            # Actualizar canvas
            self.geom_fig.tight_layout()
            self.geom_canvas.draw()
            
            # Cambiar al tab de geometría
            self.notebook.set("Geometría")
            
        except Exception as e:
            print(f"Error en show_slope_only: {e}")
            import traceback
            traceback.print_exc()
    
    def update_geometry(self, parameters):
        """Actualizar gráfico de geometría."""
        try:
            # Crear geometría
            altura = parameters['altura']
            angulo_talud = parameters['angulo_talud']
            
            # Calcular longitud base
            longitud_base = altura / math.tan(math.radians(angulo_talud))
            
            # Crear perfil
            perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
            
            # Crear círculo de falla (estimado)
            xc = longitud_base * 0.4
            yc = altura * 1.1
            radio = 1.5 * altura
            circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
            
            # Guardar para uso posterior
            self.current_perfil = perfil
            self.current_circulo = circulo
            
            # Plotear
            self.geom_ax.clear()
            
            # Perfil del talud
            x_perfil = [p.x for p in perfil.puntos]
            y_perfil = [p.y for p in perfil.puntos]
            self.geom_ax.plot(x_perfil, y_perfil, 'k-', linewidth=2, label='Perfil del talud')
            self.geom_ax.fill_between(x_perfil, y_perfil, alpha=0.3, color='brown', label='Suelo')
            
            # Círculo de falla
            theta = np.linspace(0, 2*np.pi, 100)
            x_circulo = circulo.xc + circulo.radio * np.cos(theta)
            y_circulo = circulo.yc + circulo.radio * np.sin(theta)
            self.geom_ax.plot(x_circulo, y_circulo, 'r--', linewidth=2, label='Superficie de falla')
            
            # Configurar gráfico
            self.geom_ax.set_xlabel('Distancia (m)')
            self.geom_ax.set_ylabel('Elevación (m)')
            self.geom_ax.set_title('Geometría del Talud')
            self.geom_ax.legend()
            self.geom_ax.grid(True, alpha=0.3)
            self.geom_ax.set_aspect('equal')
            
            # Actualizar
            self.geom_fig.tight_layout()
            self.geom_canvas.draw()
            
        except Exception as e:
            print(f"Error actualizando geometría: {e}")
            import traceback
            traceback.print_exc()
