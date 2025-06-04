"""
FASE 2 AMPLIADA: ANÁLISIS PASO A PASO DEL MÉTODO BISHOP
Debugging profundo de la implementación del método Bishop
"""

import math
from typing import List, Tuple
from data.models import CirculoFalla, Estrato, Dovela
from core.geometry import crear_dovelas
from core.bishop import calcular_m_alpha, calcular_fuerza_resistente_bishop, calcular_fuerza_actuante_bishop

def debug_bishop_paso_a_paso():
    """
    Analiza paso a paso el método de Bishop para identificar errores conceptuales.
    """
    print("=" * 100)
    print("🔬 ANÁLISIS PASO A PASO DEL MÉTODO BISHOP")
    print("=" * 100)
    
    # Usar una dovela individual problemática para análisis
    perfil = [(0, 10), (10, 10), (20, 0), (40, 0)]
    circulo = CirculoFalla(xc=20, yc=-5, radio=20)
    estrato = Estrato(cohesion=15.0, phi_grados=20.0, gamma=18.0, nombre="Test")
    
    # Generar dovelas
    dovelas = crear_dovelas(circulo, perfil, estrato, num_dovelas=10)
    
    print(f"📊 ANÁLISIS DE LA PRIMERA DOVELA (la más problemática):")
    dovela = dovelas[0]  # La que causa más problemas
    
    print(f"\n📐 PROPIEDADES DE LA DOVELA:")
    print(f"   Posición X: {dovela.x_centro:.2f} m")
    print(f"   Ancho: {dovela.ancho:.2f} m") 
    print(f"   Altura: {dovela.altura:.2f} m")
    print(f"   Peso: {dovela.peso:.2f} kN")
    print(f"   Ángulo α: {math.degrees(dovela.angulo_alpha):.1f}°")
    print(f"   sin(α): {dovela.sin_alpha:.3f}")
    print(f"   cos(α): {dovela.cos_alpha:.3f}")
    print(f"   tan(φ): {dovela.tan_phi:.3f}")
    print(f"   Cohesión: {dovela.cohesion:.1f} kPa")
    print(f"   Longitud arco: {dovela.longitud_arco:.2f} m")
    
    print(f"\n⚖️ ANÁLISIS DE FUERZAS:")
    
    # Fuerza actuante
    fuerza_actuante = calcular_fuerza_actuante_bishop(dovela)
    print(f"   Fuerza actuante = W × sin(α) = {dovela.peso:.2f} × {dovela.sin_alpha:.3f} = {fuerza_actuante:.2f} kN")
    
    if fuerza_actuante < 0:
        print(f"   ⚠️ PROBLEMA: Fuerza actuante negativa indica movimiento hacia arriba")
        print(f"   ⚠️ CAUSA: sin(α) = {dovela.sin_alpha:.3f} < 0 porque α = {math.degrees(dovela.angulo_alpha):.1f}° < 0")
        print(f"   ⚠️ INTERPRETACIÓN: La dovela empuja hacia arriba en lugar de deslizar hacia abajo")
    
    # Análisis del factor mα
    print(f"\n🔢 ANÁLISIS DEL FACTOR mα:")
    factor_test = 1.0
    try:
        m_alpha = calcular_m_alpha(dovela, factor_test)
        print(f"   mα = cos(α) + sin(α)×tan(φ)/Fs")
        print(f"   mα = {dovela.cos_alpha:.3f} + {dovela.sin_alpha:.3f}×{dovela.tan_phi:.3f}/{factor_test}")
        print(f"   mα = {dovela.cos_alpha:.3f} + {dovela.sin_alpha * dovela.tan_phi / factor_test:.3f}")
        print(f"   mα = {m_alpha:.6f}")
        
        if m_alpha <= 0:
            print(f"   ❌ PROBLEMA: mα ≤ 0 hace que la fuerza resistente sea indefinida o negativa")
        else:
            print(f"   ✅ mα > 0: factor válido")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Análisis teórico
    print(f"\n📚 ANÁLISIS TEÓRICO:")
    print(f"   En el método de Bishop, α es el ángulo de la base de la dovela con la horizontal")
    print(f"   α > 0: base inclinada hacia abajo (lado derecho más bajo)")
    print(f"   α < 0: base inclinada hacia arriba (lado izquierdo más bajo)")
    print(f"   ")
    print(f"   Para una superficie de falla típica por deslizamiento:")
    print(f"   - Dovelas del lado izquierdo: α < 0 (empujan hacia arriba)")
    print(f"   - Dovelas del lado derecho: α > 0 (empujan hacia abajo)")
    print(f"   - La suma neta debe ser hacia abajo para que haya deslizamiento")
    
    # Análisis de toda la masa deslizante
    print(f"\n🌍 ANÁLISIS DE LA MASA TOTAL:")
    fuerzas_actuantes = [calcular_fuerza_actuante_bishop(d) for d in dovelas]
    suma_total = sum(fuerzas_actuantes)
    
    print(f"   Fuerzas por dovela:")
    for i, (d, f) in enumerate(zip(dovelas, fuerzas_actuantes)):
        signo = "↓" if f > 0 else "↑"
        print(f"      Dovela {i+1}: X={d.x_centro:.1f}, α={math.degrees(d.angulo_alpha):5.1f}°, F={f:7.1f}kN {signo}")
    
    print(f"   Suma total: {suma_total:.1f} kN")
    
    if suma_total < 0:
        print(f"   ❌ PROBLEMA: Suma negativa indica que la masa se mueve hacia arriba (imposible)")
        print(f"   🔍 CAUSA PROBABLE: Círculo mal posicionado genera más dovelas 'empujando hacia arriba'")
    else:
        print(f"   ✅ Suma positiva: masa se desliza hacia abajo (correcto)")

