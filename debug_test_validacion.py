#!/usr/bin/env python3
"""
Debug específico para el test que falla
"""

import sys
import os

# Agregar path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.validation import validar_conjunto_dovelas
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple, crear_dovelas

def debug_test_especifico():
    """Debug del test específico que falla"""
    print("🔍 DEBUG: Test Validación Conjunto Dovelas")
    print("=" * 50)
    
    # Exactamente los mismos parámetros que usa el test
    circulo = CirculoFalla(xc=10.0, yc=8.0, radio=6.0)
    perfil = crear_perfil_simple(0.0, 10.0, 20.0, 0.0, 10)
    estrato = Estrato(cohesion=10.0, phi_grados=30.0, gamma=18.0, nombre="Arena")
    
    print(f"Configuración del test:")
    print(f"  Círculo: xc={circulo.xc}, yc={circulo.yc}, r={circulo.radio}")
    print(f"  Perfil: {len(perfil)} puntos")
    print(f"  Estrato: c={estrato.cohesion}, φ={estrato.phi_grados}°")
    
    # Test 1: Dovelas válidas (8 dovelas)
    print(f"\n📊 TEST 1: Conjunto válido (8 dovelas)")
    try:
        dovelas_validas = crear_dovelas(circulo, perfil, estrato, num_dovelas=8)
        print(f"  Dovelas creadas: {len(dovelas_validas)}")
        
        resultado = validar_conjunto_dovelas(dovelas_validas)
        print(f"  ✅ Es válido: {resultado.es_valido}")
        print(f"  📝 Mensaje: {resultado.mensaje}")
        print(f"  🔧 Código error: {resultado.codigo_error}")
        
        # Mostrar detalles si falla
        if not resultado.es_valido:
            print(f"  ❌ PROBLEMA DETECTADO")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
    
    # Test 2: Pocas dovelas (3 dovelas)
    print(f"\n📊 TEST 2: Pocas dovelas (3 dovelas)")
    try:
        dovelas_pocas = crear_dovelas(circulo, perfil, estrato, num_dovelas=3)
        print(f"  Dovelas creadas: {len(dovelas_pocas)}")
        
        resultado_pocas = validar_conjunto_dovelas(dovelas_pocas)
        print(f"  ✅ Es válido: {resultado_pocas.es_valido}")
        print(f"  📝 Mensaje: {resultado_pocas.mensaje}")
        print(f"  🔧 Código error: {resultado_pocas.codigo_error}")
        
        # El test espera que 3 dovelas pasen validación
        if resultado_pocas.es_valido:
            print(f"  ✅ CORRECTO: 3 dovelas pasan validación")
        else:
            print(f"  ❌ PROBLEMA: 3 dovelas NO pasan validación")
            print(f"      Esto causará que falle el test")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

if __name__ == "__main__":
    debug_test_especifico()
