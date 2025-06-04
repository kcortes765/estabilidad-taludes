"""
Test específico para encontrar el error exacto.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import traceback
import math
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple, crear_dovelas

def main():
    print("=== TEST ESPECÍFICO PARA ERROR ===")
    
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
        
        # Crear dovelas
        print("Creando dovelas...")
        dovelas = crear_dovelas(circulo, perfil, estrato, num_dovelas=8)
        print(f"✅ Dovelas creadas: {len(dovelas)}")
        
        # Probar validaciones una por una
        print("Probando validar_conjunto_dovelas...")
        from data.validation import validar_conjunto_dovelas
        resultado = validar_conjunto_dovelas(dovelas)
        print(f"✅ validar_conjunto_dovelas: {resultado.es_valido}")
        
        print("Probando validar_convergencia_bishop...")
        from data.validation import validar_convergencia_bishop
        factores = [1.0, 1.1]
        resultado = validar_convergencia_bishop(factores, 1)
        print(f"✅ validar_convergencia_bishop: {resultado.es_valido}")
        
        print("Probando validar_factor_seguridad...")
        from data.validation import validar_factor_seguridad
        resultado = validar_factor_seguridad(1.2)
        print(f"✅ validar_factor_seguridad: {resultado.es_valido}")
        
    except Exception as e:
        print(f"❌ Error específico: {e}")
        print("Traceback completo:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
