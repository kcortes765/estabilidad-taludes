#!/usr/bin/env python3
"""
Script de inicio mejorado para la aplicación GUI de estabilidad de taludes.
"""

import sys
import os
import traceback
from logging_utils import setup_logging

def main():
    """Función principal con manejo de errores."""
    try:
        setup_logging()
        print("Iniciando aplicación GUI de Estabilidad de Taludes...")
        print("=" * 50)
        
        # Verificar imports
        print("Verificando módulos...")
        
        try:
            from gui_examples import get_caso_ejemplo, get_nombres_casos
            print("✓ gui_examples")
        except Exception as e:
            print(f"✗ gui_examples: {e}")
            return
        
        try:
            import gui_components
            print("✓ gui_components")
        except Exception as e:
            print(f"✗ gui_components: {e}")
            return
        
        try:
            import gui_dialogs
            print("✓ gui_dialogs")
        except Exception as e:
            print(f"✗ gui_dialogs: {e}")
            return
        
        try:
            from gui_app import SlopeStabilityApp
            print("✓ gui_app")
        except Exception as e:
            print(f"✗ gui_app: {e}")
            return
        
        print("\nTodos los módulos importados correctamente.")
        print("Iniciando aplicación...")
        print("=" * 50)
        
        # Crear y ejecutar aplicación
        app = SlopeStabilityApp()
        app.root.mainloop()
        
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("\nDetalles del error:")
        traceback.print_exc()
        input("\nPresione Enter para salir...")

if __name__ == "__main__":
    main()