def investigar_geometrias_literatura():
    """
    Investiga geometrías de la literatura clásica que deberían funcionar.
    """
    print(f"\n" + "=" * 100)
    print("📖 INVESTIGACIÓN: GEOMETRÍAS DE LITERATURA CLÁSICA")
    print("=" * 100)
    
    # Caso Bishop 1955 clásico (aproximado)
    print(f"\n📚 CASO BISHOP 1955 (adaptado):")
    
    # Geometría típica de Bishop: talud 2:1 (26.57°)
    perfil_bishop = [
        (0, 20),    # Cresta del talud
        (5, 20),    # Terreno horizontal superior
        (25, 10),   # Pie del talud (pendiente 2:1)
        (40, 10)    # Terreno horizontal inferior
    ]
    
    # Círculo que corta el talud apropiadamente
    circulo_bishop = CirculoFalla(xc=15, yc=35, radio=30)
    estrato_bishop = Estrato(cohesion=20.0, phi_grados=25.0, gamma=19.0, nombre="Bishop1955")
    
    print(f"   Perfil: talud 2:1 con berma")
    print(f"   Círculo: centro=({circulo_bishop.xc}, {circulo_bishop.yc}), radio={circulo_bishop.radio}")
    
    try:
        dovelas_bishop = crear_dovelas(circulo_bishop, perfil_bishop, estrato_bishop, num_dovelas=8)
        
        fuerzas = [calcular_fuerza_actuante_bishop(d) for d in dovelas_bishop]
        suma = sum(fuerzas)
        
        print(f"   Dovelas generadas: {len(dovelas_bishop)}")
        print(f"   Rango de ángulos: {min([math.degrees(d.angulo_alpha) for d in dovelas_bishop]):.1f}° a {max([math.degrees(d.angulo_alpha) for d in dovelas_bishop]):.1f}°")
        print(f"   Suma de fuerzas actuantes: {suma:.1f} kN")
        
        if suma > 0:
            print(f"   ✅ GEOMETRÍA VIABLE: suma positiva")
            
            # Calcular factor de seguridad aproximado
            try:
                from core.bishop import analizar_bishop
                resultado = analizar_bishop(circulo_bishop, perfil_bishop, estrato_bishop, num_dovelas=8)
                print(f"   Factor de seguridad: {resultado.factor_seguridad:.3f}")
                print(f"   Convergió: {resultado.convergio}")
                
                if resultado.es_valido:
                    print(f"   ✅ ANÁLISIS EXITOSO: esta geometría funciona!")
                    return circulo_bishop, perfil_bishop, estrato_bishop
                    
            except Exception as e:
                print(f"   ⚠️ Error en análisis Bishop: {e}")
        else:
            print(f"   ❌ Suma negativa: geometría problemática")
            
    except Exception as e:
        print(f"   ❌ Error generando dovelas: {e}")
    
    return None, None, None

if __name__ == "__main__":
    debug_bishop_paso_a_paso()
    geometria_valida = investigar_geometrias_literatura()
    
    if geometria_valida[0] is not None:
        print(f"\n🎯 GEOMETRÍA VÁLIDA ENCONTRADA - se puede usar en evaluaciones")
    else:
        print(f"\n❌ No se encontró geometría válida - se necesita más investigación")
