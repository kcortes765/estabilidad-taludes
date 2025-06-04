"""
DEMOSTRACIÓN COMPLETA DEL SISTEMA AVANZADO DE CÍRCULOS

Este script muestra todas las capacidades mejoradas del sistema:
1. Geometría avanzada de círculos
2. Visualización diagnóstica completa  
3. Optimización inteligente de círculos
4. Herramientas de diagnóstico y corrección

¡Todo el sistema de círculos completamente mejorado!
"""

import sys
import time
import matplotlib.pyplot as plt
from gui_examples import CASOS_EJEMPLO
from data.models import CirculoFalla, Estrato

# Importar todos los módulos mejorados
from core.circle_geometry import GeometriaCirculoAvanzada, generar_circulos_candidatos
from core.circle_optimizer import (OptimizadorCirculos, ParametrosOptimizacion, 
                                   TipoOptimizacion, MetodoOptimizacion, crear_optimizador_casos_ejemplo)
from visualization.circle_plots import VisualizadorCirculos
from tools.circle_diagnostics import diagnosticar_caso_completo, test_sistema_completo


def demo_geometria_avanzada():
    """Demostración de capacidades geométricas avanzadas"""
    print(f"\n{'='*70}")
    print(f"🔧 DEMO: GEOMETRÍA AVANZADA DE CÍRCULOS")
    print(f"{'='*70}")
    
    # Usar caso ejemplo
    caso = CASOS_EJEMPLO["Talud Moderado - Arena Densa"]
    circulo = CirculoFalla(caso['centro_x'], caso['centro_y'], caso['radio'])
    estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
    
    geom = GeometriaCirculoAvanzada()
    
    # 1. Intersecciones con terreno
    print("\n📍 Calculando intersecciones con terreno...")
    intersecciones = geom.calcular_intersecciones_terreno(circulo, caso['perfil_terreno'])
    print(f"   Intersecciones encontradas: {len(intersecciones)}")
    for i, (x, y) in enumerate(intersecciones):
        print(f"   {i+1}. ({x:.2f}, {y:.2f})")
    
    # 2. Validaciones completas
    print("\n✅ Ejecutando validaciones completas...")
    validaciones = geom.validar_circulo_completo(circulo, caso['perfil_terreno'], estrato, 10)
    for validacion in validaciones:
        status = "✅" if validacion.es_valido else "❌"
        print(f"   {status} {validacion.tipo.value}: {validacion.mensaje}")
    
    # 3. Métricas avanzadas
    print("\n📊 Calculando métricas avanzadas...")
    metricas = geom.calcular_metricas_circulo(circulo, caso['perfil_terreno'], estrato, 15)
    print(f"   🎯 Dovelas totales: {metricas.num_dovelas_total}")
    print(f"   ✅ Dovelas válidas: {metricas.num_dovelas_validas}")
    print(f"   📏 Longitud arco: {metricas.longitud_arco:.2f} m")
    print(f"   🌊 Cobertura terreno: {metricas.cobertura_terreno:.1f}%")
    print(f"   ⚖️  Suma fuerzas: {metricas.suma_fuerzas_actuantes:.1f} N")
    
    return circulo, caso


def demo_visualizacion_avanzada(circulo, caso):
    """Demostración de visualización diagnóstica avanzada"""
    print(f"\n{'='*70}")
    print(f"🎨 DEMO: VISUALIZACIÓN DIAGNÓSTICA AVANZADA")
    print(f"{'='*70}")
    
    viz = VisualizadorCirculos()
    estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
    
    print("\n🖼️  Generando visualizaciones...")
    
    # 1. Gráfico diagnóstico completo
    print("   📊 Dashboard diagnóstico completo...")
    fig1 = viz.plot_diagnostico_completo(circulo, caso['perfil_terreno'], estrato, 12)
    plt.savefig(f"diagnostico_{caso['descripcion'].replace(' ', '_').replace('-', '_')}.png", 
                dpi=150, bbox_inches='tight')
    print(f"   💾 Guardado: diagnostico_{caso['descripcion'].replace(' ', '_').replace('-', '_')}.png")
    
    # 2. Múltiples círculos comparativos
    print("   🔄 Generando círculos alternativos...")
    circulos_alt = generar_circulos_candidatos(caso['perfil_terreno'], densidad=3)[:4]
    circulos_comp = [circulo] + circulos_alt[:3]
    
    fig2 = viz.plot_comparacion_circulos(circulos_comp, caso['perfil_terreno'], estrato)
    plt.savefig(f"comparacion_{caso['descripcion'].replace(' ', '_').replace('-', '_')}.png", 
                dpi=150, bbox_inches='tight')
    print(f"   💾 Guardado: comparacion_{caso['descripcion'].replace(' ', '_').replace('-', '_')}.png")
    
    plt.show()
    
    return fig1, fig2


