#!/usr/bin/env python3
"""Test sin validación para evitar errores de validación y enfocarse en FS"""

import sys
sys.path.append('.')

from gui_examples import CASOS_EJEMPLO
from core.geometry import CirculoFalla, Estrato, crear_dovelas
from core.bishop import analizar_bishop

print("TEST SIN VALIDACIÓN - ENFOQUE EN FACTOR DE SEGURIDAD")
print("="*60)

for nombre, caso in CASOS_EJEMPLO.items():
    print(f"\n📋 Caso: {nombre}")
    print(f"   Centro: ({caso['centro_x']}, {caso['centro_y']}) Radio: {caso['radio']}")
    print(f"   Objetivo: {caso['esperado']}")
    
    try:
        # Crear objetos
        circulo = CirculoFalla(caso['centro_x'], caso['centro_y'], caso['radio'])
        estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
        
        # Intentar crear dovelas
        dovelas = crear_dovelas(circulo, caso['perfil_terreno'], estrato, 10)
        print(f"   ✅ Dovelas creadas: {len(dovelas)}")
        
        # Intentar análisis Bishop SIN VALIDACIÓN
        resultado = analizar_bishop(
            circulo=circulo, 
            perfil_terreno=caso['perfil_terreno'], 
            estrato=estrato, 
            num_dovelas=10,
            validar_entrada=False  # ¡CLAVE! Sin validación
        )
        
        fs = resultado['factor_seguridad']
        print(f"   ✅ Factor de Seguridad: {fs:.3f}")
        
        # Evaluar si FS es realista
        if 1.0 <= fs <= 3.0:
            print(f"   🎯 FS PERFECTO - Realista para geotecnia")
        elif 3.0 < fs <= 5.0:
            print(f"   ✅ FS BUENO - Aceptable")
        elif fs > 5.0:
            print(f"   ⚠️  FS MUY ALTO - Círculo muy conservador")
        elif fs < 1.0:
            print(f"   ⚠️  FS BAJO - Talud inestable")
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")

print("\n" + "="*60)
print("ANÁLISIS COMPLETADO")
