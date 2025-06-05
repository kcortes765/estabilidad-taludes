"""
Test directo de analizar_bishop con validaciones habilitadas.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import traceback
import math
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple
from core.bishop import analizar_bishop

def main():
    print("=== TEST BISHOP CON VALIDACIONES ===")
    
    try:
        # Crear datos básicos - parámetros más realistas
        altura = 15.0  # Talud más alto
        angulo_talud = 60.0  # Más empinado
        longitud_base = altura / math.tan(math.radians(angulo_talud))
        
        # Crear perfil
        perfil = crear_perfil_simple(0.0, altura, longitud_base * 2, 0.0, 20)
        print("✅ Perfil creado")
        
        # Crear círculo más crítico
        radio = 1.2 * altura  # Radio más pequeño
        xc = longitud_base * 0.8  # Más hacia el talud
        yc = altura * 0.6  # Centro más bajo
        circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
        print("✅ Círculo creado")
        
        # Crear estrato con parámetros más débiles
        estrato = Estrato(cohesion=10.0, phi_grados=20.0, gamma=19.0, nombre="Test")  # Suelo más débil
        print("✅ Estrato creado")
        
        print("Llamando a analizar_bishop CON validaciones...")
        
        # Llamar función con validaciones habilitadas
        resultado = analizar_bishop(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            nivel_freatico=None,
            num_dovelas=8,
            factor_inicial=1.0,
            tolerancia=0.001,
            max_iteraciones=50,
            validar_entrada=True  # HABILITADO
        )
        
        print("✅ Análisis completado")
        print(f"Factor de seguridad: {resultado.factor_seguridad:.3f}")
        print(f"Convergió: {resultado.convergio}")
        print(f"Iteraciones: {resultado.iteraciones}")
        
    except Exception as e:
        print(f"❌ Error específico: {e}")
        print("Traceback completo:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
