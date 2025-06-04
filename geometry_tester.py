"""
FASE 2: VALIDACIÓN DE CÁLCULOS GEOMÉTRICOS
Tests unitarios para verificar exactitud de funciones geométricas fundamentales
"""

import math
from typing import List, Tuple
from core.geometry import calcular_angulo_alpha, calcular_y_circulo, interpolar_terreno

def test_calcular_angulo_alpha():
    """
    Test unitario de calcular_angulo_alpha() con casos conocidos.
    """
    print("=" * 80)
    print("🧪 TEST UNITARIO: calcular_angulo_alpha()")
    print("=" * 80)
    
    # Caso 1: Círculo centrado en origen, punto en X=0 (punto más bajo)
    print("\n📐 CASO 1: Círculo centrado en origen")
    xc, yc, radio = 0, 0, 10
    casos_test = [
        (-10, "Extremo izquierdo"),
        (-5, "Izquierda intermedio"), 
        (0, "Centro (punto más bajo)"),
        (5, "Derecha intermedio"),
        (10, "Extremo derecho")
    ]
    
    for x, descripcion in casos_test:
        try:
            alpha = calcular_angulo_alpha(x, xc, yc, radio)
            alpha_grados = math.degrees(alpha)
            
            # Cálculo manual esperado
            sin_theta = x / radio
            theta = math.asin(sin_theta)
            alpha_esperado = theta
            alpha_esperado_grados = math.degrees(alpha_esperado)
            
            print(f"   X={x:3}: α={alpha_grados:6.1f}° (esperado: {alpha_esperado_grados:6.1f}°) - {descripcion}")
            
            # Verificar coherencia
            if abs(alpha_grados - alpha_esperado_grados) > 0.1:
                print(f"      ⚠️ DISCREPANCIA: diferencia de {abs(alpha_grados - alpha_esperado_grados):.1f}°")
                
        except Exception as e:
            print(f"   X={x:3}: ❌ ERROR - {e}")
    
    # Caso 2: Círculo desplazado - geometría problemática actual
    print(f"\n📐 CASO 2: Círculo problemático actual (xc=20, yc=-5, r=20)")
    xc, yc, radio = 20, -5, 20
    x_test = [2, 6, 10, 14, 18, 22, 26, 30, 34, 38]  # Positions de dovelas actuales
    
    for x in x_test:
        try:
            alpha = calcular_angulo_alpha(x, xc, yc, radio)
            alpha_grados = math.degrees(alpha)
            
            # Analizar si el ángulo es problemático
            estado = "✅ OK" if -45 <= alpha_grados <= 45 else "❌ PROBLEMÁTICO"
            if alpha_grados < -45:
                problema = "demasiado negativo"
            elif alpha_grados > 45:
                problema = "demasiado positivo"
            else:
                problema = ""
                
            print(f"   X={x:2}: α={alpha_grados:6.1f}° - {estado} {problema}")
            
        except Exception as e:
            print(f"   X={x:2}: ❌ ERROR - {e}")

def test_calcular_y_circulo():
    """
    Test unitario de calcular_y_circulo() para verificar intersecciones.
    """
    print("\n" + "=" * 80)
    print("🧪 TEST UNITARIO: calcular_y_circulo()")
    print("=" * 80)
    
    # Caso: círculo problemático actual
    xc, yc, radio = 20, -5, 20
    
    print(f"Círculo: centro=({xc}, {yc}), radio={radio}")
    print(f"Ecuación: (x - {xc})² + (y - {yc})² = {radio}²")
    
    x_test = [0, 10, 15, 20, 25, 30, 40]
    
    print(f"\n{'X':<3} {'Y_superior':<12} {'Y_inferior':<12} {'Manual_inf':<12} {'Diferencia':<10}")
    print("-" * 60)
    
    for x in x_test:
        y_sup = calcular_y_circulo(x, xc, yc, radio, parte_superior=True)
        y_inf = calcular_y_circulo(x, xc, yc, radio, parte_superior=False)
        
        # Cálculo manual para verificar
        discriminante = radio**2 - (x - xc)**2
        if discriminante >= 0:
            y_manual_inf = yc - math.sqrt(discriminante)
        else:
            y_manual_inf = None
            
        if y_inf is not None and y_manual_inf is not None:
            diferencia = abs(y_inf - y_manual_inf)
        else:
            diferencia = "N/A"
            
        print(f"{x:<3} {y_sup:<12} {y_inf:<12} {y_manual_inf:<12} {diferencia}")

def test_geometria_ideal():
    """
    Propone y testa una geometría que debería funcionar mejor.
    """
    print("\n" + "=" * 80)
    print("🎯 PROPUESTA: GEOMETRÍA IDEAL")
    print("=" * 80)
    
    # Perfil de terreno actual
    perfil = [(0, 10), (10, 10), (20, 0), (40, 0)]
    
    print("🏔️ Perfil del terreno:")
    for x, y in perfil:
        print(f"   ({x}, {y})")
    
    # Propuestas de círculos mejorados
    propuestas = [
        (15, 5, 12, "Círculo más alto y pequeño"),
        (20, 2, 15, "Centro ligeramente sobre el terreno"),
        (25, 8, 18, "Centro desplazado a la derecha"),
        (15, 15, 20, "Centro muy arriba del terreno")
    ]
    
    print(f"\n📊 ANÁLISIS DE PROPUESTAS:")
    print(f"{'Propuesta':<30} {'Centro':<12} {'Radio':<6} {'Rango_α':<15} {'Estado'}")
    print("-" * 80)
    
    for xc, yc, radio, descripcion in propuestas:
        # Analizar rango de ángulos en el rango de terreno
        x_min = max(0, xc - radio)  # Límite del perfil
        x_max = min(40, xc + radio)  # Límite del perfil
        
        if x_min >= x_max:
            estado = "❌ No intersecta"
            rango_alpha = "N/A"
        else:
            try:
                # Calcular ángulos en los extremos
                alpha_min = calcular_angulo_alpha(x_min, xc, yc, radio)
                alpha_max = calcular_angulo_alpha(x_max, xc, yc, radio)
                
                alpha_min_deg = math.degrees(alpha_min)
                alpha_max_deg = math.degrees(alpha_max)
                
                rango_alpha = f"[{alpha_min_deg:.1f}°, {alpha_max_deg:.1f}°]"
                
                # Evaluar si es aceptable
                if -45 <= alpha_min_deg <= 45 and -45 <= alpha_max_deg <= 45:
                    estado = "✅ VIABLE"
                else:
                    estado = "❌ Ángulos extremos"
                    
            except Exception as e:
                estado = f"❌ Error: {e}"
                rango_alpha = "N/A"
        
        print(f"{descripcion:<30} ({xc},{yc}){'':<6} {radio:<6} {rango_alpha:<15} {estado}")

if __name__ == "__main__":
    test_calcular_angulo_alpha()
    test_calcular_y_circulo()  
    test_geometria_ideal()
