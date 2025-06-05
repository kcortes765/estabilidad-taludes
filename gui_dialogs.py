"""
Diálogos y funciones auxiliares para la interfaz gráfica.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import os


class ParametricDialog(ctk.CTkToplevel):
    """Diálogo para configurar análisis paramétrico."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Análisis Paramétrico - Estudio de Sensibilidad")
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar interfaz del diálogo."""
        # Título y descripción
        title_label = ctk.CTkLabel(self, text="ANÁLISIS PARAMÉTRICO", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=10)
        
        desc_text = """
El análisis paramétrico varía un parámetro en un rango específico
y muestra cómo cambia el factor de seguridad. Útil para:

• Estudios de sensibilidad
• Optimización de diseño  
• Análisis de riesgo
• Determinación de parámetros críticos
        """
        
        desc_label = ctk.CTkLabel(self, text=desc_text, justify="left")
        desc_label.pack(pady=10, padx=20)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Selección de parámetro
        param_frame = ctk.CTkFrame(main_frame)
        param_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(param_frame, text="Parámetro a variar:", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.parameter_var = tk.StringVar(value="cohesion")
        self.parameter_menu = ctk.CTkOptionMenu(
            param_frame,
            values=["cohesion", "phi_grados", "gamma", "altura", "angulo_talud"],
            variable=self.parameter_var,
            command=self.on_parameter_change
        )
        self.parameter_menu.pack(pady=5)
        
        # Descripción del parámetro seleccionado
        self.param_desc_label = ctk.CTkLabel(param_frame, text="", 
                                           font=ctk.CTkFont(size=12))
        self.param_desc_label.pack(pady=5)
        
        # Rango de valores
        range_frame = ctk.CTkFrame(main_frame)
        range_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(range_frame, text="Rango de análisis:", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        # Valor mínimo
        min_frame = ctk.CTkFrame(range_frame)
        min_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(min_frame, text="Valor mínimo:").pack(side="left", padx=5)
        self.min_var = tk.DoubleVar(value=10.0)
        self.min_entry = ctk.CTkEntry(min_frame, textvariable=self.min_var, width=100)
        self.min_entry.pack(side="right", padx=5)
        
        # Valor máximo
        max_frame = ctk.CTkFrame(range_frame)
        max_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(max_frame, text="Valor máximo:").pack(side="left", padx=5)
        self.max_var = tk.DoubleVar(value=50.0)
        self.max_entry = ctk.CTkEntry(max_frame, textvariable=self.max_var, width=100)
        self.max_entry.pack(side="right", padx=5)
        
        # Número de pasos
        steps_frame = ctk.CTkFrame(range_frame)
        steps_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(steps_frame, text="Número de pasos:").pack(side="left", padx=5)
        self.steps_var = tk.IntVar(value=10)
        self.steps_entry = ctk.CTkEntry(steps_frame, textvariable=self.steps_var, width=100)
        self.steps_entry.pack(side="right", padx=5)
        
        # Botones
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancelar", 
                                  command=self.on_cancel)
        cancel_btn.pack(side="left", padx=10, pady=10)
        
        ok_btn = ctk.CTkButton(button_frame, text="Ejecutar Análisis", 
                              command=self.on_ok)
        ok_btn.pack(side="right", padx=10, pady=10)
        
        # Actualizar descripción inicial
        self.on_parameter_change("cohesion")
    
    def on_parameter_change(self, value):
        """Actualizar descripción y rangos sugeridos según parámetro."""
        descriptions = {
            "cohesion": "Cohesión del suelo (kPa)\nRango típico: 0-100 kPa",
            "phi_grados": "Ángulo de fricción (grados)\nRango típico: 15-45°",
            "gamma": "Peso unitario (kN/m³)\nRango típico: 16-22 kN/m³",
            "altura": "Altura del talud (m)\nRango típico: 5-25 m",
            "angulo_talud": "Ángulo del talud (grados)\nRango típico: 30-60°"
        }
        
        suggested_ranges = {
            "cohesion": (0, 50, 10),
            "phi_grados": (15, 35, 8),
            "gamma": (16, 22, 6),
            "altura": (5, 20, 8),
            "angulo_talud": (30, 60, 10)
        }
        
        # Actualizar descripción
        self.param_desc_label.configure(text=descriptions.get(value, ""))
        
        # Actualizar rangos sugeridos
        if value in suggested_ranges:
            min_val, max_val, steps = suggested_ranges[value]
            self.min_var.set(min_val)
            self.max_var.set(max_val)
            self.steps_var.set(steps)
    
    def on_ok(self):
        """Confirmar configuración."""
        try:
            param = self.parameter_var.get()
            min_val = self.min_var.get()
            max_val = self.max_var.get()
            steps = self.steps_var.get()
            
            # Validaciones
            if min_val >= max_val:
                messagebox.showerror("Error", "El valor mínimo debe ser menor que el máximo")
                return
            
            if steps < 3:
                messagebox.showerror("Error", "Debe haber al menos 3 pasos")
                return
            
            if steps > 20:
                messagebox.showerror("Error", "Máximo 20 pasos permitidos")
                return
            
            # Crear rango
            param_range = np.linspace(min_val, max_val, steps)
            
            # Configurar resultado
            self.result = {
                'parameter': param,
                'range': param_range
            }
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en configuración: {str(e)}")
    
    def on_cancel(self):
        """Cancelar diálogo."""
        self.result = None
        self.destroy()


class AppUtils:
    """Utilidades para la aplicación."""
    
    @staticmethod
    def export_results(app_instance):
        """Exportar resultados y gráficos."""
        if not app_instance.current_bishop_result and not app_instance.current_fellenius_result:
            messagebox.showwarning("Sin resultados", "No hay resultados para exportar")
            return
        
        # Seleccionar directorio
        directory = filedialog.askdirectory(title="Seleccionar directorio para exportar")
        if not directory:
            return
        
        try:
            # Exportar gráficos
            base_filename = os.path.join(directory, "analisis_talud")
            success = app_instance.plotting_panel.export_plots(base_filename)
            
            if success:
                # Exportar reporte de texto
                AppUtils._export_text_report(app_instance, base_filename + "_reporte.txt")
                messagebox.showinfo("Exportación exitosa", 
                                  f"Resultados exportados a:\n{directory}")
            else:
                messagebox.showerror("Error", "Error al exportar gráficos")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la exportación:\n{str(e)}")
    
    @staticmethod
    def _export_text_report(app_instance, filename):
        """Exportar reporte de texto."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE ANÁLISIS DE ESTABILIDAD DE TALUDES\n")
            f.write("=" * 50 + "\n\n")
            
            # Parámetros
            params = app_instance.parameter_panel.get_parameters()
            f.write("PARÁMETROS DEL ANÁLISIS:\n")
            f.write(f"Altura del talud: {params['altura']:.1f} m\n")
            f.write(f"Ángulo del talud: {params['angulo_talud']:.1f}°\n")
            f.write(f"Cohesión: {params['cohesion']:.1f} kPa\n")
            f.write(f"Ángulo de fricción: {params['phi_grados']:.1f}°\n")
            f.write(f"Peso específico: {params['gamma']:.1f} kN/m³\n")
            f.write(f"Número de dovelas: {params['num_dovelas']}\n")
            if params['con_agua']:
                f.write(f"Nivel freático: {params['altura_nf']:.1f} m\n")
            f.write("\n")
            
            # Resultados Bishop
            if app_instance.current_bishop_result:
                f.write("RESULTADOS - MÉTODO DE BISHOP:\n")
                f.write(f"Factor de Seguridad: {app_instance.current_bishop_result.factor_seguridad:.3f}\n")
                f.write(f"Iteraciones: {app_instance.current_bishop_result.iteraciones}\n")
                f.write(f"Convergió: {'Sí' if app_instance.current_bishop_result.convergio else 'No'}\n")
                f.write("\n")
            
            # Resultados Fellenius
            if app_instance.current_fellenius_result:
                f.write("RESULTADOS - MÉTODO DE FELLENIUS:\n")
                f.write(f"Factor de Seguridad: {app_instance.current_fellenius_result.factor_seguridad:.3f}\n")
                f.write(f"Momento Resistente: {app_instance.current_fellenius_result.momento_resistente:.1f} kN·m\n")
                f.write(f"Momento Actuante: {app_instance.current_fellenius_result.momento_actuante:.1f} kN·m\n")
                f.write("\n")
            
            # Interpretación
            if app_instance.current_bishop_result:
                fs = app_instance.current_bishop_result.factor_seguridad
                f.write("INTERPRETACIÓN:\n")
                if fs >= 2.0:
                    f.write("Estado: MUY SEGURO\n")
                    f.write("Recomendación: Talud muy estable, proceder con confianza\n")
                elif fs >= 1.5:
                    f.write("Estado: SEGURO\n")
                    f.write("Recomendación: Talud estable, condiciones aceptables\n")
                elif fs >= 1.3:
                    f.write("Estado: ACEPTABLE\n")
                    f.write("Recomendación: Talud marginalmente estable, monitorear\n")
                else:
                    f.write("Estado: MARGINAL/INESTABLE\n")
                    f.write("Recomendación: Considerar medidas de estabilización\n")
    
    @staticmethod
    def clear_results(app_instance):
        """Limpiar todos los resultados."""
        app_instance.current_bishop_result = None
        app_instance.current_fellenius_result = None
        
        # Limpiar paneles
        app_instance.results_panel.update_results()
        app_instance.plotting_panel.clear_all_plots()
        
        app_instance.update_status("Resultados limpiados")
    
    @staticmethod
    def show_file_menu():
        """Mostrar menú de archivo."""
        messagebox.showinfo("Menú Archivo", 
                          "Funciones de archivo:\n"
                          "• Exportar resultados\n"
                          "• Guardar configuración\n"
                          "• Cargar proyecto\n"
                          "• Generar reporte PDF")
    
    @staticmethod
    def show_analysis_menu():
        """Mostrar menú de análisis."""
        messagebox.showinfo("Menú Análisis", 
                          "Tipos de análisis:\n"
                          "• Análisis rápido\n"
                          "• Análisis paramétrico\n"
                          "• Análisis con agua\n"
                          "• Búsqueda de círculo crítico\n"
                          "• Análisis de sensibilidad")
    
    @staticmethod
    def show_tools_menu():
        """Mostrar menú de herramientas."""
        messagebox.showinfo("Menú Herramientas", 
                          "Herramientas disponibles:\n"
                          "• Calculadora geotécnica\n"
                          "• Conversor de unidades\n"
                          "• Generador de perfiles\n"
                          "• Análisis de dovelas\n"
                          "• Comparador de métodos")
    
    @staticmethod
    def show_help():
        """Mostrar ayuda del sistema."""
        help_text = """
ANÁLISIS DE ESTABILIDAD DE TALUDES

=== TIPOS DE ANÁLISIS ===

1. ANÁLISIS NORMAL:
   • Calcula el factor de seguridad para parámetros específicos
   • Usa métodos Bishop Modificado y Fellenius
   • Resultado: Factor de seguridad único
   • Tiempo: Rápido (segundos)

2. ANÁLISIS PARAMÉTRICO:
   • Varía un parámetro en un rango definido
   • Genera gráfico de sensibilidad
   • Muestra cómo cambia Fs con el parámetro
   • Útil para análisis de sensibilidad y optimización

=== MÉTODOS DE CÁLCULO ===

• BISHOP MODIFICADO:
  - Método iterativo más preciso
  - Considera fuerzas entre dovelas
  - Generalmente menos conservador

• FELLENIUS:
  - Método directo más simple
  - Asume fuerzas entre dovelas = 0
  - Más conservador (Fs menores)

=== CASOS DE EJEMPLO ===

1. Talud Estable: Fs > 1.5 (seguro)
2. Talud Marginal: 1.2 < Fs < 1.4 (cuidado)
3. Talud con Agua: Fs ≈ 1.0-1.2 (crítico)
4. Talud Inestable: Fs < 1.0 (peligroso)
5. Caso Problemático: Prueba límites del software

=== INTERPRETACIÓN ===

• Fs > 1.5: ESTABLE (verde)
• 1.3 < Fs < 1.5: ACEPTABLE (naranja)
• 1.0 < Fs < 1.3: MARGINAL (amarillo)
• Fs < 1.0: INESTABLE (rojo)

=== CONTROLES ===

• Use sliders para cambios rápidos
• Escriba valores exactos en campos
• Seleccione casos de ejemplo predefinidos
• Active nivel freático para análisis con agua
        """
        
        # Crear ventana de ayuda
        help_window = ctk.CTkToplevel()
        help_window.title("Ayuda - Análisis de Estabilidad")
        help_window.geometry("600x700")
        help_window.transient()
        help_window.grab_set()
        
        # Texto de ayuda con scroll
        text_frame = ctk.CTkFrame(help_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = ctk.CTkTextbox(text_frame, width=550, height=600)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.configure(state="disabled")
        
        # Botón cerrar
        close_btn = ctk.CTkButton(help_window, text="Cerrar", 
                                 command=help_window.destroy)
        close_btn.pack(pady=10)


# Agregar métodos de utilidad a la clase principal
def add_utility_methods(app_class):
    """Agregar métodos de utilidad a la clase de aplicación."""
    
    def export_results(self):
        """Exportar resultados y gráficos."""
        AppUtils.export_results(self)
    
    def clear_results(self):
        """Limpiar todos los resultados."""
        AppUtils.clear_results(self)
    
    def show_file_menu(self):
        """Mostrar menú de archivo."""
        AppUtils.show_file_menu()
    
    def show_analysis_menu(self):
        """Mostrar menú de análisis."""
        AppUtils.show_analysis_menu()
    
    def show_tools_menu(self):
        """Mostrar menú de herramientas."""
        AppUtils.show_tools_menu()
    
    def show_help(self):
        """Mostrar ayuda."""
        AppUtils.show_help()
    
    # Agregar métodos a la clase
    app_class.export_results = export_results
    app_class.clear_results = clear_results
    app_class.show_file_menu = show_file_menu
    app_class.show_analysis_menu = show_analysis_menu
    app_class.show_tools_menu = show_tools_menu
    app_class.show_help = show_help


class ManualCircleDialog(ctk.CTkToplevel):
    """Diálogo para selección manual del círculo de falla."""
    
    def __init__(self, parent, params):
        super().__init__(parent)
        self.title("Selección Manual del Círculo de Falla")
        self.geometry("900x700")
        self.transient(parent)
        self.grab_set()
        
        self.params = params
        self.result = None
        self.selected_center = None
        self.selected_radius = None
        
        self.setup_ui()
        self.create_slope_plot()
        
    def setup_ui(self):
        """Configurar la interfaz del diálogo."""
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para el gráfico
        plot_frame = ctk.CTkFrame(main_frame)
        plot_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para controles
        control_frame = ctk.CTkFrame(main_frame, width=200)
        control_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        control_frame.grid_propagate(False)
        
        # Título de controles
        title_label = ctk.CTkLabel(control_frame, text="SELECCIÓN MANUAL", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=10)
        
        # Instrucciones
        instructions = """
1. Haga clic en el gráfico para seleccionar el centro del círculo

2. Use el control deslizante para ajustar el radio

3. El círculo se actualizará en tiempo real

4. Haga clic en "Aplicar" para confirmar
        """
        
        instructions_label = ctk.CTkLabel(control_frame, text=instructions, 
                                        justify="left", font=ctk.CTkFont(size=11))
        instructions_label.pack(pady=10, padx=10)
        
        # Control de radio
        radio_frame = ctk.CTkFrame(control_frame)
        radio_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(radio_frame, text="Radio (m):", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.radio_var = tk.DoubleVar(value=self.params.get('radio', 15.0))
        self.radio_entry = ctk.CTkEntry(radio_frame, textvariable=self.radio_var, width=100)
        self.radio_entry.pack(pady=2)
        
        self.radio_slider = ctk.CTkSlider(radio_frame, from_=5, to=50, 
                                        variable=self.radio_var,
                                        command=self.on_radio_change)
        self.radio_slider.pack(fill="x", pady=5)
        
        # Información del círculo actual
        info_frame = ctk.CTkFrame(control_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(info_frame, text="CÍRCULO ACTUAL:", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.center_label = ctk.CTkLabel(info_frame, text="Centro: No seleccionado")
        self.center_label.pack(pady=2)
        
        self.radius_label = ctk.CTkLabel(info_frame, text=f"Radio: {self.radio_var.get():.1f} m")
        self.radius_label.pack(pady=2)
        
        # Botones
        button_frame = ctk.CTkFrame(control_frame)
        button_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        
        self.apply_btn = ctk.CTkButton(button_frame, text="✓ Aplicar", 
                                     command=self.on_apply, state="disabled",
                                     fg_color="green", hover_color="darkgreen")
        self.apply_btn.pack(fill="x", pady=2)
        
        cancel_btn = ctk.CTkButton(button_frame, text="✗ Cancelar", 
                                 command=self.on_cancel,
                                 fg_color="red", hover_color="darkred")
        cancel_btn.pack(fill="x", pady=2)
        
        # Configurar matplotlib en el frame de plot
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Conectar evento de clic
        self.canvas.mpl_connect('button_press_event', self.on_plot_click)
        
    def create_slope_plot(self):
        """Crear el gráfico del talud."""
        from data.models import generar_perfil_simple
        from visualization.circle_plots import plot_slope_profile
        
        # Generar perfil del talud
        perfil = generar_perfil_simple(
            altura=self.params['altura'],
            angulo_grados=self.params['angulo_talud'],
        )
        
        # Limpiar el gráfico
        self.ax.clear()
        
        # Dibujar el perfil del talud
        x_coords = [p[0] for p in perfil]
        y_coords = [p[1] for p in perfil]
        
        self.ax.plot(x_coords, y_coords, 'b-', linewidth=2, label='Perfil del talud')
        self.ax.fill_between(x_coords, y_coords, alpha=0.3, color='brown')
        
        # Configurar el gráfico
        self.ax.set_xlabel('Distancia (m)')
        self.ax.set_ylabel('Altura (m)')
        self.ax.set_title('Haga clic para seleccionar el centro del círculo')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_aspect('equal')
        self.ax.legend()
        
        # Guardar el perfil para uso posterior
        self.perfil = perfil
        
        self.canvas.draw()
        
    def on_plot_click(self, event):
        """Manejar clic en el gráfico."""
        if event.inaxes != self.ax:
            return
            
        # Obtener coordenadas del clic
        self.selected_center = (event.xdata, event.ydata)
        
        # Actualizar información
        self.center_label.configure(text=f"Centro: ({event.xdata:.1f}, {event.ydata:.1f})")
        
        # Habilitar botón aplicar
        self.apply_btn.configure(state="normal")
        
        # Dibujar círculo
        self.update_circle_display()
        
    def on_radio_change(self, value=None):
        """Manejar cambio en el radio."""
        self.radius_label.configure(text=f"Radio: {self.radio_var.get():.1f} m")
        if self.selected_center:
            self.update_circle_display()
            
    def update_circle_display(self):
        """Actualizar la visualización del círculo."""
        if not self.selected_center:
            return
            
        # Limpiar círculos anteriores
        for line in self.ax.lines[1:]:  # Mantener el perfil del talud
            line.remove()
        for patch in self.ax.patches:
            patch.remove()
            
        # Dibujar nuevo círculo
        import matplotlib.patches as patches
        
        circle = patches.Circle(self.selected_center, self.radio_var.get(), 
                              fill=False, color='red', linewidth=2)
        self.ax.add_patch(circle)
        
        # Marcar el centro
        self.ax.plot(self.selected_center[0], self.selected_center[1], 
                    'ro', markersize=8, label='Centro del círculo')
        
        # Actualizar leyenda
        self.ax.legend()
        
        self.canvas.draw()
        
    def on_apply(self):
        """Aplicar la selección."""
        if self.selected_center:
            self.result = (self.selected_center[0], self.selected_center[1], self.radio_var.get())
            self.destroy()
            
    def on_cancel(self):
        """Cancelar la selección."""
        self.result = None
        self.destroy()