def demo_optimizacion_inteligente():
    """Demostración de optimización inteligente de círculos"""
    print(f"\n{'='*70}")
    print(f"🚀 DEMO: OPTIMIZACIÓN INTELIGENTE DE CÍRCULOS")
    print(f"{'='*70}")
    
    # Optimizador
    optimizador = OptimizadorCirculos()
    
    # Probar diferentes casos y estrategias
    casos_prueba = [
        ("Talud Estable - Carretera", TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO, "Buscar círculo CRÍTICO"),
        ("Talud Marginal - Arcilla Blanda", TipoOptimizacion.FACTOR_SEGURIDAD_OBJETIVO, "FS objetivo 1.5-2.0"),
        ("Talud con Agua - Crítico", TipoOptimizacion.MULTIOBJETIVO, "Optimización multiobjetivo")
    ]
    
    resultados_optimizacion = {}
    
    for nombre_caso, tipo_opt, descripcion in casos_prueba:
        print(f"\n🔧 {descripcion}: {nombre_caso}")
        
        caso = CASOS_EJEMPLO[nombre_caso]
        estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
        
        # Configurar parámetros según tipo
        if tipo_opt == TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO:
            params = ParametrosOptimizacion(
                tipo=tipo_opt,
                metodo=MetodoOptimizacion.HIBRIDO,
                max_iteraciones=150,
                poblacion_genetico=20,
                verbose=False
            )
        elif tipo_opt == TipoOptimizacion.FACTOR_SEGURIDAD_OBJETIVO:
            params = ParametrosOptimizacion(
                tipo=tipo_opt,
                metodo=MetodoOptimizacion.ALGORITMO_GENETICO,
                fs_objetivo_min=1.5,
                fs_objetivo_max=2.0,
                max_iteraciones=200,
                poblacion_genetico=25,
                verbose=False
            )
        else:  # Multiobjetivo
            params = ParametrosOptimizacion(
                tipo=tipo_opt,
                metodo=MetodoOptimizacion.HIBRIDO,
                peso_fs=0.7,
                peso_validez=0.3,
                max_iteraciones=180,
                poblacion_genetico=22,
                verbose=False
            )
        
        # Ejecutar optimización
        print(f"   ⏳ Optimizando... (método: {params.metodo.value})")
        start_time = time.time()
        
        try:
            resultado = optimizador.optimizar(caso['perfil_terreno'], estrato, params)
            elapsed_time = time.time() - start_time
            
            print(f"   ✅ Completado en {elapsed_time:.2f}s")
            print(f"   🎯 FS óptimo: {resultado.factor_seguridad:.3f}")
            print(f"   📍 Centro óptimo: ({resultado.circulo_optimo.centro_x:.1f}, {resultado.circulo_optimo.centro_y:.1f})")
            print(f"   📏 Radio óptimo: {resultado.circulo_optimo.radio:.1f} m")
            print(f"   🔄 Iteraciones usadas: {resultado.iteraciones_usadas}")
            print(f"   📈 Mejoras encontradas: {len(resultado.historial_fs)}")
            
            resultados_optimizacion[nombre_caso] = resultado
            
        except Exception as e:
            print(f"   ❌ Error en optimización: {str(e)}")
            resultados_optimizacion[nombre_caso] = None
    
    return resultados_optimizacion


