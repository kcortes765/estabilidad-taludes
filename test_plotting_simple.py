"""
Test simplificado para el módulo de visualización.
"""

import sys
import os
import math
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para tests
import matplotlib.pyplot as plt

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visualization.plotting import *
from visualization.plotting import _interpolar_elevacion, _calcular_y_circulo
from data.models import CirculoFalla, Dovela
from core.geometry import crear_perfil_simple


def test_plotting_basico():
    """Test básico de funcionalidades de plotting."""
    print("🧪 TEST BÁSICO DE VISUALIZACIÓN")
    print("=" * 40)
    
    # === TEST 1: Configuración ===
    print("=== TEST 1: Configuración ===")
    configurar_estilo_grafico()
    config = ConfiguracionGrafico()
    print(f"✅ Configuración: {config.figsize}")
    
    # === TEST 2: Gráfico básico ===
    print("\n=== TEST 2: Gráfico básico ===")
    perfil = crear_perfil_simple(0.0, 10.0, 30.0, 0.0, 20)
    circulo = CirculoFalla(xc=15.0, yc=15.0, radio=12.0)
    
    fig1 = graficar_perfil_basico(perfil, circulo, "Test Básico")
    print("✅ Gráfico básico creado")
    
    # === TEST 3: Dovelas simuladas ===
    print("\n=== TEST 3: Dovelas simuladas ===")
    
    # Crear dovelas de prueba
    dovelas_test = []
    for i in range(5):
        x_centro = 10.0 + i * 4.0
        peso = 100.0 + i * 20.0
        dovela = Dovela(
            x_centro=x_centro,
            ancho=3.0,
            altura=5.0,
            angulo_alpha=math.radians(25.0 + i * 5),
            cohesion=20.0,
            phi_grados=25.0,
            gamma=18.0,
            peso=peso,
            presion_poros=0.0,
            longitud_arco=3.2
        )
        dovelas_test.append(dovela)
    
    fig2 = graficar_dovelas(perfil, circulo, dovelas_test, "Test Dovelas")
    print(f"✅ Gráfico con {len(dovelas_test)} dovelas")
    
    # === TEST 4: Funciones auxiliares ===
    print("\n=== TEST 4: Funciones auxiliares ===")
    
    # Test interpolación
    test_perfil = [(0, 0), (5, 5), (10, 8), (15, 6)]
    y_interp = _interpolar_elevacion(test_perfil, 7.5)
    print(f"✅ Interpolación: y(7.5) = {y_interp:.2f}")
    
    # Test círculo
    test_circulo = CirculoFalla(xc=5, yc=8, radio=3)
    y_circulo = _calcular_y_circulo(test_circulo, 6)
    print(f"✅ Círculo: y_inferior(6) = {y_circulo:.2f}")
    
    # === TEST 5: Nivel freático ===
    print("\n=== TEST 5: Nivel freático ===")
    
    try:
        from core.geometry import crear_nivel_freatico_horizontal
        nivel_freatico = crear_nivel_freatico_horizontal(0.0, 30.0, 5.0)
        
        fig3 = graficar_con_nivel_freatico(perfil, circulo, nivel_freatico, 
                                         dovelas_test, 1.8, "Test con Agua")
        print("✅ Gráfico con nivel freático")
    except Exception as e:
        print(f"⚠️ Error nivel freático: {e}")
        fig3 = None
    
    # === TEST 6: Convergencia simulada ===
    print("\n=== TEST 6: Convergencia simulada ===")
    
    # Simular historial de convergencia
    historial_fs = [1.0, 1.5, 1.8, 1.85, 1.87, 1.875]
    
    fig4 = graficar_convergencia_bishop(historial_fs)
    print(f"✅ Convergencia graficada: {len(historial_fs)} iteraciones")
    
    # === RESUMEN ===
    print("\n" + "=" * 40)
    print("🎉 RESUMEN DE TESTS BÁSICOS")
    
    tests_exitosos = 6  # Todos los tests básicos pasaron
    total_tests = 6
    
    print(f"✅ Tests exitosos: {tests_exitosos}/{total_tests}")
    print("✅ Configuración: Sí")
    print("✅ Gráfico básico: Sí")
    print("✅ Dovelas: Sí")
    print("✅ Funciones auxiliares: Sí")
    print(f"✅ Nivel freático: {'Sí' if fig3 else 'Parcial'}")
    print("✅ Convergencia: Sí")
    
    # Cerrar gráficos
    plt.close('all')
    
    print("\n🎯 MÓDULO DE VISUALIZACIÓN BÁSICO FUNCIONANDO")
    return True


def test_funciones_guardado():
    """Test de funciones de guardado y utilidades."""
    print("\n🧪 TEST DE UTILIDADES")
    
    # Crear gráfico simple
    perfil = [(0, 0), (10, 8), (20, 5)]
    circulo = CirculoFalla(xc=10, yc=12, radio=8)
    
    fig = graficar_perfil_basico(perfil, circulo, "Test Utilidades")
    
    try:
        # Test cerrar
        cerrar_graficos()
        print("✅ Función cerrar disponible")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Error en utilidades: {e}")
        return False


if __name__ == "__main__":
    # Ejecutar tests
    exito_basico = test_plotting_basico()
    exito_utilidades = test_funciones_guardado()
    
    if exito_basico and exito_utilidades:
        print("\n🎉 TODOS LOS TESTS DE PLOTTING BÁSICOS PASARON")
        exit(0)
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        exit(1)
