#!/usr/bin/env python3
"""
Script de verificación completa del sistema de análisis de estabilidad de taludes.
Verifica instalación, dependencias, módulos y funcionalidad básica.
"""

import sys
import os
import importlib
from pathlib import Path

def print_header(title):
    """Imprimir encabezado con formato."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_section(title):
    """Imprimir sección con formato."""
    print(f"\n--- {title} ---")

def check_python_version():
    """Verificar versión de Python."""
    print_section("Verificando Python")
    version = sys.version_info
    print(f"Versión de Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✓ Versión de Python compatible")
        return True
    else:
        print("✗ Se requiere Python 3.8 o superior")
        return False

def check_dependencies():
    """Verificar dependencias requeridas."""
    print_section("Verificando Dependencias")
    
    dependencies = [
        'tkinter',
        'customtkinter', 
        'matplotlib',
        'numpy',
        'threading',
        'pathlib'
    ]
    
    success = True
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"✗ {dep} - NO ENCONTRADO")
            success = False
    
    return success

def check_project_structure():
    """Verificar estructura del proyecto."""
    print_section("Verificando Estructura del Proyecto")
    
    required_files = [
        'gui_app.py',
        'gui_analysis.py',
        'gui_components.py',
        'gui_plotting.py',
        'gui_examples.py',
        'core/bishop.py',
        'core/fellenius.py',
        'core/geometry.py',
        'data/models.py',
        'data/validation.py'
    ]
    
    success = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - NO ENCONTRADO")
            success = False
    
    return success

def check_imports():
    """Verificar importaciones del proyecto."""
    print_section("Verificando Importaciones del Proyecto")
    
    modules = [
        ('gui_analysis', 'analizar_desde_gui'),
        ('gui_examples', 'get_caso_ejemplo'),
        ('core.bishop', 'analizar_bishop'),
        ('core.fellenius', 'analizar_fellenius'),
        ('data.models', 'CirculoFalla'),
        ('data.validation', 'validar_parametros_geotecnicos')
    ]
    
    success = True
    for module_name, function_name in modules:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, function_name):
                print(f"✓ {module_name}.{function_name}")
            else:
                print(f"✗ {module_name}.{function_name} - FUNCIÓN NO ENCONTRADA")
                success = False
        except ImportError as e:
            print(f"✗ {module_name} - ERROR: {e}")
            success = False
    
    return success

def test_basic_functionality():
    """Probar funcionalidad básica."""
    print_section("Probando Funcionalidad Básica")
    
    try:
        # Test 1: Crear objetos básicos
        from data.models import CirculoFalla, Estrato
        circulo = CirculoFalla(xc=8.0, yc=14.0, radio=16.0)
        estrato = Estrato(cohesion=35.0, phi_grados=30.0, gamma=19.0)
        print("✓ Creación de objetos básicos")
        
        # Test 2: Funciones geométricas
        from core.geometry import crear_perfil_terreno
        perfil = crear_perfil_terreno(altura=8.0, angulo_grados=35.0)
        print("✓ Funciones geométricas")
        
        # Test 3: Análisis simple
        from core.bishop import analizar_bishop
        resultado = analizar_bishop(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            num_dovelas=10
        )
        print(f"✓ Análisis Bishop - FS: {resultado.factor_seguridad:.3f}")
        
        # Test 4: Wrapper GUI
        from gui_analysis import analizar_desde_gui
        from gui_examples import get_caso_ejemplo
        
        caso = get_caso_ejemplo("Talud Estable - Carretera")
        resultado_gui = analizar_desde_gui(caso)
        
        if resultado_gui['valido']:
            print(f"✓ Wrapper GUI - Bishop FS: {resultado_gui['bishop'].factor_seguridad:.3f}")
        else:
            print(f"✗ Wrapper GUI - Error: {resultado_gui.get('error', 'Desconocido')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error en funcionalidad básica: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_creation():
    """Probar creación de GUI."""
    print_section("Probando Creación de GUI")
    
    try:
        import customtkinter as ctk
        
        # Crear ventana de prueba
        root = ctk.CTk()
        root.title("Test GUI")
        root.geometry("400x300")
        
        # Crear componentes básicos
        label = ctk.CTkLabel(root, text="Sistema de Análisis de Estabilidad")
        label.pack(pady=20)
        
        button = ctk.CTkButton(root, text="Test Button")
        button.pack(pady=10)
        
        # Cerrar inmediatamente
        root.after(100, root.destroy)
        
        print("✓ GUI básica creada exitosamente")
        return True
        
    except Exception as e:
        print(f"✗ Error creando GUI: {e}")
        return False

def generate_report(results):
    """Generar reporte final."""
    print_header("REPORTE FINAL")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"Tests ejecutados: {total_tests}")
    print(f"Tests exitosos: {passed_tests}")
    print(f"Tests fallidos: {total_tests - passed_tests}")
    print(f"Tasa de éxito: {passed_tests/total_tests*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("La GUI puede ejecutarse sin problemas")
        print("\nPara ejecutar la GUI:")
        print("  python gui_app.py")
    else:
        print("\n⚠️  SISTEMA CON PROBLEMAS")
        print("Revisar errores antes de ejecutar la GUI")
        
        failed_tests = [test for test, result in results.items() if not result]
        print(f"\nTests fallidos: {', '.join(failed_tests)}")

def main():
    """Función principal."""
    print_header("VERIFICACIÓN COMPLETA DEL SISTEMA")
    print("Análisis de Estabilidad de Taludes - GUI")
    
    # Ejecutar verificaciones
    results = {}
    
    results['Python'] = check_python_version()
    results['Dependencias'] = check_dependencies()
    results['Estructura'] = check_project_structure()
    results['Importaciones'] = check_imports()
    results['Funcionalidad'] = test_basic_functionality()
    results['GUI'] = test_gui_creation()
    
    # Generar reporte
    generate_report(results)
    
    return all(results.values())

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nVerificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