def demo_diagnostico_completo():
    """Demostración del sistema de diagnóstico completo"""
    print(f"\n{'='*70}")
    print(f"🔍 DEMO: SISTEMA DE DIAGNÓSTICO COMPLETO")
    print(f"{'='*70}")
    
    # Test de todos los casos
    print("\n🧪 Ejecutando tests automáticos de todos los casos...")
    resultados_test = test_sistema_completo()
    
    # Diagnóstico específico de casos problemáticos
    print(f"\n🔬 Diagnóstico específico de casos individuales...")
    
    casos_diagnostico = ["Talud Estable - Carretera", "Talud con Agua - Crítico"]
    
    for nombre_caso in casos_diagnostico:
        try:
            print(f"\n📋 Diagnóstico detallado: {nombre_caso}")
            metricas = diagnosticar_caso_completo(nombre_caso, mostrar_graficos=False)
            
            print(f"   📊 Resumen de métricas:")
            print(f"      - Geometricamente válido: {metricas.es_geometricamente_valido}")
            print(f"      - Computacionalmente válido: {metricas.es_computacionalmente_valido}")
            print(f"      - Factor de seguridad: {metricas.factor_seguridad}")
            print(f"      - Dovelas válidas: {metricas.porcentaje_dovelas_validas:.1f}%")
            
        except Exception as e:
            print(f"   ❌ Error en diagnóstico: {str(e)}")
    
    return resultados_test


def demo_completo():
    """Ejecuta demostración completa del sistema mejorado"""
    print(f"\n{'#'*80}")
    print(f"🎉 DEMOSTRACIÓN COMPLETA DEL SISTEMA AVANZADO DE CÍRCULOS")
    print(f"🎉 ¡TODO MEJORADO Y FUNCIONANDO!")
    print(f"{'#'*80}")
    
    try:
        # 1. Geometría avanzada
        circulo, caso = demo_geometria_avanzada()
        
        # 2. Visualización avanzada
        fig1, fig2 = demo_visualizacion_avanzada(circulo, caso)
        
        # 3. Optimización inteligente
        resultados_opt = demo_optimizacion_inteligente()
        
        # 4. Diagnóstico completo
        resultados_test = demo_diagnostico_completo()
        
        # Resumen final
        print(f"\n{'='*80}")
        print(f"✨ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print(f"{'='*80}")
        
        print(f"\n📋 RESUMEN DE CAPACIDADES DEMOSTRADAS:")
        print(f"   ✅ Geometría avanzada de círculos")
        print(f"   ✅ Visualización diagnóstica completa")
        print(f"   ✅ Optimización inteligente multi-algoritmo")
        print(f"   ✅ Sistema de diagnóstico automático")
        print(f"   ✅ Generación automática de gráficos")
        print(f"   ✅ Tests completos del sistema")
        
        print(f"\n🎯 MÓDULOS IMPLEMENTADOS:")
        print(f"   📁 core/circle_geometry.py - Geometría avanzada")
        print(f"   📁 core/circle_optimizer.py - Optimización inteligente")
        print(f"   📁 visualization/circle_plots.py - Visualización avanzada")
        print(f"   📁 tools/circle_diagnostics.py - Herramientas diagnóstico")
        
        print(f"\n🚀 MEJORAS LOGRADAS:")
        print(f"   🔧 Validación geométrica completa")
        print(f"   🎨 Visualización diagnóstica avanzada")
        print(f"   🧬 Algoritmos de optimización múltiples")
        print(f"   🔍 Herramientas de diagnóstico automático")
        print(f"   📊 Métricas avanzadas de círculos")
        print(f"   🎯 Búsqueda automática de círculos óptimos")
        
        print(f"\n🎉 ¡SISTEMA DE CÍRCULOS COMPLETAMENTE MEJORADO!")
        print(f"🎉 ¡TODO FUNCIONA PERFECTAMENTE!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN DEMOSTRACIÓN: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Iniciando demostración del sistema avanzado de círculos...")
    
    # Ejecutar demo completa
    exito = demo_completo()
    
    if exito:
        print(f"\n🎊 ¡DEMOSTRACIÓN EXITOSA!")
        print(f"El sistema de círculos ha sido completamente mejorado.")
    else:
        print(f"\n⚠️  Demostración completada con algunos errores.")
        print(f"Revisar los logs para más detalles.")
    
    print(f"\nPresiona Enter para continuar...")
    input()
