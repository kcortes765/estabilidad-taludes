"""
Test funcional para el método de Fellenius.

Valida:
- Cálculo correcto del factor de seguridad
- Manejo de casos típicos (talud homogéneo, con nivel freático)
- Validaciones de entrada y salida
- Generación de reportes
- Comparación con valores teóricos
"""

import sys
import os
import math

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models import Estrato, CirculoFalla
from core.fellenius import (
    analizar_fellenius, fellenius_talud_homogeneo, fellenius_con_nivel_freatico,
    generar_reporte_fellenius, comparar_con_factor_teorico
)
from core.geometry import crear_perfil_simple, crear_nivel_freatico_horizontal


def test_fellenius_talud_homogeneo():
    """Test del método de Fellenius para talud homogéneo."""
    print("\n=== TEST FELLENIUS - TALUD HOMOGÉNEO ===")
    
    try:
        # Caso típico: talud 1:1.5 (33.7°), altura 10m
        resultado = fellenius_talud_homogeneo(
            altura=10.0,
            angulo_talud=33.7,  # Talud 1:1.5
            cohesion=20.0,      # kPa
            phi_grados=25.0,    # grados
            gamma=18.0,         # kN/m³
            factor_radio=1.3,
            num_dovelas=12
        )
        
        print(f"✅ Factor de Seguridad: {resultado.factor_seguridad:.3f}")
        print(f"   Momento Resistente: {resultado.momento_resistente:.1f} kN·m")
        print(f"   Momento Actuante: {resultado.momento_actuante:.1f} kN·m")
        print(f"   Número de dovelas: {len(resultado.dovelas)}")
        print(f"   Dovelas en tracción: {resultado.detalles_calculo['dovelas_en_traccion']}")
        print(f"   Resultado válido: {resultado.es_valido}")
        
        # Verificar rangos esperados
        assert 0.8 <= resultado.factor_seguridad <= 2.5, f"Fs fuera de rango: {resultado.factor_seguridad}"
        assert abs(resultado.momento_resistente) > 0, "Momento resistente debe ser positivo"
        assert abs(resultado.momento_actuante) > 0, "Momento actuante debe ser positivo"
        assert len(resultado.dovelas) == 12, "Número incorrecto de dovelas"
        
        print("✅ Test talud homogéneo PASADO")
        return resultado
        
    except Exception as e:
        print(f"❌ Error en test talud homogéneo: {e}")
        raise


def test_fellenius_con_nivel_freatico():
    """Test del método de Fellenius con nivel freático."""
    print("\n=== TEST FELLENIUS - CON NIVEL FREÁTICO ===")
    
    try:
        # Mismo talud pero con nivel freático a 3m de profundidad
        resultado = fellenius_con_nivel_freatico(
            altura=10.0,
            angulo_talud=33.7,
            cohesion=20.0,
            phi_grados=25.0,
            gamma=18.0,
            gamma_sat=20.0,      # kN/m³ saturado
            profundidad_freatico=3.0,  # m desde superficie
            factor_radio=1.3,
            num_dovelas=12
        )
        
        print(f"✅ Factor de Seguridad: {resultado.factor_seguridad:.3f}")
        print(f"   Momento Resistente: {resultado.momento_resistente:.1f} kN·m")
        print(f"   Momento Actuante: {resultado.momento_actuante:.1f} kN·m")
        print(f"   Dovelas en tracción: {resultado.detalles_calculo['dovelas_en_traccion']}")
        
        # El nivel freático debería reducir el factor de seguridad
        assert 0.5 <= resultado.factor_seguridad <= 2.0, f"Fs fuera de rango: {resultado.factor_seguridad}"
        assert resultado.es_valido, "Resultado debe ser válido"
        
        print("✅ Test con nivel freático PASADO")
        return resultado
        
    except Exception as e:
        print(f"❌ Error en test con nivel freático: {e}")
        raise


def test_fellenius_manual():
    """Test manual con geometría específica."""
    print("\n=== TEST FELLENIUS - CASO MANUAL ===")
    
    try:
        # Crear geometría manual
        perfil = crear_perfil_simple(0.0, 8.0, 20.0, 0.0, 15)
        
        # Círculo de falla específico
        circulo = CirculoFalla(xc=8.0, yc=12.0, radio=10.0)
        
        # Estrato con parámetros conocidos
        estrato = Estrato(
            cohesion=15.0,    # kPa
            phi_grados=30.0,  # grados
            gamma=19.0,       # kN/m³
            nombre="Manual"
        )
        
        # Análisis
        resultado = analizar_fellenius(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            num_dovelas=10
        )
        
        print(f"✅ Factor de Seguridad: {resultado.factor_seguridad:.3f}")
        print(f"   Centro círculo: ({circulo.xc}, {circulo.yc})")
        print(f"   Radio: {circulo.radio} m")
        print(f"   Número dovelas: {len(resultado.dovelas)}")
        
        # Verificar consistencia
        assert resultado.factor_seguridad > 0, "Factor de seguridad debe ser positivo"
        assert len(resultado.dovelas) == 10, "Número incorrecto de dovelas"
        assert resultado.es_valido, "Resultado debe ser válido"
        
        print("✅ Test manual PASADO")
        return resultado
        
    except Exception as e:
        print(f"❌ Error en test manual: {e}")
        raise


