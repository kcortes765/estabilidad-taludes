"""Prueba rápida de factores de seguridad de los casos de ejemplo
Ejecutar con: python test_fs.py
"""
import sys
from gui_examples import CASOS_EJEMPLO
from core.geometry import CirculoFalla, Estrato, crear_dovelas
from core.bishop import analizar_bishop

print("\nTEST FACTOR DE SEGURIDAD - CASOS DE EJEMPLO")
print("="*60)
for nombre, caso in CASOS_EJEMPLO.items():
    print(f"\nCaso: {nombre}")
    try:
        circulo = CirculoFalla(caso['centro_x'], caso['centro_y'], caso['radio'])
        estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
        # Intentar crear dovelas
        dovelas = crear_dovelas(circulo, caso['perfil_terreno'], estrato, 10)
        resultado = analizar_bishop(circulo, caso['perfil_terreno'], estrato, 10)
        fs = resultado['factor_seguridad']
        print(f"  ✅ FS = {fs:.3f} ({len(dovelas)} dovelas)")
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
