"""
Test funcional para el módulo core.geometry

Valida todas las funciones geométricas fundamentales:
- Cálculos de círculos
- Interpolación de terreno
- Creación de dovelas
- Validaciones geométricas
"""

import math
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.geometry import (
    calcular_y_circulo, interpolar_terreno, calcular_angulo_alpha,
    calcular_longitud_arco, calcular_altura_dovela, calcular_peso_dovela,
    calcular_presion_poros, crear_dovelas, validar_geometria_circulo,
    crear_perfil_simple, crear_nivel_freatico_horizontal
)
from data.models import CirculoFalla, Estrato


def test_calcular_y_circulo():
    """Test para cálculo de intersección círculo-vertical"""
    print("=== TEST CÁLCULO Y CÍRCULO ===")
    
    # Círculo centrado en (5, 10) con radio 3
    xc, yc, radio = 5.0, 10.0, 3.0
    
    # Punto en el centro (x = xc)
    y_superior = calcular_y_circulo(5.0, xc, yc, radio, True)
    y_inferior = calcular_y_circulo(5.0, xc, yc, radio, False)
    
    print(f"Círculo: centro=({xc}, {yc}), radio={radio}")
    print(f"En x=5.0: y_superior={y_superior:.2f}, y_inferior={y_inferior:.2f}")
    
    assert abs(y_superior - 13.0) < 0.01, f"Y superior esperado 13.0, obtenido {y_superior}"
    assert abs(y_inferior - 7.0) < 0.01, f"Y inferior esperado 7.0, obtenido {y_inferior}"
    
    # Punto en el borde (x = xc + radio)
    y_borde = calcular_y_circulo(8.0, xc, yc, radio, True)
    print(f"En x=8.0 (borde): y={y_borde:.2f}")
    assert abs(y_borde - 10.0) < 0.01, f"Y en borde esperado 10.0, obtenido {y_borde}"
    
    # Punto fuera del círculo
    y_fuera = calcular_y_circulo(10.0, xc, yc, radio, True)
    print(f"En x=10.0 (fuera): y={y_fuera}")
    assert y_fuera is None, "Punto fuera del círculo debe retornar None"
    
    print("✅ Test cálculo Y círculo PASADO\n")


def test_interpolar_terreno():
    """Test para interpolación de terreno"""
    print("=== TEST INTERPOLACIÓN TERRENO ===")
    
    # Perfil simple: pendiente de 1:2 (1 vertical, 2 horizontal)
    perfil = [(0.0, 10.0), (10.0, 5.0), (20.0, 0.0)]
    
    print("Perfil de terreno:")
    for x, y in perfil:
        print(f"  ({x:.1f}, {y:.1f})")
    
    # Test interpolación en puntos conocidos
    y_0 = interpolar_terreno(0.0, perfil)
    y_10 = interpolar_terreno(10.0, perfil)
    y_20 = interpolar_terreno(20.0, perfil)
    
    print(f"Interpolación en puntos conocidos:")
    print(f"  x=0.0 → y={y_0:.2f} (esperado 10.0)")
    print(f"  x=10.0 → y={y_10:.2f} (esperado 5.0)")
    print(f"  x=20.0 → y={y_20:.2f} (esperado 0.0)")
    
    assert abs(y_0 - 10.0) < 0.01
    assert abs(y_10 - 5.0) < 0.01
    assert abs(y_20 - 0.0) < 0.01
    
    # Test interpolación en punto medio
    y_5 = interpolar_terreno(5.0, perfil)
    y_15 = interpolar_terreno(15.0, perfil)
    
    print(f"Interpolación en puntos medios:")
    print(f"  x=5.0 → y={y_5:.2f} (esperado 7.5)")
    print(f"  x=15.0 → y={y_15:.2f} (esperado 2.5)")
    
    assert abs(y_5 - 7.5) < 0.01
    assert abs(y_15 - 2.5) < 0.01
    
    print("✅ Test interpolación terreno PASADO\n")


