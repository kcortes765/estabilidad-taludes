"""
Test simple del método de Fellenius para verificar funcionamiento básico.
"""

import sys
import os
import math

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple
from core.fellenius import analizar_fellenius


def test_fellenius_basico():
    """Test básico del método de Fellenius."""
    print("🧪 TEST BÁSICO FELLENIUS")
    print("=" * 40)
    
    try:
        # Crear geometría simple
        perfil = [(0, 0), (5, 5), (10, 5), (15, 0)]
        
        # Círculo de falla
        circulo = CirculoFalla(xc=7.5, yc=8.0, radio=6.0)
        
        # Estrato simple
        estrato = Estrato(
            cohesion=20.0,
            phi_grados=25.0,
            gamma=18.0,
            nombre="Test"
        )
        
        print("📋 Datos de entrada:")
        print(f"   Perfil: {len(perfil)} puntos")
        print(f"   Círculo: centro=({circulo.xc}, {circulo.yc}), radio={circulo.radio}")
        print(f"   Suelo: c={estrato.cohesion} kPa, φ={estrato.phi_grados}°, γ={estrato.gamma} kN/m³")
        
        # Análisis sin validaciones estrictas
        resultado = analizar_fellenius(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            num_dovelas=8,
            validar_entrada=False  # Desactivar validaciones estrictas
        )
        
        print(f"\n✅ RESULTADOS:")
        print(f"   Factor de Seguridad: {resultado.factor_seguridad:.3f}")
        print(f"   Momento Resistente: {resultado.momento_resistente:.1f} kN·m")
        print(f"   Momento Actuante: {resultado.momento_actuante:.1f} kN·m")
        print(f"   Número de dovelas: {len(resultado.dovelas)}")
        print(f"   Es válido: {resultado.es_valido}")
        
        if resultado.advertencias:
            print(f"   Advertencias: {len(resultado.advertencias)}")
            for adv in resultado.advertencias[:3]:  # Mostrar solo las primeras 3
                print(f"     • {adv}")
        
        # Verificaciones básicas
        assert resultado.factor_seguridad > 0, "Factor de seguridad debe ser positivo"
        assert resultado.momento_resistente > 0, "Momento resistente debe ser positivo"
        assert resultado.momento_actuante > 0, "Momento actuante debe ser positivo"
        assert len(resultado.dovelas) == 8, "Número incorrecto de dovelas"
        
        print("\n✅ TEST BÁSICO PASADO")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fellenius_simple_homogeneo():
    """Test con función auxiliar para talud homogéneo."""
    print("\n🏔️ TEST TALUD HOMOGÉNEO SIMPLE")
    print("=" * 40)
    
    try:
        from core.fellenius import fellenius_talud_homogeneo
        
        # Parámetros simples
        altura = 8.0
        angulo = 30.0
        cohesion = 15.0
        phi = 20.0
        gamma = 18.0
        
        print("📋 Parámetros:")
        print(f"   Altura: {altura} m")
        print(f"   Ángulo talud: {angulo}°")
        print(f"   Cohesión: {cohesion} kPa")
        print(f"   Fricción: {phi}°")
        print(f"   Peso específico: {gamma} kN/m³")
        
        resultado = fellenius_talud_homogeneo(
            altura=altura,
            angulo_talud=angulo,
            cohesion=cohesion,
            phi_grados=phi,
            gamma=gamma,
            factor_radio=1.3,
            num_dovelas=10
        )
        
        print(f"\n✅ RESULTADOS:")
        print(f"   Factor de Seguridad: {resultado.factor_seguridad:.3f}")
        print(f"   Número de dovelas: {len(resultado.dovelas)}")
        print(f"   Dovelas en tracción: {resultado.detalles_calculo.get('dovelas_en_traccion', 0)}")
        print(f"   Es válido: {resultado.es_valido}")
        
        # Clasificación simple
        if resultado.factor_seguridad < 1.0:
            print("   🔴 INESTABLE")
        elif resultado.factor_seguridad < 1.2:
            print("   🟡 MARGINAL")
        elif resultado.factor_seguridad < 1.5:
            print("   🟢 ESTABLE")
        else:
            print("   🔵 MUY ESTABLE")
        
        assert 0.5 <= resultado.factor_seguridad <= 3.0, f"Fs fuera de rango razonable: {resultado.factor_seguridad}"
        
        print("\n✅ TEST HOMOGÉNEO PASADO")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecutar tests simples."""
    print("🧪 TESTS SIMPLES - MÉTODO DE FELLENIUS")
    print("=" * 50)
    
    tests_pasados = 0
    tests_totales = 2
    
    # Test 1: Básico
    if test_fellenius_basico():
        tests_pasados += 1
    
    # Test 2: Homogéneo
    if test_fellenius_simple_homogeneo():
        tests_pasados += 1
    
    # Resumen
    print("\n" + "=" * 50)
    print(f"🎯 RESUMEN: {tests_pasados}/{tests_totales} tests pasaron")
    
    if tests_pasados == tests_totales:
        print("✅ MÉTODO DE FELLENIUS FUNCIONANDO CORRECTAMENTE")
    else:
        print("⚠️ ALGUNOS TESTS FALLARON")
    
    print("=" * 50)
    return tests_pasados == tests_totales


if __name__ == "__main__":
    main()
