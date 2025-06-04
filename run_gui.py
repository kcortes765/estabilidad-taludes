#!/usr/bin/env python3
"""
Script de inicio para la interfaz gráfica del sistema de análisis de estabilidad de taludes.
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Función principal para iniciar la aplicación GUI."""
    try:
        # Verificar dependencias
        print("Verificando dependencias...")
        
        try:
            import customtkinter
            print("✓ CustomTkinter disponible")
        except ImportError:
            print("✗ CustomTkinter no encontrado")
            print("Instale con: pip install customtkinter")
            return False
        
        try:
            import matplotlib
            print("✓ Matplotlib disponible")
        except ImportError:
            print("✗ Matplotlib no encontrado")
            print("Instale con: pip install matplotlib")
            return False
        
        try:
            import numpy
            print("✓ NumPy disponible")
        except ImportError:
            print("✗ NumPy no encontrado")
            print("Instale con: pip install numpy")
            return False
        
        # Verificar módulos del proyecto
        try:
            from core.bishop import analizar_bishop
            from core.fellenius import analizar_fellenius
            print("✓ Módulos de análisis disponibles")
        except ImportError as e:
            print(f"✗ Error importando módulos de análisis: {e}")
            return False
        
        try:
            from gui_app import SlopeStabilityApp
            print("✓ Módulos GUI disponibles")
        except ImportError as e:
            print(f"✗ Error importando módulos GUI: {e}")
            return False
        
        print("\nIniciando aplicación...")
        
        # Crear y ejecutar aplicación
        app = SlopeStabilityApp()
        app.run()
        
        return True
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nPresione Enter para salir...")
        input()
        sys.exit(1)
