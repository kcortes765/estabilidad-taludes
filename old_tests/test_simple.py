#!/usr/bin/env python3
"""Test simple para verificar creación de dovelas"""

import sys
sys.path.append('.')

from gui_examples import CASOS_EJEMPLO
from core.geometry import CirculoFalla, Estrato, crear_dovelas
from core.bishop import analizar_bishop

print("TEST SIMPLE DE CREACIÓN DE DOVELAS")
print("="*50)

for nombre, caso in CASOS_EJEMPLO.items():
    print(f"\n📋 Caso: {nombre}")
    print(f"   Centro: ({caso['centro_x']}, {caso['centro_y']}) Radio: {caso['radio']}")
    
    try:
        # Crear objetos
        circulo = CirculoFalla(caso['centro_x'], caso['centro_y'], caso['radio'])
        estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
        
        # Intentar crear dovelas
        dovelas = crear_dovelas(circulo, caso['perfil_terreno'], estrato, 10)
        print(f"   ✅ Dovelas creadas: {len(dovelas)}")
        
        # Intentar análisis Bishop
        resultado = analizar_bishop(circulo, caso['perfil_terreno'], estrato, 10)
        fs = resultado['factor_seguridad']
        print(f"   ✅ Factor de Seguridad: {fs:.3f}")
        
        # Evaluar si FS es realista
        if fs > 10:
            print(f"   ⚠️  FS MUY ALTO - Círculo muy conservador")
        elif fs < 0.5:
            print(f"   ⚠️  FS MUY BAJO - Círculo muy crítico")
        else:
            print(f"   🎯 FS RAZONABLE")
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")

print("\n" + "="*50)
print("FIN DEL TEST")
