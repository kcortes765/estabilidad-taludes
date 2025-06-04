#!/usr/bin/env python3
"""
Test simple para verificar que la GUI funciona correctamente.
"""

def test_imports():
    """Probar importaciones básicas."""
    try:
        print("1. Probando importaciones...")
        
        # Importaciones básicas
        import customtkinter as ctk
        print("   ✓ CustomTkinter OK")
        
        from gui_analysis import analizar_desde_gui, validar_parametros_gui
        print("   ✓ GUI Analysis OK")
        
        from gui_examples import get_caso_ejemplo
        print("   ✓ GUI Examples OK")
        
        print("   ✓ Todas las importaciones exitosas")
        return True
        
    except Exception as e:
        print(f"   ✗ Error en importaciones: {e}")
        return False

def test_gui_analysis():
    """Probar análisis desde GUI."""
    try:
        print("\n2. Probando análisis GUI...")
        
        from gui_analysis import analizar_desde_gui
        from gui_examples import get_caso_ejemplo
        
        # Obtener caso de ejemplo
        caso = get_caso_ejemplo("Talud Estable - Carretera")
        print(f"   - Caso: {caso['descripcion']}")
        
        # Ejecutar análisis
        resultado = analizar_desde_gui(caso)
        
        if resultado['valido']:
            print(f"   ✓ Análisis exitoso:")
            print(f"     - Bishop FS: {resultado['bishop'].factor_seguridad:.3f}")
            print(f"     - Fellenius FS: {resultado['fellenius'].factor_seguridad:.3f}")
            return True
        else:
            print(f"   ✗ Análisis falló: {resultado.get('error', 'Error desconocido')}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_creation():
    """Probar creación básica de GUI."""
    try:
        print("\n3. Probando creación de GUI...")
        
        import customtkinter as ctk
        
        # Crear ventana simple
        root = ctk.CTk()
        root.title("Test GUI")
        root.geometry("300x200")
        
        # Crear label simple
        label = ctk.CTkLabel(root, text="GUI Test OK")
        label.pack(pady=20)
        
        # Cerrar inmediatamente
        root.after(1000, root.destroy)
        
        print("   ✓ GUI creada exitosamente")
        
        # No ejecutar mainloop para evitar bloqueo
        # root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error creando GUI: {e}")
        return False

if __name__ == "__main__":
    print("=== TEST GUI SIMPLE ===\n")
    
    success = True
    
    # Ejecutar tests
    success &= test_imports()
    success &= test_gui_analysis()
    success &= test_gui_creation()
    
    print(f"\n=== RESULTADO FINAL ===")
    if success:
        print("✓ Todos los tests pasaron exitosamente")
        print("La GUI debería funcionar correctamente")
    else:
        print("✗ Algunos tests fallaron")
        print("Revisar errores antes de ejecutar la GUI")
    
    print("\n=== FIN TEST ===")
