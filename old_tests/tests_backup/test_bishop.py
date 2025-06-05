"""
Test funcional completo para el método de Bishop Modificado.

Este test valida:
1. Análisis básico de Bishop con convergencia
2. Análisis con nivel freático
3. Comparación con Fellenius
4. Generación de reportes
5. Casos límite y validaciones
6. Funciones auxiliares
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from data.models import Estrato, CirculoFalla
from core.bishop import (
    analizar_bishop, ResultadoBishop, generar_reporte_bishop,
    bishop_talud_homogeneo, bishop_con_nivel_freatico,
    comparar_bishop_fellenius, generar_reporte_comparacion,
    calcular_m_alpha
)
from core.geometry import crear_perfil_simple, crear_nivel_freatico_horizontal
from data.validation import ValidacionError


def test_bishop_basico():
    """Test básico del método de Bishop con talud homogéneo."""
    print("=== TEST 1: Análisis básico de Bishop ===")
    
    # Talud de carretera típico
    altura = 12.0
    angulo_talud = 45.0
    
    # Crear geometría con extensión adecuada
    longitud_base = altura / math.tan(math.radians(angulo_talud))
    perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
    
    # Círculo de falla más realista
    radio = 18.0
    xc = longitud_base * 0.3  # Centro más hacia atrás
    yc = altura * 1.1  # Centro más alto
    circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
    
    # Suelo arcilloso
    estrato = Estrato(cohesion=25.0, phi_grados=20.0, gamma=18.0, nombre="Arcilla")
    
    # Análisis
    resultado = analizar_bishop(circulo, perfil, estrato, num_dovelas=10, factor_inicial=1.2)
    
    # Verificaciones
    assert resultado.convergio, "Bishop debe converger"
    assert 0.8 <= resultado.factor_seguridad <= 5.0, f"Fs fuera de rango: {resultado.factor_seguridad}"
    assert resultado.iteraciones <= 50, f"Demasiadas iteraciones: {resultado.iteraciones}"
    assert resultado.es_valido, "Resultado debe ser válido"
    assert len(resultado.dovelas) >= 5, f"Debe tener al menos 5 dovelas, tiene {len(resultado.dovelas)}"
    assert len(resultado.fuerzas_resistentes) == len(resultado.dovelas), "Fuerzas resistentes deben coincidir con dovelas"
    assert len(resultado.factores_m_alpha) == len(resultado.dovelas), "Factores mα deben coincidir con dovelas"
    
    # Verificar que todos los mα son positivos
    for i, m_alpha in enumerate(resultado.factores_m_alpha):
        assert m_alpha > 0, f"mα debe ser > 0 en dovela {i}: {m_alpha}"
    
    # Verificar convergencia
    assert abs(resultado.historial_fs[-1] - resultado.historial_fs[-2]) < 0.001, "Debe haber convergido"
    
    print(f"✅ Factor de seguridad: {resultado.factor_seguridad:.3f}")
    print(f"✅ Iteraciones: {resultado.iteraciones}")
    print(f"✅ Dovelas en tracción: {resultado.detalles_calculo['dovelas_en_traccion']}")
    print(f"✅ Momento resistente: {resultado.momento_resistente:.1f} kN·m")
    print(f"✅ Momento actuante: {resultado.momento_actuante:.1f} kN·m")


def test_bishop_con_nivel_freatico():
    """Test de Bishop con nivel freático."""
    print("\n=== TEST 2: Bishop con nivel freático ===")
    
    # Usar función auxiliar
    resultado_seco = bishop_talud_homogeneo(
        altura=15.0,
        angulo_talud=35.0,
        cohesion=30.0,
        phi_grados=25.0,
        gamma=19.0,
        num_dovelas=12
    )
    
    resultado_con_agua = bishop_con_nivel_freatico(
        altura=15.0,
        angulo_talud=35.0,
        cohesion=30.0,
        phi_grados=25.0,
        gamma=19.0,
        altura_nivel_freatico=8.0,  # Nivel freático a 8m
        num_dovelas=12
    )
    
    # Verificaciones
    assert resultado_seco.convergio and resultado_con_agua.convergio, "Ambos deben converger"
    assert resultado_seco.es_valido and resultado_con_agua.es_valido, "Ambos deben ser válidos"
    
    # El nivel freático debe reducir el factor de seguridad
    reduccion = resultado_seco.factor_seguridad - resultado_con_agua.factor_seguridad
    assert reduccion > 0, f"Nivel freático debe reducir Fs: seco={resultado_seco.factor_seguridad:.3f}, húmedo={resultado_con_agua.factor_seguridad:.3f}"
    
    # Reducción típica: 10-40%
    porcentaje_reduccion = (reduccion / resultado_seco.factor_seguridad) * 100
    assert 5 <= porcentaje_reduccion <= 50, f"Reducción atípica: {porcentaje_reduccion:.1f}%"
    
    print(f"✅ Fs seco: {resultado_seco.factor_seguridad:.3f}")
    print(f"✅ Fs con agua: {resultado_con_agua.factor_seguridad:.3f}")
    print(f"✅ Reducción: {porcentaje_reduccion:.1f}%")


def test_comparacion_bishop_fellenius():
    """Test de comparación entre Bishop y Fellenius."""
    print("\n=== TEST 3: Comparación Bishop vs Fellenius ===")
    
    # Crear caso de prueba con geometría realista
    altura = 10.0
    angulo_talud = 45.0
    longitud_base = altura / math.tan(math.radians(angulo_talud))
    perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
    
    # Círculo de falla realista
    radio = altura * 1.5
    xc = longitud_base * 0.3
    yc = altura * 1.1
    circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
    estrato = Estrato(cohesion=20.0, phi_grados=22.0, gamma=17.5, nombre="Limo")
    
    # Comparación
    comparacion = comparar_bishop_fellenius(circulo, perfil, estrato, num_dovelas=8)
    
    # Verificaciones
    assert comparacion['bishop'].convergio, "Bishop debe converger"
    assert comparacion['fellenius'].es_valido, "Fellenius debe ser válido"
    assert comparacion['bishop'].es_valido, "Bishop debe ser válido"
    
    # Verificar diferencias típicas
    diferencia_abs = abs(comparacion['diferencia_porcentual'])
    assert diferencia_abs <= 30, f"Diferencia muy grande: {diferencia_abs:.1f}%"
    
    # Bishop generalmente da Fs mayor que Fellenius (menos conservador)
    fs_bishop = comparacion['factor_seguridad_bishop']
    fs_fellenius = comparacion['factor_seguridad_fellenius']
    
    print(f"✅ Fs Bishop: {fs_bishop:.3f}")
    print(f"✅ Fs Fellenius: {fs_fellenius:.3f}")
    print(f"✅ Diferencia: {comparacion['diferencia_porcentual']:+.1f}%")
    print(f"✅ Más conservador: {comparacion['mas_conservador']}")
    print(f"✅ Iteraciones Bishop: {comparacion['iteraciones_bishop']}")


def test_generar_reportes():
    """Test de generación de reportes."""
    print("\n=== TEST 4: Generación de reportes ===")
    
    # Análisis simple
    resultado = bishop_talud_homogeneo(
        altura=8.0,
        angulo_talud=40.0,
        cohesion=15.0,
        phi_grados=18.0,
        gamma=16.0
    )
    
    # Generar reporte
    reporte = generar_reporte_bishop(resultado)
    
    # Verificaciones del reporte
    assert "BISHOP MODIFICADO" in reporte, "Debe mencionar el método"
    assert f"{resultado.factor_seguridad:.3f}" in reporte, "Debe incluir Fs"
    assert f"{resultado.iteraciones}" in reporte, "Debe incluir iteraciones"
    assert "CONVERGENCIA" in reporte, "Debe incluir sección de convergencia"
    assert "MOMENTOS" in reporte, "Debe incluir momentos"
    assert "DOVELAS" in reporte, "Debe incluir análisis de dovelas"
    
    # Verificar clasificación
    if resultado.factor_seguridad < 1.0:
        assert "INESTABLE" in reporte
    elif resultado.factor_seguridad < 1.2:
        assert "MARGINALMENTE" in reporte
    elif resultado.factor_seguridad < 1.5:
        assert "ESTABLE" in reporte
    else:
        assert "MUY ESTABLE" in reporte
    
    print(f"✅ Reporte generado: {len(reporte)} caracteres")
    print(f"✅ Clasificación incluida correctamente")
    
    # Test de reporte de comparación con geometría realista
    altura = 8.0
    angulo_talud = 45.0
    longitud_base = altura / math.tan(math.radians(angulo_talud))
    perfil_comp = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
    
    radio_comp = altura * 1.5
    xc_comp = longitud_base * 0.3
    yc_comp = altura * 1.1
    circulo_comp = CirculoFalla(xc=xc_comp, yc=yc_comp, radio=radio_comp)
    
    comparacion = comparar_bishop_fellenius(
        circulo_comp,
        perfil_comp,
        Estrato(cohesion=18.0, phi_grados=20.0, gamma=17.0, nombre="Test")
    )
    
    reporte_comp = generar_reporte_comparacion(comparacion)
    assert "BISHOP MODIFICADO vs FELLENIUS" in reporte_comp
    assert "FACTORES DE SEGURIDAD" in reporte_comp
    assert "RECOMENDACIONES" in reporte_comp
    
    print(f"✅ Reporte comparativo generado: {len(reporte_comp)} caracteres")


def test_casos_limite():
    """Test de casos límite y validaciones."""
    print("\n=== TEST 5: Casos límite ===")
    
    # Test con ángulos empinados (posible problema de mα)
    try:
        resultado = bishop_talud_homogeneo(
            altura=20.0,
            angulo_talud=70.0,  # Muy empinado
            cohesion=5.0,       # Baja cohesión
            phi_grados=15.0,    # Bajo ángulo de fricción
            gamma=20.0,
            factor_inicial=0.5  # Factor inicial bajo
        )
        
        if resultado.convergio:
            print(f"✅ Caso empinado convergió: Fs = {resultado.factor_seguridad:.3f}")
            assert resultado.factor_seguridad > 0.3, "Fs muy bajo"
        else:
            print("⚠️ Caso empinado no convergió (esperado)")
            
    except ValidacionError as e:
        print(f"⚠️ Error esperado en caso empinado: {e}")
    
    # Test con parámetros altos (debe converger bien)
    resultado_alto = bishop_talud_homogeneo(
        altura=8.0,
        angulo_talud=30.0,
        cohesion=50.0,      # Alta cohesión
        phi_grados=35.0,    # Alto ángulo de fricción
        gamma=18.0
    )
    
    assert resultado_alto.convergio, "Caso con parámetros altos debe converger"
    assert resultado_alto.factor_seguridad > 1.5, f"Fs debe ser alto: {resultado_alto.factor_seguridad:.3f}"
    assert resultado_alto.iteraciones <= 15, f"Debe converger rápido: {resultado_alto.iteraciones} iter"
    
    print(f"✅ Caso parámetros altos: Fs = {resultado_alto.factor_seguridad:.3f}, {resultado_alto.iteraciones} iter")


def test_calcular_m_alpha():
    """Test específico para el cálculo de mα."""
    print("\n=== TEST 6: Cálculo de mα ===")
    
    # Crear dovela de prueba
    from data.models import Dovela
    
    # Calcular peso de la dovela
    peso = 1.0 * 2.0 * 18.0  # ancho * altura * gamma
    
    dovela = Dovela(
        x_centro=5.0,
        ancho=1.0,
        altura=2.0,
        angulo_alpha=math.radians(30.0),  # 30 grados
        cohesion=20.0,
        phi_grados=25.0,  # en grados
        gamma=18.0,
        peso=peso,
        presion_poros=0.0,
        longitud_arco=1.2
    )
    
    # Test con diferentes factores de seguridad
    factores_test = [0.5, 1.0, 1.5, 2.0]
    
    for fs in factores_test:
        m_alpha = calcular_m_alpha(dovela, fs)
        
        # Verificar que mα > 0
        assert m_alpha > 0, f"mα debe ser > 0 para Fs={fs}: mα={m_alpha}"
        
        # Verificar fórmula: mα = cos(α) + sin(α)·tan(φ)/Fs
        esperado = dovela.cos_alpha + (dovela.sin_alpha * dovela.tan_phi) / fs
        assert abs(m_alpha - esperado) < 1e-10, f"Error en cálculo de mα para Fs={fs}"
        
        print(f"✅ Fs={fs:.1f}: mα={m_alpha:.4f}")
    
    # Test caso límite: Fs muy bajo debe dar error si mα ≤ 0
    try:
        # Crear dovela con ángulo muy empinado
        peso_empinada = 1.0 * 2.0 * 18.0  # ancho * altura * gamma
        
        dovela_empinada = Dovela(
            x_centro=5.0,
            ancho=1.0,
            altura=2.0,
            angulo_alpha=math.radians(80.0),  # 80 grados - muy empinado
            cohesion=5.0,
            phi_grados=15.0,  # φ bajo en grados
            gamma=18.0,
            peso=peso_empinada,
            presion_poros=0.0,
            longitud_arco=1.2
        )
        
        m_alpha_critico = calcular_m_alpha(dovela_empinada, 0.3)  # Fs muy bajo
        
        if m_alpha_critico <= 0:
            print("⚠️ mα ≤ 0 detectado correctamente")
        else:
            print(f"✅ mα crítico: {m_alpha_critico:.4f}")
            
    except ValidacionError as e:
        print(f"✅ Error esperado para mα ≤ 0: {str(e)[:60]}...")


def main():
    """Ejecutar todos los tests."""
    print("🧪 INICIANDO TESTS FUNCIONALES DE BISHOP MODIFICADO")
    print("=" * 60)
    
    try:
        test_bishop_basico()
        test_bishop_con_nivel_freatico()
        test_comparacion_bishop_fellenius()
        test_generar_reportes()
        test_casos_limite()
        test_calcular_m_alpha()
        
        print("\n" + "=" * 60)
        print("🎉 TODOS LOS TESTS DE BISHOP PASARON EXITOSAMENTE")
        print("✅ Método iterativo funcionando correctamente")
        print("✅ Convergencia validada")
        print("✅ Comparación con Fellenius implementada")
        print("✅ Reportes y validaciones funcionando")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR EN TESTS: {e}")
        raise


if __name__ == "__main__":
    main()
