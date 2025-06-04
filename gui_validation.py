"""
Sistema de validación en tiempo real para la GUI de análisis de estabilidad de taludes.
Previene la entrada de parámetros que generen dovelas inválidas.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, Tuple, Optional
from validacion_geometrica import ValidadorGeometrico, RangosValidos

class ValidadorGUI:
    """Validador en tiempo real para parámetros de la GUI"""
    
    def __init__(self):
        self.validador_geometrico = None
        self.rangos_validos = None
        
    def actualizar_perfil_terreno(self, altura: float, angulo_talud: float):
        """
        Actualiza el perfil del terreno y recalcula rangos válidos
        """
        try:
            import math
            
            # Calcular perfil basado en parámetros
            angulo_rad = math.radians(angulo_talud)
            proyeccion_horizontal = altura / math.tan(angulo_rad)
            longitud_total = 40
            
            perfil = [
                (0, altura),
                (longitud_total * 0.3, altura),
                (longitud_total * 0.3 + proyeccion_horizontal, 0),
                (longitud_total, 0)
            ]
            
            # Crear validador geométrico
            self.validador_geometrico = ValidadorGeometrico(perfil)
            self.rangos_validos = self.validador_geometrico.calcular_rangos_validos()
            
            return True
            
        except Exception as e:
            print(f"Error actualizando perfil: {e}")
            return False
    
    def validar_parametro_individual(self, parametro: str, valor: float) -> Tuple[bool, str]:
        """
        Valida un parámetro individual y retorna si es válido y mensaje
        
        Args:
            parametro: Nombre del parámetro ('centro_x', 'centro_y', 'radio')
            valor: Valor a validar
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if not self.rangos_validos:
            return True, "Rangos no calculados"
        
        if parametro == 'centro_x':
            if self.rangos_validos.centro_x_min <= valor <= self.rangos_validos.centro_x_max:
                return True, "✓ Centro X válido"
            else:
                return False, f"Centro X debe estar entre {self.rangos_validos.centro_x_min:.1f} y {self.rangos_validos.centro_x_max:.1f}"
        
        elif parametro == 'centro_y':
            if self.rangos_validos.centro_y_min <= valor <= self.rangos_validos.centro_y_max:
                return True, "✓ Centro Y válido"
            else:
                return False, f"Centro Y debe estar entre {self.rangos_validos.centro_y_min:.1f} y {self.rangos_validos.centro_y_max:.1f}"
        
        elif parametro == 'radio':
            if self.rangos_validos.radio_min <= valor <= self.rangos_validos.radio_max:
                return True, "✓ Radio válido"
            else:
                return False, f"Radio debe estar entre {self.rangos_validos.radio_min:.1f} y {self.rangos_validos.radio_max:.1f}"
        
        return True, "Parámetro no reconocido"
    
    def validar_configuracion_completa(self, centro_x: float, centro_y: float, radio: float) -> Tuple[bool, str, int]:
        """
        Valida la configuración completa del círculo
        
        Returns:
            Tupla (es_valido, mensaje, dovelas_estimadas)
        """
        if not self.validador_geometrico:
            return False, "Validador no inicializado", 0
        
        resultado = self.validador_geometrico.validar_parametros(centro_x, centro_y, radio)
        
        return resultado.es_valido, resultado.mensaje, resultado.dovelas_validas_estimadas
    
    def sugerir_parametros_validos(self) -> Optional[Dict[str, float]]:
        """
        Sugiere parámetros válidos basados en el perfil actual
        
        Returns:
            Diccionario con parámetros sugeridos o None si no es posible
        """
        if not self.validador_geometrico:
            return None
        
        return self.validador_geometrico.generar_parametros_validos_ejemplo()
    
    def get_rangos_validos(self) -> Optional[RangosValidos]:
        """Retorna los rangos válidos actuales"""
        return self.rangos_validos