def test_calcular_angulo_alpha():
    """Test para cálculo de ángulo alpha"""
    print("=== TEST ÁNGULO ALPHA ===")
    
    # Círculo centrado en (10, 8) con radio 6
    xc, yc, radio = 10.0, 8.0, 6.0
    
    print(f"Círculo: centro=({xc}, {yc}), radio={radio}")
    
    # Punto en el centro del círculo (α = 0)
    alpha_centro = calcular_angulo_alpha(10.0, xc, yc, radio)
    print(f"En x=10.0 (centro): α={alpha_centro:.3f} rad = {math.degrees(alpha_centro):.1f}°")
    assert abs(alpha_centro) < 0.01, f"Ángulo en centro esperado 0, obtenido {alpha_centro}"
    
    # Punto a la derecha (α positivo)
    alpha_derecha = calcular_angulo_alpha(13.0, xc, yc, radio)
    print(f"En x=13.0: α={alpha_derecha:.3f} rad = {math.degrees(alpha_derecha):.1f}°")
    assert alpha_derecha > 0, "Ángulo a la derecha debe ser positivo"
    
    # Punto a la izquierda (α negativo)
    alpha_izquierda = calcular_angulo_alpha(7.0, xc, yc, radio)
    print(f"En x=7.0: α={alpha_izquierda:.3f} rad = {math.degrees(alpha_izquierda):.1f}°")
    assert alpha_izquierda < 0, "Ángulo a la izquierda debe ser negativo"
    
    print("✅ Test ángulo alpha PASADO\n")


def test_crear_perfil_simple():
    """Test para creación de perfil simple"""
    print("=== TEST PERFIL SIMPLE ===")
    
    perfil = crear_perfil_simple(0.0, 10.0, 20.0, 0.0, 5)
    
    print("Perfil creado:")
    for i, (x, y) in enumerate(perfil):
        print(f"  Punto {i}: ({x:.1f}, {y:.1f})")
    
    assert len(perfil) == 5, f"Esperado 5 puntos, obtenido {len(perfil)}"
    assert perfil[0] == (0.0, 10.0), f"Primer punto incorrecto: {perfil[0]}"
    assert perfil[-1] == (20.0, 0.0), f"Último punto incorrecto: {perfil[-1]}"
    
    print("✅ Test perfil simple PASADO\n")


def test_crear_dovelas():
    """Test para creación de dovelas"""
    print("=== TEST CREACIÓN DOVELAS ===")
    
    # Crear círculo de falla
    circulo = CirculoFalla(xc=10.0, yc=8.0, radio=6.0)
    
    # Crear perfil de terreno simple
    perfil = crear_perfil_simple(0.0, 10.0, 20.0, 0.0, 10)
    
    # Crear estrato
    estrato = Estrato(nombre="Arena", cohesion=5.0, phi_grados=30.0, gamma=18.0)
    
    print(f"Círculo: centro=({circulo.xc}, {circulo.yc}), radio={circulo.radio}")
    print(f"Estrato: {estrato.nombre}, c'={estrato.cohesion}, φ={estrato.phi_grados}°, γ={estrato.gamma}")
    
    # Crear dovelas
    dovelas = crear_dovelas(circulo, perfil, estrato, num_dovelas=5)
    
    print(f"\nDovelas creadas: {len(dovelas)}")
    
    peso_total = 0.0
    for i, dovela in enumerate(dovelas):
        print(f"Dovela {i+1}:")
        print(f"  x_centro: {dovela.x_centro:.2f} m")
        print(f"  ancho: {dovela.ancho:.2f} m")
        print(f"  altura: {dovela.altura:.2f} m")
        print(f"  α: {math.degrees(dovela.angulo_alpha):.1f}°")
        print(f"  peso: {dovela.peso:.1f} kN")
        peso_total += dovela.peso
    
    print(f"\nPeso total de dovelas: {peso_total:.1f} kN")
    
    assert len(dovelas) > 0, "Debe crear al menos una dovela"
    assert all(d.peso > 0 for d in dovelas), "Todas las dovelas deben tener peso positivo"
    assert all(d.altura > 0 for d in dovelas), "Todas las dovelas deben tener altura positiva"
    
    print("✅ Test creación dovelas PASADO\n")


