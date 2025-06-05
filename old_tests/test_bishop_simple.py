"""
Test simple para depurar Bishop.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import math
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple
from core.bishop import bishop_talud_homogeneo

def main():
    print("=== TEST SIMPLE DE BISHOP ===")
    
    try:
        # Test básico sin validaciones
        resultado = bishop_talud_homogeneo(
            altura=10.0,
            angulo_talud=45.0,
            cohesion=20.0,
            phi_grados=25.0,
            gamma=18.0,
            num_dovelas=8,
            validar_entrada=False  # Deshabilitar validaciones
        )
        
        print(f"✅ Factor de seguridad: {resultado.factor_seguridad:.3f}")
        print(f"✅ Convergió: {resultado.convergio}")
        print(f"✅ Iteraciones: {resultado.iteraciones}")
        print(f"✅ Es válido: {resultado.es_valido}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
