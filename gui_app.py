"""
Aplicación principal de la interfaz gráfica para análisis de estabilidad de taludes.
"""

import customtkinter as ctk
import logging
from logging_utils import get_logger
import tkinter as tk
import tkinter.messagebox as messagebox
import threading
logger = get_logger(__name__)
import numpy as np

from gui_components import ParameterPanel, ResultsPanel, ToolsPanel
from gui_plotting import PlottingPanel
from gui_dialogs import ParametricDialog


class SlopeStabilityApp:
    """Aplicación principal para análisis de estabilidad de taludes."""
    
    def __init__(self):
        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.setup_window()
        
        # Variables de estado
        self.current_bishop_result = None
        self.current_fellenius_result = None
        self.analysis_running = False
        
        # Configurar interfaz
        self.setup_ui()
        self.setup_menu()
    
    def setup_window(self):
        """Configurar ventana principal."""
        self.root.title("Sistema de Análisis de Estabilidad de Taludes v2.0")
        
        # Configurar para pantalla completa
        self.root.state('zoomed')  # Windows maximizado
        
        # Configuración alternativa para otros sistemas
        try:
            self.root.attributes('-zoomed', True)  # Linux
        except:
            pass
        
        # Configurar tamaño mínimo
        self.root.minsize(1200, 800)
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurar grid principal
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def setup_ui(self):
        """Configurar la interfaz de usuario."""
        # Frame principal con grid
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel izquierdo con scroll
        left_scroll_frame = ctk.CTkScrollableFrame(main_frame, width=450)
        left_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Panel de parámetros
        self.parameter_panel = ParameterPanel(left_scroll_frame, self.on_parameter_change)
        self.parameter_panel.pack(fill="x", pady=(0, 5))
        
        # Panel de resultados
        self.results_panel = ResultsPanel(left_scroll_frame)
        self.results_panel.pack(fill="x", pady=5)
        
        # Panel de herramientas
        self.tools_panel = ToolsPanel(left_scroll_frame, app_instance=self)
        self.tools_panel.pack(fill="x", pady=(5, 0))
        
        # Panel derecho (visualización)
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Panel de plotting
        self.plotting_panel = PlottingPanel(right_frame)
        self.plotting_panel.grid(row=0, column=0, sticky="nsew")
        
        # Barra de estado
        self.setup_status_bar()
    
    def setup_menu(self):
        """Configurar barra de menú."""
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        menu_frame.grid_propagate(False)
        
        # Botones del menú
        help_btn = ctk.CTkButton(menu_frame, text="❓ Ayuda", command=self.show_help, 
                                width=80, height=30)
        help_btn.pack(side="right", padx=5, pady=5)
        
        about_btn = ctk.CTkButton(menu_frame, text="ℹ️ Acerca de", command=self.show_about,
                                 width=100, height=30)
        about_btn.pack(side="right", padx=5, pady=5)
    
    def setup_status_bar(self):
        """Configurar barra de estado."""
        self.status_frame = ctk.CTkFrame(self.root, height=30)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_frame.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Listo para análisis", 
                                        font=ctk.CTkFont(size=12))
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, width=200)
        self.progress_bar.pack(side="right", padx=10, pady=5)
        self.progress_bar.set(0)
    
    def on_parameter_change(self, command=None):
        """Callback cuando cambian los parámetros."""
        logger.debug('on_parameter_change llamado con comando: %s', command)
        
        if command == 'show_geometry':
            logger.debug('Ejecutando show_geometry')
            # Mostrar solo la geometría del talud
            self.show_slope_geometry()
        elif command == 'run_analysis':
            logger.debug('Ejecutando run_analysis')
            # Ejecutar análisis completo
            self.run_analysis()
        elif self.current_bishop_result or self.current_fellenius_result:
            logger.debug('Auto-actualizando análisis existente')
            # Auto-actualizar si hay resultados previos
            self.run_analysis()
        else:
            logger.debug('Comando no reconocido o sin resultados previos: %s', command)
    
    def show_slope_geometry(self):
        """Mostrar solo la geometría del talud sin análisis."""
        logger.debug('Iniciando show_slope_geometry')
        try:
            # Obtener parámetros
            params = self.parameter_panel.get_parameters()
            logger.debug('Parámetros obtenidos: %s', params)
            
            # Generar perfil del talud
            from data.models import generar_perfil_simple
            perfil_terreno = generar_perfil_simple(
                altura=params['altura'],
                angulo_grados=params['angulo_talud'],
            )
            logger.debug('Perfil generado con %d puntos', len(perfil_terreno))
            
            # Mostrar en el panel de plotting
            self.plotting_panel.show_slope_only(perfil_terreno, params)
            logger.debug('Perfil enviado al panel de plotting')
            
            self.update_status(f"Geometría cargada: Talud {params['altura']:.1f}m, ángulo {params['angulo_talud']:.1f}°")
            
        except Exception as e:
            logger.exception('Error en show_slope_geometry: %s', e)
            self.update_status(f"Error al cargar geometría: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def run_analysis(self):
        """Ejecutar análisis en hilo separado."""
        if self.analysis_running:
            return
        
        self.analysis_running = True
        self.update_status("Ejecutando análisis...")
        self.progress_bar.set(0.1)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self._run_analysis_thread)
        thread.daemon = True
        thread.start()
    
    def _run_analysis_thread(self):
        """Ejecutar análisis en hilo separado."""
        try:
            # Obtener parámetros
            params = self.parameter_panel.get_parameters()
            
            self.progress_bar.set(0.3)
            self.update_status("Validando parámetros...")
            
            # Importar clases y funciones necesarias
            from data.models import generar_perfil_simple, CirculoFalla
            from core.circle_constraints import (
                aplicar_limites_inteligentes,
                validar_circulo_geometricamente,
            )
            from gui_analysis import analizar_desde_gui

            # 1. Generar perfil del talud (similar a show_slope_geometry)
            #    Consider using a shared utility if this logic is duplicated often.
            try:
                perfil_terreno = generar_perfil_simple(
                    altura=params['altura'],
                    angulo_grados=params['angulo_talud'],
                )
            except Exception as e:
                self.update_status(f"Error generando perfil para validación: {e}")
                messagebox.showerror("Error Interno", f"No se pudo generar el perfil del talud para validación: {e}")
                self.analysis_running = False
                self.progress_bar.set(0)
                return

            # 2. Calcular límites geométricos automáticos basados en el perfil
            try:
                limites_geometricos = aplicar_limites_inteligentes(
                    perfil_terreno, "talud_empinado"
                )
            except Exception as e:
                self.update_status(f"Error calculando límites geométricos: {e}")
                messagebox.showerror(
                    "Error Interno",
                    f"No se pudo calcular los límites geométricos: {e}",
                )
                self.analysis_running = False
                self.progress_bar.set(0)
                return

            # 3. Crear objeto CirculoFalla con parámetros de la GUI
            circulo_actual = CirculoFalla(xc=params['centro_x'],
                                        yc=params['centro_y'],
                                        radio=params['radio'])

            # 4. Validar y corregir el círculo
            self.update_status("Validando geometría del círculo...")
            resultado_validacion = validar_circulo_geometricamente(
                circulo_actual,
                limites_geometricos,
                corregir_automaticamente=True,
            )

            if not resultado_validacion.es_valido:
                if resultado_validacion.circulo_corregido:
                    self.update_status("Círculo original inválido, aplicando corrección automática...")
                    messagebox.showwarning(
                        "Corrección Automática",
                        f"El círculo original era inválido y ha sido corregido.\n"
                        f"Violaciones: {'; '.join(resultado_validacion.violaciones)}\n"
                        f"Sugerencias: {'; '.join(resultado_validacion.sugerencias)}"
                    )
                    logger.info('Violaciones de círculo: %s', resultado_validacion.violaciones)
                    params['centro_x'] = resultado_validacion.circulo_corregido.xc
                    params['centro_y'] = resultado_validacion.circulo_corregido.yc
                    params['radio'] = resultado_validacion.circulo_corregido.radio

                    if hasattr(self.parameter_panel, 'update_circle_entries'):
                        self.parameter_panel.update_circle_entries(
                            params['centro_x'], params['centro_y'], params['radio']
                        )
                    else:
                        logger.warning('ParameterPanel no tiene update_circle_entries. Los campos no se actualizarán visualmente.')
                        self.update_status(
                            "Círculo corregido. Ejecute 'Mostrar Geometría' para ver cambios si no se reflejan."
                        )
                else:
                    logger.warning('ParameterPanel no tiene update_circle_entries. Los campos no se actualizarán visualmente.')
                    messagebox.showerror(
                        "Error de Validación",
                        f"El círculo de falla es inválido y no pudo ser corregido automáticamente.\n"
                        f"Violaciones: {'; '.join(resultado_validacion.violaciones)}\n"
                        f"Sugerencias: {'; '.join(resultado_validacion.sugerencias)}"
                    )
                    self.analysis_running = False
                    self.progress_bar.set(0)
                    return # Detener análisis
            else:
                self.update_status("Geometría del círculo validada.")

            self.progress_bar.set(0.5)
            self.update_status("Ejecutando análisis...")
            
            # Ejecutar análisis usando wrapper
            resultado = analizar_desde_gui(params)
            
            self.progress_bar.set(0.8)
            
            if resultado['valido']:
                # Análisis exitoso
                self.current_bishop_result = resultado['bishop']
                self.current_fellenius_result = resultado['fellenius']
                
                self.progress_bar.set(1.0)
                self.update_status("Análisis completado exitosamente")
                
                # Actualizar resultados en la GUI
                self.root.after(100, lambda: self._update_results_ui(resultado))
                
            else:
                # Error en análisis
                error_msg = resultado.get('error', 'Error desconocido')
                self.progress_bar.set(0.0)
                self.update_status(f"Error: {error_msg}")
                
                # Mostrar error al usuario
                self.root.after(100, lambda: self._show_analysis_error(error_msg))
            
        except Exception as e:
            # Error inesperado
            import traceback
            error_msg = f"Error inesperado: {str(e)}"
            traceback.print_exc()
            
            self.progress_bar.set(0.0)
            self.update_status(error_msg)
            self.root.after(100, lambda: self._show_analysis_error(error_msg))
        
        finally:
            self.analysis_running = False
            self.root.after(100, lambda: self.progress_bar.set(0.0))
    
    def _update_results_ui(self, resultado):
        """Actualizar interfaz con resultados del análisis."""
        try:
            # Mostrar mensaje sobre correcciones automáticas si aplica
            if 'mensaje_limites' in resultado:
                self.update_status(resultado['mensaje_limites'])
                # También mostrar en diálogo informativo si hubo corrección
                if resultado.get('circulo_corregido', False):
                    self.root.after(500, lambda: self._show_circle_correction_info(resultado))
            
            # Actualizar panel de resultados
            if hasattr(self, 'results_panel'):
                self.results_panel.update_results(
                    bishop_result=resultado['bishop'],
                    fellenius_result=resultado['fellenius']
                )
            
            # Actualizar gráfico
            if hasattr(self, 'plotting_panel'):
                self.plotting_panel.update_analysis(
                    perfil_terreno=resultado['perfil_terreno'],
                    circulo=resultado['circulo'],
                    dovelas=resultado['bishop'].dovelas,
                    nivel_freatico=resultado.get('nivel_freatico'),
                    bishop_result=resultado['bishop'],
                    fellenius_result=resultado['fellenius']
                )
                
        except Exception as e:
            logger.exception("Error actualizando UI: %s", e)
    
    def _show_analysis_error(self, error_msg):
        """Mostrar error de análisis al usuario y registrarlo."""
        logger.error("%s", error_msg)
        self.update_status(error_msg)
        import tkinter.messagebox as messagebox
        messagebox.showerror(
            "Error en Análisis",
            f"No se pudo completar el análisis:\n\n{error_msg}\n\n"
            "Verifique los parámetros e intente nuevamente."
        )
    
    def run_parametric_analysis(self):
        """Ejecutar análisis paramétrico."""
        if self.analysis_running:
            messagebox.showwarning("Análisis en Curso", "Espere a que termine el análisis actual")
            return
        
        # Obtener parámetros base
        base_params = self.parameter_panel.get_parameters()
        
        # Mostrar diálogo de configuración
        dialog = ParametricDialog(self.root, base_params)
        
        if dialog.result:
            self._run_parametric_analysis(dialog.result)
    
    def _run_parametric_analysis(self, config):
        """Ejecutar análisis paramétrico."""
        self.analysis_running = True
        self.update_status("Ejecutando análisis paramétrico...")
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self._parametric_analysis_thread, args=(config,))
        thread.daemon = True
        thread.start()
    
    def _parametric_analysis_thread(self, config):
        """Ejecutar análisis paramétrico en hilo separado."""
        try:
            parameter = config['parameter']
            param_range = config['range']
            base_params = config['base_params']
            
            bishop_results = []
            fellenius_results = []
            
            total_steps = len(param_range)
            
            for i, param_value in enumerate(param_range):
                # Actualizar progreso
                progress = (i + 1) / total_steps
                self.progress_bar.set(progress)
                self.update_status(f"Análisis paramétrico: {i+1}/{total_steps}")
                
                # Configurar parámetros
                current_params = base_params.copy()
                current_params[parameter] = param_value
                
                # Ejecutar análisis
                if current_params['con_agua']:
                    bishop_result = bishop_talud_homogeneo(
                        altura=current_params['altura'],
                        angulo_talud=current_params['angulo_talud'],
                        cohesion=current_params['cohesion'],
                        phi_grados=current_params['phi_grados'],
                        gamma=current_params['gamma'],
                        num_dovelas=current_params['num_dovelas'],
                        altura_nf=current_params['altura_nf']
                    )
                    fellenius_result = fellenius_talud_homogeneo(
                        altura=current_params['altura'],
                        angulo_talud=current_params['angulo_talud'],
                        cohesion=current_params['cohesion'],
                        phi_grados=current_params['phi_grados'],
                        gamma=current_params['gamma'],
                        num_dovelas=current_params['num_dovelas'],
                        altura_nf=current_params['altura_nf']
                    )
                else:
                    bishop_result = bishop_talud_homogeneo(
                        altura=current_params['altura'],
                        angulo_talud=current_params['angulo_talud'],
                        cohesion=current_params['cohesion'],
                        phi_grados=current_params['phi_grados'],
                        gamma=current_params['gamma'],
                        num_dovelas=current_params['num_dovelas']
                    )
                    fellenius_result = fellenius_talud_homogeneo(
                        altura=current_params['altura'],
                        angulo_talud=current_params['angulo_talud'],
                        cohesion=current_params['cohesion'],
                        phi_grados=current_params['phi_grados'],
                        gamma=current_params['gamma'],
                        num_dovelas=current_params['num_dovelas']
                    )
                
                bishop_results.append(bishop_result)
                fellenius_results.append(fellenius_result)
            
            # Actualizar resultados
            parametric_data = {
                'parameter': parameter,
                'range': param_range,
                'bishop_results': bishop_results,
                'fellenius_results': fellenius_results
            }
            
            self.root.after(0, self._update_parametric_results, parametric_data)
            
        except Exception as e:
            error_msg = f"Error en análisis paramétrico: {str(e)}"
            self.root.after(0, self._handle_analysis_error, error_msg)
    
    def _update_parametric_results(self, parametric_data):
        """Actualizar resultados de análisis paramétrico."""
        # Actualizar gráfico de comparación con datos paramétricos
        self.plotting_panel.update_parametric_plot(parametric_data)
        
        self.progress_bar.set(1.0)
        self.update_status("Análisis paramétrico completado")
        self.analysis_running = False
        
        messagebox.showinfo("Análisis Completado", 
                          f"Análisis paramétrico completado.\n"
                          f"Parámetro: {parametric_data['parameter']}\n"
                          f"Puntos analizados: {len(parametric_data['range'])}")
    
    def update_status(self, message):
        """Actualizar mensaje de estado."""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
    
    def on_closing(self):
        """Manejar cierre de aplicación."""
        if self.analysis_running:
            if messagebox.askokcancel("Cerrar", "Hay un análisis en curso. ¿Desea cerrar la aplicación?"):
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Ejecutar la aplicación."""
        self.root.mainloop()
    
    def find_critical_fs(self):
        """Encontrar el factor de seguridad crítico optimizando la ubicación del círculo."""
        try:
            from gui_analysis import buscar_fs_critico_gui
            
            # Obtener parámetros actuales
            params = self.parameter_panel.get_parameters()
            
            # Mostrar diálogo de progreso
            progress_dialog = ctk.CTkToplevel(self.root)
            progress_dialog.title("Buscando FS Crítico")
            progress_dialog.geometry("400x200")
            progress_dialog.transient(self.root)
            progress_dialog.grab_set()
            
            # Centrar diálogo
            progress_dialog.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (progress_dialog.winfo_width() // 2)
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (progress_dialog.winfo_height() // 2)
            progress_dialog.geometry(f"+{x}+{y}")
            
            # Contenido del diálogo
            ctk.CTkLabel(progress_dialog, text="🎯 BÚSQUEDA DE FS CRÍTICO", 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
            
            status_label = ctk.CTkLabel(progress_dialog, text="Iniciando búsqueda...")
            status_label.pack(pady=10)
            
            progress_bar = ctk.CTkProgressBar(progress_dialog, width=300)
            progress_bar.pack(pady=10)
            progress_bar.set(0)
            
            # Configurar rangos de búsqueda
            altura = params['altura']
            
            # Rangos para centro del círculo
            rango_centro_x = (-altura, altura*2)
            rango_centro_y = (altura*0.8, altura*2.5)
            rango_radio = (altura*0.6, altura*2)
            
            # Ejecutar búsqueda
            resultado_busqueda = buscar_fs_critico_gui(
                params_base=params,
                rango_centro_x=rango_centro_x,
                rango_centro_y=rango_centro_y,
                rango_radio=rango_radio,
                num_iteraciones=200
            )
            
            if resultado_busqueda['valido']:
                best_config = resultado_busqueda['mejor_config']
                min_fs = resultado_busqueda['fs_critico']
                
                # Actualizar parámetros con la mejor configuración
                self.root.after(0, lambda: self.parameter_panel.update_circle_params(
                    best_config['centro_x'],
                    best_config['centro_y'],
                    best_config['radio']
                ))
                
                # Actualizar resultados
                self.current_bishop_result = best_config['resultado']['bishop']
                self.current_fellenius_result = best_config['resultado']['fellenius']
                
                # Actualizar UI
                self.root.after(0, lambda: self._update_results_ui(best_config['resultado']))
                
                mensaje = (f"FS Crítico encontrado: {min_fs:.3f}\n"
                         f"Centro: ({best_config['centro_x']:.1f}, {best_config['centro_y']:.1f})\n"
                         f"Radio: {best_config['radio']:.1f} m\n"
                         f"Tasa de éxito: {resultado_busqueda['tasa_exito']:.1%}")
            else:
                mensaje = "No se encontró una configuración válida"
            
            progress_dialog.destroy()
            
            if resultado_busqueda['valido']:
                messagebox.showinfo("FS Crítico Encontrado", mensaje)
            else:
                messagebox.showwarning("Sin Resultado", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar búsqueda crítica: {str(e)}")
    
    def update_progress(self, progress_bar, status_label, progress, current, total):
        """Actualizar barra de progreso."""
        progress_bar.set(progress)
        status_label.configure(text=f"Evaluando configuración {current}/{total}...")
    
    def show_critical_result(self, dialog, best_config):
        """Mostrar resultado de búsqueda crítica."""
        dialog.destroy()
        
        if best_config:
            # Actualizar parámetros con la configuración crítica
            self.parameter_panel.centro_x_var.set(best_config['centro_x'])
            self.parameter_panel.centro_y_var.set(best_config['centro_y'])
            self.parameter_panel.radio_var.set(best_config['radio'])
            
            # Actualizar resultados
            self.current_results = {
                'bishop': best_config['resultado']['bishop'],
                'fellenius': best_config['resultado']['fellenius']
            }
            
            # Actualizar displays
            self.results_panel.update_results(self.current_results)
            self.plotting_panel.update_plots(self.current_results, self.parameter_panel.get_parameters())
            
            # Mostrar mensaje
            messagebox.showinfo("FS Crítico Encontrado", 
                              f"Factor de Seguridad Crítico: {best_config['fs']:.3f}\n\n"
                              f"Ubicación del círculo crítico:\n"
                              f"Centro X: {best_config['centro_x']:.2f} m\n"
                              f"Centro Y: {best_config['centro_y']:.2f} m\n"
                              f"Radio: {best_config['radio']:.2f} m\n\n"
                              f"Los parámetros han sido actualizados automáticamente.")
        else:
            messagebox.showwarning("Sin Resultado", 
                                 "No se pudo encontrar una configuración válida.\n"
                                 "Intente ajustar los parámetros del talud.")
    
    def show_error(self, dialog, message):
        """Mostrar error en búsqueda."""
        dialog.destroy()
        messagebox.showerror("Error", message)
    
    def show_help(self):
        """Mostrar diálogo de ayuda."""
        from gui_dialogs import AppUtils
        AppUtils.show_help(self.root)
    
    def show_about(self):
        """Mostrar información sobre la aplicación."""
        messagebox.showinfo("Acerca de", 
                          "Análisis de Estabilidad de Taludes\n\n"
                          "Versión: 1.0\n"
                          "Métodos: Bishop Modificado y Fellenius\n"
                          "Desarrollado para análisis geotécnico profesional\n\n"
                          " 2024 Sistema de Análisis de Estabilidad")
    
    def _show_circle_correction_info(self, resultado):
        """Mostrar información sobre corrección automática de círculos."""
        try:
            if 'circulo_original' in resultado and 'circulo' in resultado:
                original = resultado['circulo_original']
                corregido = resultado['circulo']
                
                mensaje = " CORRECCIÓN AUTOMÁTICA DE CÍRCULO\n\n"
                mensaje += "El sistema detectó parámetros problemáticos y aplicó correcciones automáticas:\n\n"
                
                mensaje += "Parámetros ORIGINALES:\n"
                mensaje += f"• Centro X: {original.xc:.2f} m\n"
                mensaje += f"• Centro Y: {original.yc:.2f} m\n"
                mensaje += f"• Radio: {original.radio:.2f} m\n\n"
                
                mensaje += "Parámetros CORREGIDOS:\n"
                mensaje += f"• Centro X: {corregido.xc:.2f} m\n"
                mensaje += f"• Centro Y: {corregido.yc:.2f} m\n"
                mensaje += f"• Radio: {corregido.radio:.2f} m\n\n"
                
                if 'mensaje_limites' in resultado:
                    mensaje += f"Motivo: {resultado['mensaje_limites']}\n\n"
                
                mensaje += "Esta corrección evita errores como 'fuerzas actuantes ≤ 0' y garantiza resultados realistas."
                
                messagebox.showinfo("Corrección Automática", mensaje)
                
        except Exception as e:
            logger.exception('Error mostrando información de corrección: %s', e)


def main():
    """Función principal para ejecutar la aplicación."""
    app = SlopeStabilityApp()
    app.run()


if __name__ == "__main__":
    main()
