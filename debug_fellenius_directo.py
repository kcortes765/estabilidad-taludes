#!/usr/bin/env python3
"""
Debug usando análisis directo de Fellenius con geometría específica
"""

import sys
import os
import math

# Agregar path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.fellenius import analizar_fellenius
from core.geometry import crear_perfil_simple
from data.models import CirculoFalla, Estrato

def debug_fellenius_directo():
    """Debug usando análisis directo"""
    print("🔍 DEBUG: Fellenius con geometría específica")
    print("=" * 50)
    
    # Crear el mismo perfil que usa el test
    longitud_base = 8.0 / math.tan(math.radians(30.0))  # ~13.86
    perfil = crear_perfil_simple(0.0, 8.0, longitud_base * 3, 0.0, 25)
    
    print(f"Perfil creado: {len(perfil)} puntos")
    print(f"  Inicio: {perfil[0]}")
    print(f"  Fin: {perfil[-1]}")
    
    # Probar diferentes círculos que intersecten bien el perfil
    circulos = [
        CirculoFalla(xc=15.0, yc=5.0, radio=12.0),  # Círculo amplio
        CirculoFalla(xc=20.0, yc=8.0, radio=15.0),  # Círculo muy amplio
        CirculoFalla(xc=10.0, yc=10.0, radio=8.0),  # Círculo más alto
        CirculoFalla(xc=20.0, yc=9.0, radio=14.0),  # Variación del que casi funcionó
        CirculoFalla(xc=18.0, yc=8.5, radio=13.0),  # Más centrado
        CirculoFalla(xc=22.0, yc=8.0, radio=16.0),  # Más a la derecha
        CirculoFalla(xc=20.0, yc=7.0, radio=15.0),  # Más bajo
    ]
    
    # Estrato homogéneo
    estrato = Estrato(
        cohesion=25.0,
        phi_grados=20.0,
        gamma=18.0,
        nombre="Arena"
    )
    
    for i, circulo in enumerate(circulos, 1):
        print(f"\n📊 CÍRCULO {i}: xc={circulo.xc}, yc={circulo.yc}, r={circulo.radio}")
        
        try:
            resultado = analizar_fellenius(
                circulo=circulo,
                perfil_terreno=perfil,
                estrato=estrato,
                num_dovelas=8
            )
            
            if resultado.es_valido:
                print(f"  ✅ ÉXITO: FS = {resultado.factor_seguridad:.3f}")
                print(f"    Dovelas: {len(resultado.dovelas)}")
                print(f"    Momento resistente: {resultado.momento_resistente:.1f}")
                print(f"    Momento actuante: {resultado.momento_actuante:.1f}")
                return circulo, resultado
            else:
                print(f"  ⚠️  INVÁLIDO: {resultado.mensaje_error}")
                
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
    
    print("\n❌ Ningún círculo funcionó")
    return None, None

if __name__ == "__main__":
    debug_fellenius_directo()