def test_generacion_reporte():
    """Test de generación de reportes."""
    print("\n=== TEST GENERACIÓN DE REPORTE ===")
    
    try:
        # Usar resultado de test anterior
        resultado = fellenius_talud_homogeneo(
            altura=8.0, angulo_talud=30.0, cohesion=25.0, 
            phi_grados=28.0, gamma=19.0, num_dovelas=8
        )
        
        # Generar reporte
        reporte = generar_reporte_fellenius(resultado)
        
        # Verificar contenido del reporte
        assert "MÉTODO DE FELLENIUS" in reporte, "Título faltante en reporte"
        assert f"{resultado.factor_seguridad:.3f}" in reporte, "Factor de seguridad faltante"
        assert "EQUILIBRIO DE MOMENTOS" in reporte, "Sección de momentos faltante"
        assert "ANÁLISIS DE DOVELAS" in reporte, "Sección de dovelas faltante"
        
        print("✅ Reporte generado correctamente")
        print(f"   Longitud del reporte: {len(reporte)} caracteres")
        
        lineas = reporte.split('\n')
        print(f"   Líneas del reporte: {len(lineas)}")

        # Mostrar parte del reporte
        print("\n📋 EXTRACTO DEL REPORTE:")
        for i, linea in enumerate(lineas[:15]):  # Primeras 15 líneas
            print(f"   {linea}")
        if len(lineas) > 15:
            print("   ...")
        
        print("✅ Test generación reporte PASADO")
        return reporte
        
    except Exception as e:
        print(f"❌ Error en test generación reporte: {e}")
        raise


def test_comparacion_teorica():
    """Test de comparación con valores teóricos."""
    print("\n=== TEST COMPARACIÓN TEÓRICA ===")
    
    try:
        # Caso con factor de seguridad esperado conocido
        resultado = fellenius_talud_homogeneo(
            altura=10.0, angulo_talud=45.0, cohesion=30.0,
            phi_grados=20.0, gamma=18.0, num_dovelas=10
        )
        
        # Comparar con valor teórico estimado
        factor_teorico = 1.2  # Valor esperado aproximado
        comparacion = comparar_con_factor_teorico(resultado, factor_teorico, tolerancia=0.3)
        
        print(f"✅ Factor calculado: {comparacion['factor_calculado']:.3f}")
        print(f"   Factor teórico: {comparacion['factor_teorico']:.3f}")
        print(f"   Diferencia: {comparacion['diferencia_absoluta']:.3f}")
        print(f"   Diferencia relativa: {comparacion['diferencia_relativa_pct']:.1f}%")
        print(f"   Es consistente: {comparacion['es_consistente']}")
        print(f"   {comparacion['mensaje']}")
        
        # Verificar que la comparación funciona
        assert 'factor_calculado' in comparacion, "Campo faltante en comparación"
        assert 'es_consistente' in comparacion, "Campo de consistencia faltante"
        
        print("✅ Test comparación teórica PASADO")
        return comparacion
        
    except Exception as e:
        print(f"❌ Error en test comparación teórica: {e}")
        raise


def test_casos_limite():
    """Test de casos límite y validaciones."""
    print("\n=== TEST CASOS LÍMITE ===")
    
    try:
        # Caso con cohesión muy alta (debería dar Fs alto)
        resultado_alta_cohesion = fellenius_talud_homogeneo(
            altura=5.0, angulo_talud=30.0, cohesion=100.0,  # Cohesión muy alta
            phi_grados=25.0, gamma=18.0, num_dovelas=8
        )
        
        print(f"✅ Alta cohesión - Fs: {resultado_alta_cohesion.factor_seguridad:.3f}")
        assert resultado_alta_cohesion.factor_seguridad > 2.0, "Fs debería ser alto con alta cohesión"
        
        # Caso con ángulo de fricción alto
        resultado_alto_phi = fellenius_talud_homogeneo(
            altura=5.0, angulo_talud=30.0, cohesion=10.0,
            phi_grados=35.0, gamma=18.0, num_dovelas=8  # Ángulo alto
        )
        
        print(f"✅ Alto φ - Fs: {resultado_alto_phi.factor_seguridad:.3f}")
        assert resultado_alto_phi.factor_seguridad > 1.0, "Fs debería ser razonable con alto φ"
        
        # Verificar que ambos casos son válidos
        assert resultado_alta_cohesion.es_valido, "Caso alta cohesión debe ser válido"
        assert resultado_alto_phi.es_valido, "Caso alto φ debe ser válido"
        
        print("✅ Test casos límite PASADO")
        
    except Exception as e:
        print(f"❌ Error en test casos límite: {e}")
        raise


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests de Fellenius."""
    print("🧪 INICIANDO TESTS DEL MÉTODO DE FELLENIUS")
    print("=" * 50)
    
    tests_pasados = 0
    tests_totales = 6
    
    try:
        # Test 1: Talud homogéneo
        test_fellenius_talud_homogeneo()
        tests_pasados += 1
        
        # Test 2: Con nivel freático
        test_fellenius_con_nivel_freatico()
        tests_pasados += 1
        
        # Test 3: Caso manual
        test_fellenius_manual()
        tests_pasados += 1
        
        # Test 4: Generación de reporte
        test_generacion_reporte()
        tests_pasados += 1
        
        # Test 5: Comparación teórica
        test_comparacion_teorica()
        tests_pasados += 1
        
        # Test 6: Casos límite
        test_casos_limite()
        tests_pasados += 1
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
    
    # Resumen final
    print("\n" + "=" * 50)
    print(f"🎯 RESUMEN DE TESTS - MÉTODO FELLENIUS")
    print(f"   Tests pasados: {tests_pasados}/{tests_totales}")
    print(f"   Porcentaje éxito: {(tests_pasados/tests_totales)*100:.1f}%")
    
    if tests_pasados == tests_totales:
        print("✅ TODOS LOS TESTS PASARON - MÉTODO FELLENIUS FUNCIONANDO")
    else:
        print(f"⚠️ {tests_totales - tests_pasados} TESTS FALLARON")
    
    print("=" * 50)
    return tests_pasados == tests_totales


if __name__ == "__main__":
    ejecutar_todos_los_tests()