def test_validar_geometria():
    """Test para validación de geometría"""
    print("=== TEST VALIDACIÓN GEOMETRÍA ===")
    
    perfil = crear_perfil_simple(0.0, 10.0, 20.0, 0.0, 10)
    
    # Círculo válido
    circulo_valido = CirculoFalla(xc=10.0, yc=8.0, radio=6.0)
    es_valido = validar_geometria_circulo(circulo_valido, perfil)
    print(f"Círculo válido: centro=({circulo_valido.xc}, {circulo_valido.yc}), radio={circulo_valido.radio}")
    print(f"¿Es válido?: {es_valido}")
    assert es_valido, "Círculo válido debe pasar la validación"
    
    # Círculo muy alto (centro muy arriba)
    circulo_alto = CirculoFalla(xc=10.0, yc=50.0, radio=6.0)
    es_valido_alto = validar_geometria_circulo(circulo_alto, perfil)
    print(f"\nCírculo muy alto: centro=({circulo_alto.xc}, {circulo_alto.yc}), radio={circulo_alto.radio}")
    print(f"¿Es válido?: {es_valido_alto}")
    
    # Círculo fuera del rango
    circulo_fuera = CirculoFalla(xc=50.0, yc=8.0, radio=6.0)
    es_valido_fuera = validar_geometria_circulo(circulo_fuera, perfil)
    print(f"\nCírculo fuera de rango: centro=({circulo_fuera.xc}, {circulo_fuera.yc}), radio={circulo_fuera.radio}")
    print(f"¿Es válido?: {es_valido_fuera}")
    assert not es_valido_fuera, "Círculo fuera de rango no debe ser válido"
    
    print("✅ Test validación geometría PASADO\n")


def test_presion_poros():
    """Test para cálculo de presión de poros"""
    print("=== TEST PRESIÓN DE POROS ===")
    
    # Perfil de terreno
    perfil = [(0.0, 10.0), (20.0, 0.0)]
    
    # Nivel freático horizontal a 3 metros de altura
    nivel_freatico = crear_nivel_freatico_horizontal(0.0, 20.0, 3.0, 5)
    
    print("Nivel freático:")
    for x, y in nivel_freatico:
        print(f"  ({x:.1f}, {y:.1f})")
    
    # Calcular presión en diferentes puntos
    x_test = 10.0
    altura_dovela = 4.0
    
    presion = calcular_presion_poros(x_test, altura_dovela, perfil, nivel_freatico)
    
    print(f"\nEn x={x_test}:")
    y_terreno = interpolar_terreno(x_test, perfil)
    y_base = y_terreno - altura_dovela
    print(f"  Elevación terreno: {y_terreno:.1f} m")
    print(f"  Elevación base dovela: {y_base:.1f} m")
    print(f"  Elevación nivel freático: 3.0 m")
    print(f"  Presión de poros: {presion:.1f} kPa")
    
    # Sin nivel freático
    presion_sin_agua = calcular_presion_poros(x_test, altura_dovela, perfil, None)
    print(f"  Presión sin agua: {presion_sin_agua:.1f} kPa")
    
    assert presion_sin_agua == 0.0, "Sin nivel freático, presión debe ser 0"
    assert presion >= 0.0, "Presión de poros no puede ser negativa"
    
    print("✅ Test presión de poros PASADO\n")


def main():
    """Ejecutar todos los tests"""
    print("🧪 INICIANDO TESTS DE GEOMETRÍA")
    print("=" * 50)
    
    try:
        test_calcular_y_circulo()
        test_interpolar_terreno()
        test_calcular_angulo_alpha()
        test_crear_perfil_simple()
        test_crear_dovelas()
        test_validar_geometria()
        test_presion_poros()
        
        print("🎉 TODOS LOS TESTS DE GEOMETRÍA PASARON EXITOSAMENTE")
        print("✅ Las funciones geométricas están funcionando correctamente")
        
    except Exception as e:
        print(f"❌ ERROR EN TESTS: {e}")
        raise


if __name__ == "__main__":
    main()
