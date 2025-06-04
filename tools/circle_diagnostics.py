"""
Herramientas de Diagnóstico Visual para Círculos de Falla

Diagnóstico completo, tests automáticos y corrección de problemas.
"""

import matplotlib.pyplot as plt
from typing import List, Tuple
from gui_examples import CASOS_EJEMPLO
from core.circle_geometry import GeometriaCirculoAvanzada
from core.circle_optimizer import OptimizadorCirculos, ParametrosOptimizacion, TipoOptimizacion, MetodoOptimizacion
from visualization.circle_plots import VisualizadorCirculos
from data.models import CirculoFalla, Estrato


def diagnosticar_caso_completo(nombre_caso: str, mostrar_graficos: bool = True):
    """Diagnóstico completo de un caso de ejemplo"""
    print(f"\n{'='*60}")
    print(f"🔍 DIAGNÓSTICO COMPLETO: {nombre_caso}")
    print(f"{'='*60}")
    
    caso = CASOS_EJEMPLO[nombre_caso]
    circulo = CirculoFalla(caso['centro_x'], caso['centro_y'], caso['radio'])
    estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
    
    # Geometría avanzada
    geom = GeometriaCirculoAvanzada()
    
    # 1. Validaciones
    print("\n📋 VALIDACIONES:")
    validaciones = geom.validar_circulo_completo(circulo, caso['perfil_terreno'], estrato, 10)
    for v in validaciones:
        icono = "✅" if v.es_valido else "❌"
        print(f"   {icono} {v.tipo.value}: {v.mensaje}")
    
    # 2. Métricas
    print("\n📊 MÉTRICAS:")
    metricas = geom.calcular_metricas_circulo(circulo, caso['perfil_terreno'], estrato, 10)
    print(f"   🎯 Dovelas válidas: {metricas.num_dovelas_validas}/{metricas.num_dovelas_total}")
    print(f"   🌊 Cobertura terreno: {metricas.cobertura_terreno:.1f}%")
    print(f"   ⚖️  Fuerzas actuantes: {metricas.suma_fuerzas_actuantes:.1f} N")
    
    # 3. Gráficos si se solicita
    if mostrar_graficos:
        viz = VisualizadorCirculos()
        fig = viz.plot_diagnostico_completo(circulo, caso['perfil_terreno'], estrato, 10)
        plt.show()
    
    return metricas


def test_sistema_completo():
    """Test completo del sistema de círculos"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST COMPLETO DEL SISTEMA DE CÍRCULOS")
    print(f"{'='*60}")
    
    resultados = {}
    
    for nombre in CASOS_EJEMPLO.keys():
        print(f"\n🔬 Testing: {nombre}")
        try:
            metricas = diagnosticar_caso_completo(nombre, mostrar_graficos=False)
            resultados[nombre] = {
                'valido_geometricamente': metricas.es_geometricamente_valido,
                'valido_computacionalmente': metricas.es_computacionalmente_valido,
                'dovelas_validas': metricas.porcentaje_dovelas_validas,
                'factor_seguridad': metricas.factor_seguridad
            }
            
            if metricas.es_geometricamente_valido and metricas.es_computacionalmente_valido:
                print(f"   ✅ PASÓ todos los tests")
            else:
                print(f"   ❌ FALLÓ tests de validación")
                
        except Exception as e:
            print(f"   💥 ERROR: {str(e)}")
            resultados[nombre] = {'error': str(e)}
    
    # Resumen
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN DE RESULTADOS:")
    print(f"{'='*60}")
    
    exitosos = 0
    for nombre, resultado in resultados.items():
        if 'error' not in resultado:
            if resultado['valido_geometricamente'] and resultado['valido_computacionalmente']:
                print(f"✅ {nombre}: FS = {resultado.get('factor_seguridad', 'N/A')}")
                exitosos += 1
            else:
                print(f"⚠️  {nombre}: Parcialmente válido")
        else:
            print(f"❌ {nombre}: {resultado['error']}")
    
    print(f"\n🎯 ÉXITO: {exitosos}/{len(CASOS_EJEMPLO)} casos funcionando correctamente")
    
    return resultados


if __name__ == "__main__":
    test_sistema_completo()
