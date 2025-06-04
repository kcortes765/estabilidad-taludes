"""
Test funcional para las clases base del sistema de estabilidad de taludes.

Este test valida que las clases Estrato, Dovela y CirculoFalla funcionen
correctamente con parámetros típicos de ingeniería geotécnica.
"""

import sys
import os
import math

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models import Estrato, Dovela, CirculoFalla, crear_estrato_homogeneo, crear_circulo_simple


def test_estrato_basico():
    """Test básico de la clase Estrato."""
    print("=== TEST ESTRATO BÁSICO ===")
    
    # Crear estrato típico de arcilla
    estrato = Estrato(
        cohesion=10.0,      # kPa
        phi_grados=25.0,    # grados
        gamma=18.0,         # kN/m³
        nombre="Arcilla"
    )
    
    print(f"Estrato: {estrato.nombre}")
    print(f"Cohesión: {estrato.cohesion} kPa")
    print(f"Ángulo de fricción: {estrato.phi_grados}° = {estrato.phi_radianes:.3f} rad")
    print(f"tan(φ): {estrato.tan_phi:.3f}")
    print(f"Peso específico: {estrato.gamma} kN/m³")
    
    # Validaciones
    assert estrato.cohesion == 10.0
    assert estrato.phi_grados == 25.0
    assert abs(estrato.phi_radianes - math.radians(25.0)) < 0.001
    assert abs(estrato.tan_phi - math.tan(math.radians(25.0))) < 0.001
    
    print("✅ Test estrato básico PASADO\n")


def test_estrato_con_validaciones():
    """Test de validaciones del estrato."""
    print("=== TEST VALIDACIONES ESTRATO ===")
    
    # Test valores válidos
    try:
        estrato_valido = Estrato(cohesion=0, phi_grados=0, gamma=16.0)
        print("✅ Estrato con valores límite válidos")
    except ValueError as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    # Test cohesión negativa
    try:
        Estrato(cohesion=-5, phi_grados=30, gamma=18)
        print("❌ Debería fallar con cohesión negativa")
        return False
    except ValueError:
        print("✅ Validación cohesión negativa correcta")
    
    # Test ángulo de fricción inválido
    try:
        Estrato(cohesion=10, phi_grados=50, gamma=18)
        print("❌ Debería fallar con φ > 45°")
        return False
    except ValueError:
        print("✅ Validación ángulo de fricción correcta")
    
    # Test peso específico inválido
    try:
        Estrato(cohesion=10, phi_grados=30, gamma=0)
        print("❌ Debería fallar con γ = 0")
        return False
    except ValueError:
        print("✅ Validación peso específico correcta")
    
    print("✅ Test validaciones estrato PASADO\n")
    return True


def test_dovela_basica():
    """Test básico de la clase Dovela."""
    print("=== TEST DOVELA BÁSICA ===")
    
    # Crear dovela típica
    dovela = Dovela(
        x_centro=5.0,           # m
        ancho=1.0,              # m
        altura=3.0,             # m
        angulo_alpha=math.radians(30),  # 30° en radianes
        cohesion=10.0,          # kPa
        phi_grados=25.0,        # grados
        gamma=18.0,             # kN/m³
        peso=54.0,              # W = γ * V = 18 * 1 * 3 = 54 kN
        presion_poros=0.0,      # kPa (sin agua)
        longitud_arco=1.15      # m (aproximado)
    )
    
    print(f"Dovela en x = {dovela.x_centro} m")
    print(f"Dimensiones: {dovela.ancho} × {dovela.altura} m")
    print(f"Ángulo α: {math.degrees(dovela.angulo_alpha):.1f}°")
    print(f"Peso: {dovela.peso} kN")
    print(f"sin(α): {dovela.sin_alpha:.3f}")
    print(f"cos(α): {dovela.cos_alpha:.3f}")
    print(f"tan(φ): {dovela.tan_phi:.3f}")
    
    # Calcular fuerza normal efectiva
    fuerza_normal = dovela.calcular_fuerza_normal_efectiva()
    print(f"Fuerza normal efectiva: {fuerza_normal:.1f} kN")
    print(f"¿En tracción?: {dovela.tiene_traccion}")
    
    # Calcular resistencia y fuerza actuante (Fellenius)
    resistencia = dovela.calcular_resistencia_fellenius()
    fuerza_actuante = dovela.calcular_fuerza_actuante_fellenius()
    
    print(f"Resistencia (Fellenius): {resistencia:.1f} kN")
    print(f"Fuerza actuante (Fellenius): {fuerza_actuante:.1f} kN")
    
    # Validaciones básicas
    assert dovela.peso > 0
    assert not dovela.tiene_traccion  # Sin agua, no debería haber tracción
    assert resistencia > 0
    assert fuerza_actuante > 0
    
    print("✅ Test dovela básica PASADO\n")


