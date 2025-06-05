"""
Test directo de analizar_bishop con debugging específico.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import math
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple
from core.bishop import analizar_bishop

def main():
    print("=== TEST DIRECTO DE ANALIZAR_BISHOP ===")
    
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
        
        print("Llamando a analizar_bishop...")
        
        # Llamar función paso a paso
        resultado = analizar_bishop(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            nivel_freatico=None,
            num_dovelas=8,
            factor_inicial=1.0,
            tolerancia=0.001,
            max_iteraciones=50,
            validar_entrada=False
        )
        
        print("✅ Análisis completado")
        print(f"Factor de seguridad: {resultado.factor_seguridad:.3f}")
        print(f"Convergió: {resultado.convergio}")
        print(f"Iteraciones: {resultado.iteraciones}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
