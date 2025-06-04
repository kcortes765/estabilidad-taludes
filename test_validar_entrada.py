"""
Test específico para validar_entrada_completa.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import traceback
import math
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple
from data.validation import validar_entrada_completa

def main():
    print("=== TEST VALIDAR_ENTRADA_COMPLETA ===")
    
    try:
        # Crear datos básicos
        altura = 10.0
        angulo_talud = 45.0
        longitud_base = altura / math.tan(math.radians(angulo_talud))
        
        # Crear perfil
        perfil = crear_perfil_simple(0.0, altura, longitud_base * 2, 0.0, 20)
        print("✅ Perfil creado")
        
        # Crear círculo
        radio = 1.5 * altura
        xc = longitud_base * 0.7
        yc = altura * 0.8
        circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
        print("✅ Círculo creado")
        
        # Crear estrato
        estrato = Estrato(cohesion=20.0, phi_grados=25.0, gamma=18.0, nombre="Test")
        print("✅ Estrato creado")
        
        print("Llamando a validar_entrada_completa...")
        
        # Llamar función
        validaciones = validar_entrada_completa(circulo, perfil, estrato, None)
        
        print(f"✅ validar_entrada_completa completada")
        print(f"Número de validaciones: {len(validaciones)}")
        
        for i, validacion in enumerate(validaciones):
            print(f"  {i+1}. {validacion.mensaje} (válido: {validacion.es_valido})")
        
    except Exception as e:
        print(f"❌ Error específico: {e}")
        print("Traceback completo:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