def test_dovela_con_traccion():
    """Test de dovela en tracción."""
    print("=== TEST DOVELA CON TRACCIÓN ===")
    
    # Crear dovela con alta presión de poros
    dovela = Dovela(
        x_centro=5.0,
        ancho=1.0,
        altura=2.0,
        angulo_alpha=math.radians(45),  # 45°
        cohesion=5.0,
        phi_grados=20.0,
        gamma=16.0,
        peso=32.0,              # W = 16 * 1 * 2 = 32 kN
        presion_poros=50.0,     # kPa (alta presión)
        longitud_arco=1.41      # m
    )
    
    fuerza_normal = dovela.calcular_fuerza_normal_efectiva()
    resistencia = dovela.calcular_resistencia_fellenius()
    
    print(f"Fuerza normal efectiva: {fuerza_normal:.1f} kN")
    print(f"¿En tracción?: {dovela.tiene_traccion}")
    print(f"Resistencia (solo cohesión): {resistencia:.1f} kN")
    
    # En tracción, solo debe actuar la cohesión
    resistencia_esperada = dovela.cohesion * dovela.longitud_arco
    print(f"Resistencia esperada: {resistencia_esperada:.1f} kN")
    
    assert dovela.tiene_traccion
    assert abs(resistencia - resistencia_esperada) < 0.1
    
    print("✅ Test dovela con tracción PASADO\n")


def test_circulo_falla():
    """Test básico de CirculoFalla."""
    print("=== TEST CÍRCULO DE FALLA ===")
    
    # Crear círculo
    circulo = CirculoFalla(xc=10.0, yc=8.0, radio=6.0)
    
    print(f"Centro: ({circulo.xc}, {circulo.yc}) m")
    print(f"Radio: {circulo.radio} m")
    print(f"Número de dovelas inicial: {circulo.num_dovelas}")
    
    # Agregar algunas dovelas
    for i in range(3):
        dovela = Dovela(
            x_centro=8.0 + i * 1.5,
            ancho=1.5,
            altura=3.0 - i * 0.5,
            angulo_alpha=math.radians(20 + i * 10),
            cohesion=10.0,
            phi_grados=25.0,
            gamma=18.0,
            peso=(3.0 - i * 0.5) * 1.5 * 18.0,
            presion_poros=0.0,
            longitud_arco=1.6
        )
        circulo.agregar_dovela(dovela)
    
    print(f"Dovelas agregadas: {circulo.num_dovelas}")
    print(f"Peso total: {circulo.peso_total:.1f} kN")
    print(f"Longitud total arco: {circulo.longitud_total_arco:.1f} m")
    
    # Validar geometría
    es_valido = circulo.validar_geometria()
    print(f"¿Geometría válida?: {es_valido}")
    
    # Calcular fuerzas normales
    circulo.calcular_fuerzas_normales_efectivas()
    print(f"¿Hay dovelas en tracción?: {circulo.tiene_dovelas_en_traccion()}")
    
    # Mostrar resumen
    print("\n" + circulo.resumen())
    
    assert circulo.num_dovelas == 3
    assert circulo.peso_total > 0
    assert es_valido
    
    print("\n✅ Test círculo de falla PASADO\n")


def test_funciones_auxiliares():
    """Test de funciones auxiliares."""
    print("=== TEST FUNCIONES AUXILIARES ===")
    
    # Test crear_estrato_homogeneo
    estrato = crear_estrato_homogeneo(15.0, 30.0, 19.0, "Arena")
    print(f"Estrato creado: {estrato.nombre}")
    print(f"Parámetros: c'={estrato.cohesion}, φ={estrato.phi_grados}°, γ={estrato.gamma}")
    
    # Test crear_circulo_simple
    circulo = crear_circulo_simple(12.0, 10.0, 8.0)
    print(f"Círculo creado: centro=({circulo.xc}, {circulo.yc}), radio={circulo.radio}")
    
    assert estrato.nombre == "Arena"
    assert circulo.radio == 8.0
    
    print("✅ Test funciones auxiliares PASADO\n")


def main():
    """Ejecuta todos los tests."""
    print("🧪 INICIANDO TESTS DE MODELOS BASE")
    print("=" * 50)
    
    try:
        test_estrato_basico()
        if not test_estrato_con_validaciones():
            return False
        test_dovela_basica()
        test_dovela_con_traccion()
        test_circulo_falla()
        test_funciones_auxiliares()
        
        print("🎉 TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("✅ Las clases base están funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ ERROR EN TESTS: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
