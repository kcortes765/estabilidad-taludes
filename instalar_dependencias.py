#!/usr/bin/env python3
"""
Script para instalar automáticamente las dependencias requeridas.
"""

import subprocess
import sys
import importlib

def install_package(package):
    """Instalar un paquete usando pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install():
    """Verificar e instalar dependencias."""
    dependencies = [
        'customtkinter',
        'matplotlib',
        'numpy'
    ]
    
    print("=== INSTALACIÓN DE DEPENDENCIAS ===\n")
    
    for package in dependencies:
        print(f"Verificando {package}...")
        
        try:
            importlib.import_module(package)
            print(f"✓ {package} ya está instalado")
        except ImportError:
            print(f"✗ {package} no encontrado. Instalando...")
            
            if install_package(package):
                print(f"✓ {package} instalado exitosamente")
            else:
                print(f"✗ Error instalando {package}")
                return False
    
    print("\n=== INSTALACIÓN COMPLETADA ===")
    print("Todas las dependencias están instaladas.")
    return True

if __name__ == "__main__":
    success = check_and_install()
    if success:
        print("\n🎉 Sistema listo para ejecutar la GUI")
        print("Ejecute: python gui_app.py")
    else:
        print("\n⚠️  Problemas durante la instalación")
        print("Instale manualmente las dependencias faltantes")
