#!/usr/bin/env python3
"""
Debug específico para el problema de Fellenius en plotting
"""

import sys
import os
import math

# Agregar path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.fellenius import fellenius_talud_homogeneo
from core.geometry import crear_perfil_simple
from data.models import CirculoFalla

def debug_fellenius_geometria():
    """Debug del problema de geometría en Fellenius"""
    print("🔍 DEBUG: Problema Fellenius en Plotting")
    print("=" * 50)
    
    # Parámetros del test actual
    longitud_base = 8.0 / math.tan(math.radians(30.0))
    print(f"Longitud base calculada: {longitud_base:.2f}")
    
    # Probar diferentes geometrías
    geometrias = [
        {"nombre": "Original (falla)", "xc": longitud_base * 0.5, "yc": 8.0 * 0.8, "radio": 1.2 * 8.0},
        {"nombre": "Más bajo", "xc": longitud_base * 0.5, "yc": 8.0 * 0.6, "radio": 1.0 * 8.0},
        {"nombre": "Más centrado", "xc": longitud_base * 0.7, "yc": 8.0 * 0.7, "radio": 1.1 * 8.0},
        {"nombre": "Conservador", "xc": longitud_base * 0.8, "yc": 8.0 * 0.9, "radio": 1.3 * 8.0},
    ]
    
    for i, geom in enumerate(geometrias, 1):
        print(f"\n📊 GEOMETRÍA {i}: {geom['nombre']}")
        print(f"  xc={geom['xc']:.2f}, yc={geom['yc']:.2f}, r={geom['radio']:.2f}")
        
        try:
            # Crear círculo y perfil
            perfil_vis = crear_perfil_simple(0.0, 8.0, longitud_base * 3, 0.0, 25)
            circulo_vis = CirculoFalla(xc=geom['xc'], yc=geom['yc'], radio=geom['radio'])
            
            # Probar análisis Fellenius
            resultado_fellenius = fellenius_talud_homogeneo(
                altura=8.0,
                angulo_talud=30.0,
                cohesion=25.0,
                phi_grados=20.0,
                gamma=18.0,
                num_dovelas=8
            )
            
            print(f"  ✅ ÉXITO: FS = {resultado_fellenius.factor_seguridad:.3f}")
            print(f"    Dovelas: {len(resultado_fellenius.dovelas)}")
            print(f"    Momento resistente: {resultado_fellenius.momento_resistente:.1f}")
            print(f"    Momento actuante: {resultado_fellenius.momento_actuante:.1f}")
            
            if resultado_fellenius.factor_seguridad > 0:
                print(f"  🎯 GEOMETRÍA VÁLIDA ENCONTRADA!")
                break
                
        except Exception as e:
            print(f"  ❌ FALLA: {e}")

if __name__ == "__main__":
    debug_fellenius_geometria()