class ValidadorEntrada:
    """Validador para campos de entrada de la GUI"""
    
    @staticmethod
    def validar_numero_positivo(valor_str: str, nombre_campo: str) -> Tuple[bool, str, float]:
        """
        Valida que un string sea un número positivo
        
        Returns:
            Tupla (es_valido, mensaje, valor_numerico)
        """
        try:
            valor = float(valor_str)
            if valor <= 0:
                return False, f"{nombre_campo} debe ser mayor que 0", 0.0
            return True, f"✓ {nombre_campo} válido", valor
        except ValueError:
            return False, f"{nombre_campo} debe ser un número válido", 0.0
    
    @staticmethod
    def validar_angulo(valor_str: str) -> Tuple[bool, str, float]:
        """
        Valida que un string sea un ángulo válido (0-90 grados)
        
        Returns:
            Tupla (es_valido, mensaje, valor_numerico)
        """
        try:
            valor = float(valor_str)
            if valor <= 0 or valor >= 90:
                return False, "Ángulo debe estar entre 0 y 90 grados", 0.0
            return True, "✓ Ángulo válido", valor
        except ValueError:
            return False, "Ángulo debe ser un número válido", 0.0
    
    @staticmethod
    def validar_cohesion(valor_str: str) -> Tuple[bool, str, float]:
        """
        Valida cohesión (0-500 kPa)
        """
        try:
            valor = float(valor_str)
            if valor < 0 or valor > 500:
                return False, "Cohesión debe estar entre 0 y 500 kPa", 0.0
            return True, "✓ Cohesión válida", valor
        except ValueError:
            return False, "Cohesión debe ser un número válido", 0.0
    
    @staticmethod
    def validar_phi(valor_str: str) -> Tuple[bool, str, float]:
        """
        Valida ángulo de fricción (0-50 grados)
        """
        try:
            valor = float(valor_str)
            if valor < 0 or valor > 50:
                return False, "Ángulo de fricción debe estar entre 0 y 50 grados", 0.0
            return True, "✓ Ángulo de fricción válido", valor
        except ValueError:
            return False, "Ángulo de fricción debe ser un número válido", 0.0
    
    @staticmethod
    def validar_peso_especifico(valor_str: str) -> Tuple[bool, str, float]:
        """
        Valida peso específico (10-30 kN/m³)
        """
        try:
            valor = float(valor_str)
            if valor < 10 or valor > 30:
                return False, "Peso específico debe estar entre 10 y 30 kN/m³", 0.0
            return True, "✓ Peso específico válido", valor
        except ValueError:
            return False, "Peso específico debe ser un número válido", 0.0

def crear_tooltip(widget, texto):
    """
    Crea un tooltip para un widget con información de validación
    """
    def mostrar_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        label = tk.Label(tooltip, text=texto, background="lightyellow", 
                        relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()
        
        def ocultar_tooltip():
            tooltip.destroy()
        
        tooltip.after(3000, ocultar_tooltip)  # Ocultar después de 3 segundos
    
    widget.bind("<Enter>", mostrar_tooltip)

def mostrar_ayuda_parametros():
    """
    Muestra una ventana de ayuda con información sobre parámetros válidos
    """
    ayuda = tk.Toplevel()
    ayuda.title("Ayuda - Parámetros Válidos")
    ayuda.geometry("600x400")
    
    texto_ayuda = """
GUÍA DE PARÁMETROS VÁLIDOS PARA ANÁLISIS DE TALUDES

PARÁMETROS GEOTÉCNICOS:
• Cohesión (c): 0-500 kPa
  - Arcillas: 10-100 kPa
  - Arenas: 0-10 kPa
  
• Ángulo de fricción (φ): 0-50°
  - Arcillas: 15-25°
  - Arenas: 30-45°
  
• Peso específico (γ): 10-30 kN/m³
  - Típico: 18-22 kN/m³

PARÁMETROS GEOMÉTRICOS:
• Altura del talud: 3-20 m (típico)
• Ángulo del talud: 15-60°
  - Estable: 15-35°
  - Crítico: 35-50°
  
• Centro del círculo:
  - Debe estar elevado sobre el terreno
  - Posición horizontal centrada en el talud
  
• Radio del círculo:
  - Debe intersectar suficientemente el terreno
  - Generar mínimo 10 dovelas válidas

CONSEJOS:
• Use los casos de ejemplo como referencia
• El sistema validará automáticamente los parámetros
• Parámetros inválidos generarán advertencias
• Para taludes críticos, use parámetros conservadores
"""
    
    text_widget = tk.Text(ayuda, wrap=tk.WORD, padx=10, pady=10)
    text_widget.insert(tk.END, texto_ayuda)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    btn_cerrar = tk.Button(ayuda, text="Cerrar", command=ayuda.destroy)
    btn_cerrar.pack(pady=10)

if __name__ == "__main__":
    # Ejemplo de uso del validador
    validador = ValidadorGUI()
    
    # Simular actualización con parámetros de talud
    validador.actualizar_perfil_terreno(altura=8.0, angulo_talud=35.0)
    
    # Validar parámetros
    es_valido, mensaje, dovelas = validador.validar_configuracion_completa(20.0, 18.0, 22.0)
    print(f"Validación: {mensaje}")
    print(f"Dovelas estimadas: {dovelas}")
    
    # Mostrar rangos válidos
    rangos = validador.get_rangos_validos()
    if rangos:
        print(f"Rangos válidos:")
        print(f"  Centro X: [{rangos.centro_x_min:.1f}, {rangos.centro_x_max:.1f}]")
        print(f"  Centro Y: [{rangos.centro_y_min:.1f}, {rangos.centro_y_max:.1f}]")
        print(f"  Radio: [{rangos.radio_min:.1f}, {rangos.radio_max:.1f}]")
