"""
Test simplificado para validaciones críticas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.validation import validar_parametros_geotecnicos, validar_factor_seguridad
from data.models import Estrato

def test_simple():
    print("=== TEST VALIDACIONES SIMPLE ===")
    
    # Test 1: Estrato válido
    estrato = Estrato(cohesion=10.0, phi_grados=30.0, gamma=18.0, nombre="Arena")
    resultado = validar_parametros_geotecnicos(estrato)
    print(f"Estrato válido: {resultado.es_valido} - {resultado.mensaje}")
    
    # Test 2: Cohesión alta
    estrato_alto = Estrato(cohesion=600.0, phi_grados=20.0, gamma=18.0, nombre="Arcilla")
    resultado_alto = validar_parametros_geotecnicos(estrato_alto)
    print(f"Cohesión alta: {resultado_alto.es_valido} - {resultado_alto.mensaje}")
    
    # Test 3: Factor de seguridad
    resultado_fs = validar_factor_seguridad(1.25)
    print(f"Factor seguridad: {resultado_fs.es_valido} - {resultado_fs.mensaje}")
    
    resultado_fs_bajo = validar_factor_seguridad(0.8)
    print(f"Factor bajo: {resultado_fs_bajo.es_valido} - {resultado_fs_bajo.mensaje}")
    
    print("✅ TESTS SIMPLES COMPLETADOS")

if __name__ == "__main__":
    test_simple()
