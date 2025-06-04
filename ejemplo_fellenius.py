"""
Ejemplo práctico del método de Fellenius para análisis de estabilidad de taludes.

Este ejemplo demuestra:
1. Análisis de un talud homogéneo típico
2. Análisis con nivel freático
3. Generación de reportes detallados
4. Comparación de resultados
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.models import Estrato, CirculoFalla
from core.fellenius import (
    fellenius_talud_homogeneo, fellenius_con_nivel_freatico,
    analizar_fellenius, generar_reporte_fellenius, comparar_con_factor_teorico
)
from core.geometry import crear_perfil_simple


def ejemplo_talud_carretera():
    """
    Ejemplo: Análisis de estabilidad de un talud de carretera.
    
    Datos del proyecto:
    - Talud de corte en arcilla
    - Altura: 12 m
    - Pendiente: 1:1.5 (33.7°)
    - Suelo: arcilla con c=25 kPa, φ=22°, γ=19 kN/m³
    """
    print("🛣️ EJEMPLO: TALUD DE CARRETERA")
    print("=" * 60)
    
    print("\n📋 DATOS DEL PROYECTO:")
    print("   Tipo: Talud de corte en carretera")
    print("   Altura: 12.0 m")
    print("   Pendiente: 1:1.5 (33.7°)")
    print("   Material: Arcilla")
    print("   Cohesión: 25 kPa")
    print("   Ángulo fricción: 22°")
    print("   Peso específico: 19 kN/m³")
    
    # Análisis sin nivel freático
    print("\n🔍 ANÁLISIS SIN NIVEL FREÁTICO:")
    resultado_seco = fellenius_talud_homogeneo(
        altura=12.0,
        angulo_talud=33.7,
        cohesion=25.0,
        phi_grados=22.0,
        gamma=19.0,
        factor_radio=1.4,
        num_dovelas=15
    )
    
    print(f"   Factor de Seguridad: {resultado_seco.factor_seguridad:.3f}")
    
    # Clasificación de estabilidad
    if resultado_seco.factor_seguridad < 1.0:
        clasificacion = "INESTABLE ⚠️"
        recomendacion = "Requiere medidas correctivas inmediatas"
    elif resultado_seco.factor_seguridad < 1.2:
        clasificacion = "MARGINALMENTE ESTABLE ⚡"
        recomendacion = "Requiere monitoreo y posibles mejoras"
    elif resultado_seco.factor_seguridad < 1.5:
        clasificacion = "ESTABLE ✅"
        recomendacion = "Aceptable para uso normal"
    else:
        clasificacion = "MUY ESTABLE 🛡️"
        recomendacion = "Excelente condición de estabilidad"
    
    print(f"   Clasificación: {clasificacion}")
    print(f"   Recomendación: {recomendacion}")
    
    # Análisis con nivel freático
    print("\n🌊 ANÁLISIS CON NIVEL FREÁTICO (4m profundidad):")
    resultado_freatico = fellenius_con_nivel_freatico(
        altura=12.0,
        angulo_talud=33.7,
        cohesion=25.0,
        phi_grados=22.0,
        gamma=19.0,
        gamma_sat=21.0,
        profundidad_freatico=4.0,
        factor_radio=1.4,
        num_dovelas=15
    )
    
    print(f"   Factor de Seguridad: {resultado_freatico.factor_seguridad:.3f}")
    
    # Comparación de resultados
    reduccion = ((resultado_seco.factor_seguridad - resultado_freatico.factor_seguridad) / 
                resultado_seco.factor_seguridad) * 100
    
    print(f"\n📊 COMPARACIÓN DE RESULTADOS:")
    print(f"   Sin nivel freático: {resultado_seco.factor_seguridad:.3f}")
    print(f"   Con nivel freático: {resultado_freatico.factor_seguridad:.3f}")
    print(f"   Reducción por agua: {reduccion:.1f}%")
    
    # Generar reporte detallado
    print(f"\n📄 REPORTE DETALLADO:")
    reporte = generar_reporte_fellenius(resultado_freatico)
    print(reporte)
    
    return resultado_seco, resultado_freatico


def ejemplo_talud_minero():
    """
    Ejemplo: Análisis de un talud de mina a cielo abierto.
    
    Datos del proyecto:
    - Talud de gran altura
    - Altura: 25 m
    - Pendiente: 45°
    - Suelo: roca alterada con c=40 kPa, φ=28°, γ=22 kN/m³
    """
    print("\n⛏️ EJEMPLO: TALUD MINERO")
    print("=" * 60)
    
    print("\n📋 DATOS DEL PROYECTO:")
    print("   Tipo: Talud de mina a cielo abierto")
    print("   Altura: 25.0 m")
    print("   Pendiente: 45°")
    print("   Material: Roca alterada")
    print("   Cohesión: 40 kPa")
    print("   Ángulo fricción: 28°")
    print("   Peso específico: 22 kN/m³")
    
    # Análisis del talud minero
    resultado = fellenius_talud_homogeneo(
        altura=25.0,
        angulo_talud=45.0,
        cohesion=40.0,
        phi_grados=28.0,
        gamma=22.0,
        factor_radio=1.2,  # Radio menor para talud empinado
        num_dovelas=20     # Más dovelas para mayor precisión
    )
    
    print(f"\n🔍 RESULTADOS DEL ANÁLISIS:")
    print(f"   Factor de Seguridad: {resultado.factor_seguridad:.3f}")
    print(f"   Momento Resistente: {resultado.momento_resistente:.0f} kN·m")
    print(f"   Momento Actuante: {resultado.momento_actuante:.0f} kN·m")
    print(f"   Número de dovelas: {len(resultado.dovelas)}")
    print(f"   Dovelas en tracción: {resultado.detalles_calculo['dovelas_en_traccion']}")
    
    # Comparar con criterio minero (Fs > 1.3 típicamente requerido)
    criterio_minero = 1.3
    comparacion = comparar_con_factor_teorico(resultado, criterio_minero, tolerancia=0.1)
    
    print(f"\n⚖️ EVALUACIÓN SEGÚN CRITERIO MINERO:")
    print(f"   Criterio requerido: Fs ≥ {criterio_minero}")
    print(f"   Factor calculado: {resultado.factor_seguridad:.3f}")
    
    if resultado.factor_seguridad >= criterio_minero:
        print("   ✅ CUMPLE con criterio minero")
        print("   Recomendación: Talud aceptable para operación")
    else:
        print("   ❌ NO CUMPLE con criterio minero")
        print("   Recomendación: Requiere reducir ángulo o mejorar parámetros")
    
    return resultado


def ejemplo_comparativo():
    """
    Ejemplo comparativo: Efecto de diferentes parámetros del suelo.
    """
    print("\n📊 EJEMPLO COMPARATIVO: EFECTO DE PARÁMETROS")
    print("=" * 60)
    
    # Caso base
    print("\n🔧 ANÁLISIS PARAMÉTRICO:")
    print("   Geometría fija: altura=10m, pendiente=30°")
    print("   Variando parámetros del suelo:")
    
    casos = [
        {"nombre": "Arcilla blanda", "c": 15, "phi": 18, "gamma": 17},
        {"nombre": "Arcilla media", "c": 25, "phi": 22, "gamma": 19},
        {"nombre": "Arcilla dura", "c": 40, "phi": 26, "gamma": 20},
        {"nombre": "Limo arcilloso", "c": 20, "phi": 24, "gamma": 18},
        {"nombre": "Arena arcillosa", "c": 10, "phi": 30, "gamma": 19}
    ]
    
    resultados = []
    
    print(f"\n{'Material':<15} | {'c (kPa)':<8} | {'φ (°)':<6} | {'γ (kN/m³)':<10} | {'Fs':<6}")
    print("-" * 60)
    
    for caso in casos:
        resultado = fellenius_talud_homogeneo(
            altura=10.0,
            angulo_talud=30.0,
            cohesion=caso["c"],
            phi_grados=caso["phi"],
            gamma=caso["gamma"],
            num_dovelas=12
        )
        
        resultados.append((caso["nombre"], resultado))
        
        print(f"{caso['nombre']:<15} | {caso['c']:>6} | {caso['phi']:>4} | {caso['gamma']:>8} | {resultado.factor_seguridad:>5.2f}")
    
    # Encontrar el mejor y peor caso
    fs_valores = [r[1].factor_seguridad for r in resultados]
    mejor_caso = resultados[fs_valores.index(max(fs_valores))]
    peor_caso = resultados[fs_valores.index(min(fs_valores))]
    
    print(f"\n🏆 MEJOR CASO: {mejor_caso[0]} (Fs = {mejor_caso[1].factor_seguridad:.3f})")
    print(f"⚠️ PEOR CASO: {peor_caso[0]} (Fs = {peor_caso[1].factor_seguridad:.3f})")
    
    diferencia = mejor_caso[1].factor_seguridad - peor_caso[1].factor_seguridad
    print(f"📈 RANGO DE VARIACIÓN: {diferencia:.3f} ({(diferencia/peor_caso[1].factor_seguridad)*100:.1f}%)")
    
    return resultados


def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🏗️ EJEMPLOS PRÁCTICOS - MÉTODO DE FELLENIUS")
    print("=" * 80)
    print("Análisis de estabilidad de taludes usando el método de Fellenius")
    print("Método directo (no iterativo) - Asume fuerzas entre dovelas = 0")
    print("=" * 80)
    
    try:
        # Ejemplo 1: Talud de carretera
        resultado_carretera = ejemplo_talud_carretera()
        
        # Ejemplo 2: Talud minero
        resultado_minero = ejemplo_talud_minero()
        
        # Ejemplo 3: Análisis comparativo
        resultados_comparativo = ejemplo_comparativo()
        
        print("\n" + "=" * 80)
        print("✅ TODOS LOS EJEMPLOS EJECUTADOS EXITOSAMENTE")
        print("\n🎯 CONCLUSIONES GENERALES:")
        print("   • El método de Fellenius proporciona resultados conservadores")
        print("   • El nivel freático reduce significativamente el factor de seguridad")
        print("   • Los parámetros del suelo tienen gran influencia en la estabilidad")
        print("   • Es importante validar la geometría y número de dovelas")
        print("   • Los reportes detallados facilitan la interpretación de resultados")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR EN EJEMPLOS: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
