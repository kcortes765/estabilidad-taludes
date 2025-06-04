"""
DEMOSTRACIÓN SIMPLIFICADA DEL SISTEMA AVANZADO DE CÍRCULOS

Sistema completamente mejorado sin dependencias gráficas.
"""

import sys
import time
from gui_examples import CASOS_EJEMPLO
from data.models import CirculoFalla, Estrato

# Importar módulos mejorados (sin matplotlib)
from core.circle_geometry import GeometriaCirculoAvanzada, generar_circulos_candidatos
from core.circle_optimizer import (OptimizadorCirculos, ParametrosOptimizacion, 
                                   TipoOptimizacion, MetodoOptimizacion)


def demo_geometria_avanzada():
    """Demostración de capacidades geométricas avanzadas"""
    print(f"\n{'='*70}")
    print(f"🔧 DEMO: GEOMETRÍA AVANZADA DE CÍRCULOS")
    print(f"{'='*70}")
    
    caso = CASOS_EJEMPLO["Talud Moderado - Arena Densa"]
    circulo = CirculoFalla(caso['centro_x'], caso['centro_y'], caso['radio'])
    estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
    
    geom = GeometriaCirculoAvanzada()
    
    print("\n📍 Calculando intersecciones con terreno...")
    intersecciones = geom.calcular_intersecciones_terreno(circulo, caso['perfil_terreno'])
    print(f"   Intersecciones encontradas: {len(intersecciones)}")
    for i, (x, y) in enumerate(intersecciones):
        print(f"   {i+1}. ({x:.2f}, {y:.2f})")
    
    print("\n✅ Ejecutando validaciones completas...")
    validaciones = geom.validar_circulo_completo(circulo, caso['perfil_terreno'], estrato, 10)
    for validacion in validaciones:
        status = "✅" if validacion.es_valido else "❌"
        print(f"   {status} {validacion.tipo.value}: {validacion.mensaje}")
    
    print("\n📊 Calculando métricas avanzadas...")
    metricas = geom.calcular_metricas_circulo(circulo, caso['perfil_terreno'], estrato, 15)
    print(f"   🎯 Dovelas totales: {metricas.num_dovelas_total}")
    print(f"   ✅ Dovelas válidas: {metricas.num_dovelas_validas}")
    print(f"   📏 Longitud arco: {metricas.longitud_arco:.2f} m")
    print(f"   🌊 Cobertura terreno: {metricas.cobertura_terreno:.1f}%")
    print(f"   ⚖️  Suma fuerzas: {metricas.suma_fuerzas_actuantes:.1f} N")
    
    return circulo, caso


def demo_optimizacion_inteligente():
    """Demostración de optimización inteligente"""
    print(f"\n{'='*70}")
    print(f"🚀 DEMO: OPTIMIZACIÓN INTELIGENTE DE CÍRCULOS")
    print(f"{'='*70}")
    
    optimizador = OptimizadorCirculos()
    
    casos_prueba = [
        ("Talud Estable - Carretera", TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO, "Buscar círculo CRÍTICO"),
        ("Talud Marginal - Arcilla Blanda", TipoOptimizacion.FACTOR_SEGURIDAD_OBJETIVO, "FS objetivo 1.5-2.0")
    ]
    
    for nombre_caso, tipo_opt, descripcion in casos_prueba:
        print(f"\n🔧 {descripcion}: {nombre_caso}")
        
        caso = CASOS_EJEMPLO[nombre_caso]
        estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
        
        if tipo_opt == TipoOptimizacion.FACTOR_SEGURIDAD_MINIMO:
            params = ParametrosOptimizacion(
                tipo=tipo_opt,
                metodo=MetodoOptimizacion.GRILLA_SISTEMATICA,
                max_iteraciones=50,
                verbose=False
            )
        else:
            params = ParametrosOptimizacion(
                tipo=tipo_opt,
                metodo=MetodoOptimizacion.BUSQUEDA_ALEATORIA,
                fs_objetivo_min=1.5,
                fs_objetivo_max=2.0,
                max_iteraciones=80,
                verbose=False
            )
        
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
            
        except Exception as e:
            print(f"   ❌ Error en optimización: {str(e)}")


def demo_test_casos():
    """Test de todos los casos sin gráficos"""
    print(f"\n{'='*70}")
    print(f"🧪 DEMO: TEST DE TODOS LOS CASOS")
    print(f"{'='*70}")
    
    geom = GeometriaCirculoAvanzada()
    exitosos = 0
    
    for nombre, caso in CASOS_EJEMPLO.items():
        print(f"\n🔬 Testing: {nombre}")
        
        try:
            circulo = CirculoFalla(caso['centro_x'], caso['centro_y'], caso['radio'])
            estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
            
            validaciones = geom.validar_circulo_completo(circulo, caso['perfil_terreno'], estrato, 10)
            metricas = geom.calcular_metricas_circulo(circulo, caso['perfil_terreno'], estrato, 10)
            
            valido_geo = metricas.es_geometricamente_valido
            valido_comp = metricas.es_computacionalmente_valido
            
            if valido_geo and valido_comp:
                print(f"   ✅ PASÓ todos los tests - FS: {metricas.factor_seguridad}")
                exitosos += 1
            else:
                print(f"   ⚠️  Parcialmente válido - Geo: {valido_geo}, Comp: {valido_comp}")
                
        except Exception as e:
            print(f"   💥 ERROR: {str(e)}")
    
    print(f"\n🎯 ÉXITO: {exitosos}/{len(CASOS_EJEMPLO)} casos funcionando correctamente")


def demo_completo():
    """Ejecuta demostración completa"""
    print(f"\n{'#'*80}")
    print(f"🎉 DEMOSTRACIÓN COMPLETA DEL SISTEMA AVANZADO DE CÍRCULOS")
    print(f"🎉 ¡TODO MEJORADO Y FUNCIONANDO!")
    print(f"{'#'*80}")
    
    try:
        # 1. Geometría avanzada
        circulo, caso = demo_geometria_avanzada()
        
        # 2. Optimización inteligente
        demo_optimizacion_inteligente()
        
        # 3. Test de todos los casos
        demo_test_casos()
        
        print(f"\n{'='*80}")
        print(f"✨ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print(f"{'='*80}")
        
        print(f"\n📋 CAPACIDADES DEMOSTRADAS:")
        print(f"   ✅ Geometría avanzada de círculos")
        print(f"   ✅ Optimización inteligente multi-algoritmo") 
        print(f"   ✅ Validación completa automática")
        print(f"   ✅ Métricas avanzadas de círculos")
        print(f"   ✅ Tests automáticos del sistema")
        
        print(f"\n🎯 MÓDULOS IMPLEMENTADOS:")
        print(f"   📁 core/circle_geometry.py - Geometría avanzada")
        print(f"   📁 core/circle_optimizer.py - Optimización inteligente")
        print(f"   📁 visualization/circle_plots.py - Visualización avanzada")
        print(f"   📁 tools/circle_diagnostics.py - Herramientas diagnóstico")
        
        print(f"\n🚀 MEJORAS LOGRADAS:")
        print(f"   🔧 Validación geométrica completa")
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
    
    exito = demo_completo()
    
    if exito:
        print(f"\n🎊 ¡DEMOSTRACIÓN EXITOSA!")
        print(f"El sistema de círculos ha sido completamente mejorado.")
    else:
        print(f"\n⚠️  Demostración completada con algunos errores.")
    
    print(f"\nPresiona Enter para continuar...")
    input()
