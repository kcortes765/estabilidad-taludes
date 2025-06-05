"""
Test para debuggear el factor de seguridad alto en Bishop.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import traceback
import math
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple, crear_dovelas
from core.bishop import analizar_bishop, iteracion_bishop

def main():
    print("=== DEBUG FACTOR DE SEGURIDAD ALTO ===")
    
    try:
        # Crear datos básicos - parámetros más críticos
        altura = 10.0
        angulo_talud = 70.0  # Muy empinado
        longitud_base = altura / math.tan(math.radians(angulo_talud))
        
        # Crear perfil
        perfil = crear_perfil_simple(0.0, altura, longitud_base * 2, 0.0, 20)
        print("✅ Perfil creado")
        
        # Crear círculo crítico
        radio = altura  # Radio pequeño
        xc = longitud_base * 1.0  # En el talud
        yc = altura * 0.4  # Centro bajo
        circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
        print("✅ Círculo creado")
        
        # Crear estrato muy débil
        estrato = Estrato(cohesion=5.0, phi_grados=15.0, gamma=20.0, nombre="Débil")
        print("✅ Estrato creado")
        
        # Crear dovelas manualmente para debug
        dovelas = crear_dovelas(circulo, perfil, estrato, num_dovelas=6)
        print(f"✅ Dovelas creadas: {len(dovelas)}")
        
        # Analizar dovelas individualmente
        print("\n=== ANÁLISIS DE DOVELAS ===")
        for i, dovela in enumerate(dovelas):
            print(f"Dovela {i+1}:")
            print(f"  Peso: {dovela.peso:.2f} kN")
            print(f"  Ángulo α: {math.degrees(dovela.angulo_alpha):.1f}°")
            print(f"  sin α: {dovela.sin_alpha:.3f}")
            print(f"  cos α: {dovela.cos_alpha:.3f}")
            print(f"  tan φ: {dovela.tan_phi:.3f}")
            
            # Calcular m_alpha
            from core.bishop import calcular_m_alpha
            m_alpha = calcular_m_alpha(dovela, 1.0)
            print(f"  mα: {m_alpha:.3f}")
            
            # Calcular fuerzas
            from core.bishop import calcular_fuerza_resistente_bishop, calcular_fuerza_actuante_bishop
            fuerza_r = calcular_fuerza_resistente_bishop(dovela, 1.0)
            fuerza_a = calcular_fuerza_actuante_bishop(dovela)
            print(f"  Fuerza resistente: {fuerza_r:.2f} kN")
            print(f"  Fuerza actuante: {fuerza_a:.2f} kN")
            print()
        
        # Hacer una iteración
        print("=== ITERACIÓN BISHOP ===")
        nuevo_fs, fuerzas_r, fuerzas_a, m_alphas = iteracion_bishop(dovelas, 1.0)
        
        suma_r = sum(fuerzas_r)
        suma_a = sum(fuerzas_a)
        
        print(f"Suma fuerzas resistentes: {suma_r:.2f} kN")
        print(f"Suma fuerzas actuantes: {suma_a:.2f} kN")
        print(f"Factor de seguridad: {nuevo_fs:.3f}")
        
        if suma_a > 0:
            print(f"Ratio R/A: {suma_r/suma_a:.3f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
