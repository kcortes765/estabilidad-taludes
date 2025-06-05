"""
Componentes de la interfaz gráfica para análisis de estabilidad de taludes.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from gui_examples import get_nombres_casos, get_caso_ejemplo


class ParameterPanel(ctk.CTkFrame):
    """Panel de parámetros del talud."""

    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz del panel de parámetros."""
        # Título
        title = ctk.CTkLabel(
            self, text="Parámetros del Talud", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

        # Geometría
        geom_frame = ctk.CTkFrame(self)
        geom_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(
            geom_frame, text="GEOMETRÍA", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=5)

        # Altura
        ctk.CTkLabel(geom_frame, text="Altura (m):").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        self.altura_var = tk.DoubleVar(value=8.0)
        self.altura_entry = ctk.CTkEntry(
            geom_frame, textvariable=self.altura_var, width=80
        )
        self.altura_entry.grid(row=1, column=1, padx=5, pady=2)
        self.altura_slider = ctk.CTkSlider(
            geom_frame,
            from_=3,
            to=20,
            variable=self.altura_var,
            command=self.on_parameter_change,
        )
        self.altura_slider.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

        # Ángulo del talud
        ctk.CTkLabel(geom_frame, text="Ángulo (°):").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        self.angulo_var = tk.DoubleVar(value=30.0)
        self.angulo_entry = ctk.CTkEntry(
            geom_frame, textvariable=self.angulo_var, width=80
        )
        self.angulo_entry.grid(row=2, column=1, padx=5, pady=2)
        self.angulo_slider = ctk.CTkSlider(
            geom_frame,
            from_=15,
            to=60,
            variable=self.angulo_var,
            command=self.on_parameter_change,
        )
        self.angulo_slider.grid(row=2, column=2, padx=5, pady=2, sticky="ew")

        # Propiedades del suelo
        soil_frame = ctk.CTkFrame(self)
        soil_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(
            soil_frame, text="PROPIEDADES DEL SUELO", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=5)

        # Cohesión
        ctk.CTkLabel(soil_frame, text="Cohesión (kPa):").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        self.cohesion_var = tk.DoubleVar(value=25.0)
        self.cohesion_entry = ctk.CTkEntry(
            soil_frame, textvariable=self.cohesion_var, width=80
        )
        self.cohesion_entry.grid(row=1, column=1, padx=5, pady=2)
        self.cohesion_slider = ctk.CTkSlider(
            soil_frame,
            from_=5,
            to=100,
            variable=self.cohesion_var,
            command=self.on_parameter_change,
        )
        self.cohesion_slider.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

        # Ángulo de fricción
        ctk.CTkLabel(soil_frame, text="Fricción (°):").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        self.phi_var = tk.DoubleVar(value=20.0)
        self.phi_entry = ctk.CTkEntry(soil_frame, textvariable=self.phi_var, width=80)
        self.phi_entry.grid(row=2, column=1, padx=5, pady=2)
        self.phi_slider = ctk.CTkSlider(
            soil_frame,
            from_=10,
            to=45,
            variable=self.phi_var,
            command=self.on_parameter_change,
        )
        self.phi_slider.grid(row=2, column=2, padx=5, pady=2, sticky="ew")

        # Peso específico
        ctk.CTkLabel(soil_frame, text="Peso esp. (kN/m³):").grid(
            row=3, column=0, padx=5, pady=2, sticky="w"
        )
        self.gamma_var = tk.DoubleVar(value=18.0)
        self.gamma_entry = ctk.CTkEntry(
            soil_frame, textvariable=self.gamma_var, width=80
        )
        self.gamma_entry.grid(row=3, column=1, padx=5, pady=2)
        self.gamma_slider = ctk.CTkSlider(
            soil_frame,
            from_=14,
            to=25,
            variable=self.gamma_var,
            command=self.on_parameter_change,
        )
        self.gamma_slider.grid(row=3, column=2, padx=5, pady=2, sticky="ew")

        # Análisis
        analysis_frame = ctk.CTkFrame(self)
        analysis_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(
            analysis_frame,
            text="CONFIGURACIÓN DE ANÁLISIS",
            font=ctk.CTkFont(weight="bold"),
        ).grid(row=0, column=0, columnspan=2, pady=5)

        # Número de dovelas
        ctk.CTkLabel(analysis_frame, text="Dovelas:").grid(
            row=1, column=0, sticky="w", padx=5
        )
        self.dovelas_var = tk.IntVar(value=10)
        self.dovelas_entry = ctk.CTkEntry(
            analysis_frame, textvariable=self.dovelas_var, width=80
        )
        self.dovelas_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.dovelas_slider = ctk.CTkSlider(
            analysis_frame,
            from_=5,
            to=20,
            number_of_steps=15,
            variable=self.dovelas_var,
            width=200,
        )
        self.dovelas_slider.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

        # Configuración del círculo de falla
        circle_frame = ctk.CTkFrame(self)
        circle_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(
            circle_frame, text="CÍRCULO DE FALLA", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=5)

        # Centro X
        ctk.CTkLabel(circle_frame, text="Centro X (m):").grid(
            row=1, column=0, sticky="w", padx=5
        )
        self.centro_x_var = tk.DoubleVar(value=0.0)
        self.centro_x_entry = ctk.CTkEntry(
            circle_frame, textvariable=self.centro_x_var, width=80
        )
        self.centro_x_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.centro_x_slider = ctk.CTkSlider(
            circle_frame,
            from_=-20,
            to=20,
            number_of_steps=80,
            variable=self.centro_x_var,
            width=200,
        )
        self.centro_x_slider.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

        # Centro Y
        ctk.CTkLabel(circle_frame, text="Centro Y (m):").grid(
            row=2, column=0, sticky="w", padx=5
        )
        self.centro_y_var = tk.DoubleVar(value=15.0)
        self.centro_y_entry = ctk.CTkEntry(
            circle_frame, textvariable=self.centro_y_var, width=80
        )
        self.centro_y_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        self.centro_y_slider = ctk.CTkSlider(
            circle_frame,
            from_=5,
            to=30,
            number_of_steps=50,
            variable=self.centro_y_var,
            width=200,
        )
        self.centro_y_slider.grid(row=2, column=2, padx=5, pady=2, sticky="ew")

        # Radio
        ctk.CTkLabel(circle_frame, text="Radio (m):").grid(
            row=3, column=0, sticky="w", padx=5
        )
        self.radio_var = tk.DoubleVar(value=12.0)
        self.radio_entry = ctk.CTkEntry(
            circle_frame, textvariable=self.radio_var, width=80
        )
        self.radio_entry.grid(row=3, column=1, padx=5, pady=2, sticky="w")
        self.radio_slider = ctk.CTkSlider(
            circle_frame,
            from_=5,
            to=25,
            number_of_steps=40,
            variable=self.radio_var,
            width=200,
        )
        self.radio_slider.grid(row=3, column=2, padx=5, pady=2, sticky="ew")

        # Nivel freático
        water_frame = ctk.CTkFrame(self)
        water_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(
            water_frame, text="NIVEL FREÁTICO", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=5)

        # Activar nivel freático
        self.agua_var = tk.BooleanVar(value=False)
        self.agua_check = ctk.CTkCheckBox(
            water_frame,
            text="Considerar nivel freático",
            variable=self.agua_var,
            command=self.on_water_toggle,
        )
        self.agua_check.grid(row=1, column=0, columnspan=3, padx=5, pady=2)

        # Altura del nivel freático
        ctk.CTkLabel(water_frame, text="Altura NF (m):").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        self.altura_nf_var = tk.DoubleVar(value=3.0)
        self.altura_nf_entry = ctk.CTkEntry(
            water_frame, textvariable=self.altura_nf_var, width=80
        )
        self.altura_nf_entry.grid(row=2, column=1, padx=5, pady=2)
        self.altura_nf_slider = ctk.CTkSlider(
            water_frame,
            from_=0,
            to=15,
            variable=self.altura_nf_var,
            command=self.on_parameter_change,
        )
        self.altura_nf_slider.grid(row=2, column=2, padx=5, pady=2, sticky="ew")

        # Casos de ejemplo
        example_frame = ctk.CTkFrame(self)
        example_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(
            example_frame, text="CASOS DE EJEMPLO", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        # Selector de casos de ejemplo
        casos_disponibles = ["Manual (valores propios)"] + get_nombres_casos()
        self.example_var = tk.StringVar(value="Manual (valores propios)")
        self.example_option = ctk.CTkOptionMenu(
            example_frame,
            values=casos_disponibles,
            variable=self.example_var,
            command=self.on_example_change,
        )
        self.example_option.grid(
            row=1, column=0, columnspan=2, padx=5, pady=2, sticky="ew"
        )

        # Etiqueta de descripción del caso
        self.case_description = ctk.CTkLabel(
            example_frame,
            text="Ingrese sus propios valores",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        self.case_description.grid(row=2, column=0, columnspan=2, padx=5, pady=2)

        # Botón Cargar Geometría
        load_geometry_frame = ctk.CTkFrame(self)
        load_geometry_frame.grid(
            row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        self.load_geometry_btn = ctk.CTkButton(
            load_geometry_frame,
            text="🏔️ Cargar Geometría",
            command=self.on_load_geometry,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.load_geometry_btn.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        # Botón Seleccionar Círculo (inicialmente oculto)
        self.select_circle_btn = ctk.CTkButton(
            load_geometry_frame,
            text="🎯 Seleccionar Círculo",
            command=self.on_select_circle,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="orange",
            hover_color="darkorange",
        )
        self.select_circle_btn.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.select_circle_btn.grid_remove()  # Ocultar inicialmente

        load_geometry_frame.grid_columnconfigure(0, weight=1)
        load_geometry_frame.grid_columnconfigure(1, weight=1)

        # Inicialmente deshabilitar controles de agua
        self.toggle_water_controls(False)

        # Configurar grid weights
        self.grid_columnconfigure(0, weight=1)
        soil_frame.grid_columnconfigure(2, weight=1)
        analysis_frame.grid_columnconfigure(2, weight=1)
        water_frame.grid_columnconfigure(2, weight=1)
        example_frame.grid_columnconfigure(1, weight=1)

        # Bind eventos de entrada manual
        for entry in [
            self.altura_entry,
            self.angulo_entry,
            self.cohesion_entry,
            self.phi_entry,
            self.gamma_entry,
            self.dovelas_entry,
            self.altura_nf_entry,
        ]:
            entry.bind("<KeyRelease>", self.on_entry_change)

    def on_parameter_change(self, value=None):
        """Callback cuando cambia un parámetro."""
        if self.callback:
            self.callback()

    def on_entry_change(self, event=None):
        """Callback cuando se cambia un valor manualmente."""
        if self.callback:
            self.callback()

    def on_water_toggle(self):
        """Toggle de controles de nivel freático."""
        enabled = self.agua_var.get()
        self.toggle_water_controls(enabled)
        if self.callback:
            self.callback()

    def update_sliders(self):
        """Actualizar todos los sliders con los valores actuales."""
        self.altura_slider.set(self.altura_var.get())
        self.angulo_slider.set(self.angulo_var.get())
        self.cohesion_slider.set(self.cohesion_var.get())
        self.phi_slider.set(self.phi_var.get())
        self.gamma_slider.set(self.gamma_var.get())
        self.dovelas_slider.set(self.dovelas_var.get())
        self.centro_x_slider.set(self.centro_x_var.get())
        self.centro_y_slider.set(self.centro_y_var.get())
        self.radio_slider.set(self.radio_var.get())
        self.altura_nf_slider.set(self.altura_nf_var.get())

    def on_example_change(self, value):
        """Callback cuando se selecciona un caso de ejemplo."""
        if value == "Manual (valores propios)":
            self.case_description.configure(text="Ingrese sus propios valores")
        else:
            caso_ejemplo = get_caso_ejemplo(value)
            if caso_ejemplo:
                self.altura_var.set(caso_ejemplo["altura"])
                self.angulo_var.set(caso_ejemplo["angulo_talud"])
                self.cohesion_var.set(caso_ejemplo["cohesion"])
                self.phi_var.set(caso_ejemplo["phi_grados"])
                self.gamma_var.set(caso_ejemplo["gamma"])
                self.agua_var.set(caso_ejemplo["con_agua"])
                self.altura_nf_var.set(caso_ejemplo["nivel_freatico"])

                # Cargar parámetros del círculo
                self.centro_x_var.set(caso_ejemplo["centro_x"])
                self.centro_y_var.set(caso_ejemplo["centro_y"])
                self.radio_var.set(caso_ejemplo["radio"])

                # Actualizar sliders
                self.update_sliders()

                # Mostrar descripción del caso
                self.case_description.configure(text=caso_ejemplo["descripcion"])

                if self.callback:
                    self.callback()

    def toggle_water_controls(self, enabled):
        """Habilitar/deshabilitar controles de agua."""
        state = "normal" if enabled else "disabled"
        self.altura_nf_entry.configure(state=state)
        self.altura_nf_slider.configure(state=state)

    def get_parameters(self):
        """Obtener todos los parámetros actuales."""
        return {
            "altura": self.altura_var.get(),
            "angulo_talud": self.angulo_var.get(),
            "cohesion": self.cohesion_var.get(),
            "phi_grados": self.phi_var.get(),
            "gamma": self.gamma_var.get(),
            "num_dovelas": int(self.dovelas_var.get()),
            "con_agua": self.agua_var.get(),
            "altura_nf": self.altura_nf_var.get(),
            "centro_x": self.centro_x_var.get(),
            "centro_y": self.centro_y_var.get(),
            "radio": self.radio_var.get(),
        }

    def update_circle_params(self, centro_x, centro_y, radio):
        """Actualizar parámetros del círculo de falla."""
        self.centro_x_var.set(centro_x)
        self.centro_y_var.set(centro_y)
        self.radio_var.set(radio)

        # Actualizar sliders
        self.centro_x_slider.set(centro_x)
        self.centro_y_slider.set(centro_y)
        self.radio_slider.set(radio)

        if self.callback:
            self.callback()

    def update_circle_entries(self, xc: float, yc: float, radio: float) -> None:
        """Actualizar los campos de entrada del círculo sin disparar callbacks."""
        # Actualizar variables asociadas a los CTkEntry
        self.centro_x_var.set(xc)
        self.centro_y_var.set(yc)
        self.radio_var.set(radio)

        # Reflejar en las entradas manualmente para evitar artefactos
        self.centro_x_entry.delete(0, tk.END)
        self.centro_x_entry.insert(0, f"{xc:.2f}")
        self.centro_y_entry.delete(0, tk.END)
        self.centro_y_entry.insert(0, f"{yc:.2f}")
        self.radio_entry.delete(0, tk.END)
        self.radio_entry.insert(0, f"{radio:.2f}")

        # Mantener coherencia con sliders pero sin ejecutar callback
        self.centro_x_slider.set(xc)
        self.centro_y_slider.set(yc)
        self.radio_slider.set(radio)

    def on_load_geometry(self):
        """Callback para cargar y mostrar la geometría del talud."""
        # Obtener parámetros actuales
        params = self.get_parameters()

        # Llamar al callback para mostrar el talud en el panel principal
        if self.callback:
            # Usar el callback con el comando específico
            self.callback("show_geometry")
        else:
            print("ERROR: No hay callback configurado!")

        # Mostrar el botón de selección de círculo
        self.select_circle_btn.grid()

        # Cambiar texto del botón de cargar geometría
        self.load_geometry_btn.configure(text="🔄 Actualizar Geometría")

        print(f"on_load_geometry ejecutado con parámetros: {params}")

    def on_select_circle(self):
        """Callback para selección manual del círculo de falla."""
        # Obtener parámetros actuales
        params = self.get_parameters()

        # Crear ventana para selección manual del círculo
        from gui_dialogs import ManualCircleDialog

        dialog = ManualCircleDialog(self, params)

        if dialog.result:
            # Actualizar parámetros del círculo con la selección manual
            centro_x, centro_y, radio = dialog.result
            self.update_circle_params(centro_x, centro_y, radio)

            # Ejecutar análisis automáticamente después de seleccionar
            if self.callback:
                self.callback("run_analysis")


class ResultsPanel(ctk.CTkFrame):
    """Panel de resultados del análisis."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz del panel de resultados."""
        # Título
        title = ctk.CTkLabel(
            self,
            text="Resultados del Análisis",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        title.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Frame para Bishop
        bishop_frame = ctk.CTkFrame(self)
        bishop_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            bishop_frame, text="MÉTODO DE BISHOP", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        # Factor de seguridad Bishop
        ctk.CTkLabel(bishop_frame, text="Factor de Seguridad:").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        self.fs_bishop_label = ctk.CTkLabel(
            bishop_frame, text="---", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.fs_bishop_label.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Iteraciones
        ctk.CTkLabel(bishop_frame, text="Iteraciones:").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        self.iter_label = ctk.CTkLabel(bishop_frame, text="---")
        self.iter_label.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # Convergencia
        ctk.CTkLabel(bishop_frame, text="Convergió:").grid(
            row=3, column=0, padx=5, pady=2, sticky="w"
        )
        self.conv_label = ctk.CTkLabel(bishop_frame, text="---")
        self.conv_label.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # Frame para Fellenius
        fellenius_frame = ctk.CTkFrame(self)
        fellenius_frame.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            fellenius_frame, text="MÉTODO DE FELLENIUS", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        # Factor de seguridad Fellenius
        ctk.CTkLabel(fellenius_frame, text="Factor de Seguridad:").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        self.fs_fellenius_label = ctk.CTkLabel(
            fellenius_frame, text="---", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.fs_fellenius_label.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Momento resistente
        ctk.CTkLabel(fellenius_frame, text="Mom. Resistente:").grid(
            row=2, column=0, padx=5, pady=2, sticky="w"
        )
        self.mr_label = ctk.CTkLabel(fellenius_frame, text="---")
        self.mr_label.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # Momento actuante
        ctk.CTkLabel(fellenius_frame, text="Mom. Actuante:").grid(
            row=3, column=0, padx=5, pady=2, sticky="w"
        )
        self.ma_label = ctk.CTkLabel(fellenius_frame, text="---")
        self.ma_label.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # Frame de interpretación
        interp_frame = ctk.CTkFrame(self)
        interp_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            interp_frame, text="INTERPRETACIÓN", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        # Estado de estabilidad
        ctk.CTkLabel(interp_frame, text="Estado:").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        self.estado_label = ctk.CTkLabel(
            interp_frame, text="---", font=ctk.CTkFont(size=14, weight="bold")
        )
        self.estado_label.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Recomendación
        ctk.CTkLabel(interp_frame, text="Recomendación:").grid(
            row=2, column=0, padx=5, pady=2, sticky="nw"
        )
        self.recom_label = ctk.CTkLabel(interp_frame, text="---", wraplength=300)
        self.recom_label.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # Comparación de métodos
        comp_frame = ctk.CTkFrame(self)
        comp_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            comp_frame, text="COMPARACIÓN DE MÉTODOS", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(comp_frame, text="Diferencia (%):").grid(
            row=1, column=0, padx=5, pady=2, sticky="w"
        )
        self.diff_label = ctk.CTkLabel(comp_frame, text="---")
        self.diff_label.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Configurar grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def update_results(self, bishop_result=None, fellenius_result=None):
        """Actualizar los resultados mostrados."""
        # Actualizar Bishop
        if bishop_result:
            fs_bishop = bishop_result.factor_seguridad
            self.fs_bishop_label.configure(text=f"{fs_bishop:.3f}")
            self.iter_label.configure(text=str(bishop_result.iteraciones))
            self.conv_label.configure(text="Sí" if bishop_result.convergio else "No")

            # Determinar color según factor de seguridad
            if fs_bishop >= 2.0:
                color = "green"
                estado = "MUY SEGURO"
                recom = "Talud muy estable, proceder con confianza"
            elif fs_bishop >= 1.5:
                color = "green"
                estado = "SEGURO"
                recom = "Talud estable, condiciones aceptables"
            elif fs_bishop >= 1.3:
                color = "orange"
                estado = "ACEPTABLE"
                recom = "Talud marginalmente estable, monitorear"
            elif fs_bishop >= 1.0:
                color = "orange"
                estado = "MARGINAL"
                recom = "Talud en límite, considerar refuerzo"
            else:
                color = "red"
                estado = "INESTABLE"
                recom = "Talud inestable, rediseño necesario"

            self.fs_bishop_label.configure(text_color=color)
            self.estado_label.configure(text=estado, text_color=color)
            self.recom_label.configure(text=recom)
        else:
            self.fs_bishop_label.configure(text="---", text_color="white")
            self.iter_label.configure(text="---")
            self.conv_label.configure(text="---")

        # Actualizar Fellenius
        if fellenius_result:
            fs_fellenius = fellenius_result.factor_seguridad
            self.fs_fellenius_label.configure(text=f"{fs_fellenius:.3f}")
            self.mr_label.configure(
                text=f"{fellenius_result.momento_resistente:.1f} kN·m"
            )
            self.ma_label.configure(
                text=f"{fellenius_result.momento_actuante:.1f} kN·m"
            )

            # Color según factor de seguridad
            if fs_fellenius >= 1.5:
                color = "green"
            elif fs_fellenius >= 1.3:
                color = "orange"
            else:
                color = "red"
            self.fs_fellenius_label.configure(text_color=color)
        else:
            self.fs_fellenius_label.configure(text="---", text_color="white")
            self.mr_label.configure(text="---")
            self.ma_label.configure(text="---")

        # Comparación
        if bishop_result and fellenius_result:
            diff = (
                (bishop_result.factor_seguridad - fellenius_result.factor_seguridad)
                / fellenius_result.factor_seguridad
            ) * 100
            self.diff_label.configure(text=f"{diff:+.1f}%")
        else:
            self.diff_label.configure(text="---")


class ToolsPanel(ctk.CTkFrame):
    """Panel de herramientas y botones de análisis."""

    def __init__(self, parent, app_instance):
        super().__init__(parent)
        self.app = app_instance
        self.setup_ui()

    def setup_ui(self):
        """Configurar interfaz del panel."""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="HERRAMIENTAS DE ANÁLISIS",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        title_label.pack(pady=10)

        # Botones principales
        main_buttons_frame = ctk.CTkFrame(self)
        main_buttons_frame.pack(fill="x", padx=10, pady=5)

        # Botón Analizar
        self.analyze_btn = ctk.CTkButton(
            main_buttons_frame,
            text="🔍 ANALIZAR TALUD",
            command=self.run_analysis,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40,
            fg_color="green",
            hover_color="darkgreen",
        )
        self.analyze_btn.pack(fill="x", pady=2)

        # Botón FS Crítico
        self.critical_btn = ctk.CTkButton(
            main_buttons_frame,
            text="🎯 ENCONTRAR FS CRÍTICO",
            command=self.find_critical_fs,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40,
            fg_color="orange",
            hover_color="darkorange",
        )
        self.critical_btn.pack(fill="x", pady=2)

        # Botones secundarios
        secondary_frame = ctk.CTkFrame(self)
        secondary_frame.pack(fill="x", padx=10, pady=5)

        # Análisis paramétrico
        self.parametric_btn = ctk.CTkButton(
            secondary_frame,
            text="📊 Análisis Paramétrico",
            command=self.run_parametric_analysis,
            height=35,
        )
        self.parametric_btn.pack(fill="x", pady=1)

        # Botones de utilidad
        utility_frame = ctk.CTkFrame(self)
        utility_frame.pack(fill="x", padx=10, pady=5)

        # Frame para botones en fila
        button_row = ctk.CTkFrame(utility_frame)
        button_row.pack(fill="x", pady=2)

        self.clear_btn = ctk.CTkButton(
            button_row, text="🗑️ Limpiar", command=self.clear_results, width=100
        )
        self.clear_btn.pack(fill="x", expand=True)

        # Ayuda
        self.help_btn = ctk.CTkButton(
            utility_frame, text="❓ Ayuda", command=self.show_help, height=30
        )
        self.help_btn.pack(fill="x", pady=2)

    def run_analysis(self):
        """Ejecutar análisis normal."""
        if self.app:
            self.app.run_analysis()

    def find_critical_fs(self):
        """Encontrar factor de seguridad crítico optimizando la ubicación del círculo."""
        if self.app:
            self.app.find_critical_fs()

    def run_parametric_analysis(self):
        """Ejecutar análisis paramétrico."""
        if self.app:
            self.app.run_parametric_analysis()

    def clear_results(self):
        """Limpiar resultados."""
        if self.app:
            self.app.clear_results()

    def show_help(self):
        """Mostrar ayuda."""
        if self.app:
            self.app.show_help()
