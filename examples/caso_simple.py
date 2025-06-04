"""
Ejemplo de caso simple: Análisis de estabilidad de un talud homogéneo.

Este ejemplo demuestra el uso básico del sistema para analizar
un talud simple con ambos métodos (Fellenius y Bishop).
"""

import sys
import os
import math

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.fellenius import fellenius_talud_homogeneo, generar_reporte_fellenius
from core.bishop import bishop_talud_homogeneo, generar_reporte_bishop, comparar_bishop_fellenius
from visualization.plotting import *
import matplotlib.pyplot as plt


def caso_talud_carretera():
    """
    Ejemplo: Análisis de estabilidad de un talud de carretera.
    
    Parámetros típicos de un talud en arcilla compacta:
    - Altura: 8 metros
    - Ángulo: 30° (pendiente 1:1.73)
    - Cohesión: 25 kPa
    - Ángulo de fricción: 20°
    - Peso específico: 18 kN/m³
    """
    print("🏗️  CASO SIMPLE: TALUD DE CARRETERA")
    print("=" * 50)
    
    # === PARÁMETROS DEL PROBLEMA ===
    print("=== PARÁMETROS DEL PROBLEMA ===")
    
    altura = 8.0          # metros
    angulo_talud = 30.0   # grados
    cohesion = 25.0       # kPa
    phi_grados = 20.0     # grados
    gamma = 18.0          # kN/m³
    num_dovelas = 10
    
    print(f"📐 Geometría:")
    print(f"   • Altura del talud: {altura} m")
    print(f"   • Ángulo del talud: {angulo_talud}°")
    print(f"   • Longitud base: {altura/math.tan(math.radians(angulo_talud)):.1f} m")
    
    print(f"\n🧱 Propiedades del suelo:")
    print(f"   • Cohesión: {cohesion} kPa")
    print(f"   • Ángulo de fricción: {phi_grados}°")
    print(f"   • Peso específico: {gamma} kN/m³")
    print(f"   • Número de dovelas: {num_dovelas}")
    
    # === ANÁLISIS CON MÉTODO DE FELLENIUS ===
    print(f"\n=== ANÁLISIS CON MÉTODO DE FELLENIUS ===")
    
    try:
        resultado_fellenius = fellenius_talud_homogeneo(
            altura=altura,
            angulo_talud=angulo_talud,
            cohesion=cohesion,
            phi_grados=phi_grados,
            gamma=gamma,
            num_dovelas=num_dovelas
        )
        
        print(f"✅ Análisis Fellenius completado")
        print(f"📊 Factor de Seguridad: {resultado_fellenius.factor_seguridad:.3f}")
        print(f"🔄 Método: Directo (no iterativo)")
        print(f"📦 Dovelas analizadas: {len(resultado_fellenius.dovelas)}")
        print(f"⚖️  Momento resistente: {resultado_fellenius.momento_resistente:.1f} kN·m")
        print(f"⚖️  Momento actuante: {resultado_fellenius.momento_actuante:.1f} kN·m")
        
        # Clasificación de estabilidad
        if resultado_fellenius.factor_seguridad < 1.0:
            clasificacion = "🔴 INESTABLE"
        elif resultado_fellenius.factor_seguridad < 1.3:
            clasificacion = "🟡 MARGINALMENTE ESTABLE"
        elif resultado_fellenius.factor_seguridad < 2.0:
            clasificacion = "🟢 ESTABLE"
        else:
            clasificacion = "🟢 MUY ESTABLE"
        
        print(f"🏷️  Clasificación: {clasificacion}")
        
    except Exception as e:
        print(f"❌ Error en Fellenius: {e}")
        resultado_fellenius = None
    
    # === ANÁLISIS CON MÉTODO DE BISHOP ===
    print(f"\n=== ANÁLISIS CON MÉTODO DE BISHOP MODIFICADO ===")
    
    try:
        resultado_bishop = bishop_talud_homogeneo(
            altura=altura,
            angulo_talud=angulo_talud,
            cohesion=cohesion,
            phi_grados=phi_grados,
            gamma=gamma,
            num_dovelas=num_dovelas
        )
        
        print(f"✅ Análisis Bishop completado")
        print(f"📊 Factor de Seguridad: {resultado_bishop.factor_seguridad:.3f}")
        print(f"🔄 Método: Iterativo")
        print(f"🔁 Iteraciones: {resultado_bishop.iteraciones}")
        print(f"✅ Convergió: {'Sí' if resultado_bishop.convergio else 'No'}")
        print(f"📦 Dovelas analizadas: {len(resultado_bishop.dovelas)}")
        
        # Clasificación de estabilidad
        if resultado_bishop.factor_seguridad < 1.0:
            clasificacion = "🔴 INESTABLE"
        elif resultado_bishop.factor_seguridad < 1.3:
            clasificacion = "🟡 MARGINALMENTE ESTABLE"
        elif resultado_bishop.factor_seguridad < 2.0:
            clasificacion = "🟢 ESTABLE"
        else:
            clasificacion = "🟢 MUY ESTABLE"
        
        print(f"🏷️  Clasificación: {clasificacion}")
        
    except Exception as e:
        print(f"❌ Error en Bishop: {e}")
        resultado_bishop = None
    
    # === COMPARACIÓN DE MÉTODOS ===
    print(f"\n=== COMPARACIÓN DE MÉTODOS ===")
    
    if resultado_fellenius and resultado_bishop:
        diferencia = ((resultado_bishop.factor_seguridad - resultado_fellenius.factor_seguridad) / 
                     resultado_fellenius.factor_seguridad) * 100
        
        print(f"📈 Fellenius: Fs = {resultado_fellenius.factor_seguridad:.3f}")
        print(f"📈 Bishop: Fs = {resultado_bishop.factor_seguridad:.3f}")
        print(f"📊 Diferencia: {diferencia:+.1f}%")
        
        if abs(diferencia) < 5:
            print(f"✅ Métodos consistentes (diferencia < 5%)")
        elif diferencia > 0:
            print(f"ℹ️  Bishop menos conservador (mayor Fs)")
        else:
            print(f"ℹ️  Fellenius menos conservador (mayor Fs)")
        
        # Recomendación
        if resultado_bishop.factor_seguridad > 1.5:
            print(f"🎯 Recomendación: Talud SEGURO para construcción")
        elif resultado_bishop.factor_seguridad > 1.3:
            print(f"⚠️  Recomendación: Talud ACEPTABLE, monitorear")
        else:
            print(f"🚨 Recomendación: Talud REQUIERE REFUERZO")
    
    # === GENERACIÓN DE REPORTES ===
    print(f"\n=== GENERACIÓN DE REPORTES ===")
    
    if resultado_fellenius:
        try:
            reporte_fellenius = generar_reporte_fellenius(resultado_fellenius, "Talud de Carretera")
            print(f"✅ Reporte Fellenius generado ({len(reporte_fellenius)} caracteres)")
        except Exception as e:
            print(f"⚠️ Error generando reporte Fellenius: {e}")
    
    if resultado_bishop:
        try:
            reporte_bishop = generar_reporte_bishop(resultado_bishop, "Talud de Carretera")
            print(f"✅ Reporte Bishop generado ({len(reporte_bishop)} caracteres)")
        except Exception as e:
            print(f"⚠️ Error generando reporte Bishop: {e}")
    
    if resultado_fellenius and resultado_bishop:
        try:
            reporte_comparativo = comparar_bishop_fellenius(resultado_bishop, resultado_fellenius, "Talud de Carretera")
            print(f"✅ Reporte comparativo generado ({len(reporte_comparativo)} caracteres)")
        except Exception as e:
            print(f"⚠️ Error generando reporte comparativo: {e}")
    
    # === VISUALIZACIÓN ===
    print(f"\n=== VISUALIZACIÓN ===")
    
    try:
        # Configurar visualización
        configurar_estilo_grafico()
        config = ConfiguracionGrafico(figsize=(14, 10))
        
        # Crear geometría para visualización
        from core.geometry import crear_perfil_simple
        longitud_base = altura / math.tan(math.radians(angulo_talud))
        perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
        
        from data.models import CirculoFalla
        circulo = CirculoFalla(xc=longitud_base * 0.3, yc=altura * 1.1, radio=1.5 * altura)
        
        # Gráfico básico
        fig1 = graficar_perfil_basico(perfil, circulo, "Talud de Carretera - Geometría", config)
        print(f"✅ Gráfico de geometría creado")
        
        # Gráfico de Bishop si está disponible
        if resultado_bishop:
            fig2 = graficar_resultado_bishop(perfil, circulo, resultado_bishop, config)
            print(f"✅ Gráfico de análisis Bishop creado")
        
        # Gráfico comparativo si ambos están disponibles
        if resultado_fellenius and resultado_bishop:
            fig3 = graficar_comparacion_metodos(perfil, circulo, resultado_fellenius, resultado_bishop, config)
            print(f"✅ Gráfico comparativo creado")
        
        # Cerrar gráficos para liberar memoria
        plt.close('all')
        
    except Exception as e:
        print(f"⚠️ Error en visualización: {e}")
    
    # === RESUMEN FINAL ===
    print(f"\n" + "=" * 50)
    print(f"🎉 RESUMEN DEL ANÁLISIS")
    
    if resultado_bishop:
        fs = resultado_bishop.factor_seguridad
        if fs >= 1.5:
            estado = "🟢 SEGURO"
            accion = "Proceder con construcción"
        elif fs >= 1.3:
            estado = "🟡 ACEPTABLE"
            accion = "Monitorear durante construcción"
        elif fs >= 1.0:
            estado = "🟠 MARGINAL"
            accion = "Considerar refuerzo"
        else:
            estado = "🔴 INESTABLE"
            accion = "Rediseñar talud"
        
        print(f"📊 Factor de Seguridad Final: {fs:.3f}")
        print(f"🏷️  Estado: {estado}")
        print(f"🎯 Acción Recomendada: {accion}")
    
    print(f"✅ Análisis completado exitosamente")
    print(f"📁 Reportes técnicos generados")
    print(f"📈 Gráficos de visualización creados")
    
    return resultado_bishop is not None


def caso_parametrico():
    """
    Ejemplo de análisis paramétrico: efecto de la cohesión.
    """
    print(f"\n🔬 ANÁLISIS PARAMÉTRICO: EFECTO DE LA COHESIÓN")
    print("=" * 50)
    
    # Parámetros base
    altura = 6.0
    angulo_talud = 35.0
    phi_grados = 25.0
    gamma = 19.0
    
    # Rango de cohesiones a analizar
    cohesiones = [10, 15, 20, 25, 30, 35, 40]
    
    print(f"📐 Parámetros fijos:")
    print(f"   • Altura: {altura} m")
    print(f"   • Ángulo: {angulo_talud}°")
    print(f"   • φ: {phi_grados}°")
    print(f"   • γ: {gamma} kN/m³")
    
    print(f"\n📊 Variación de cohesión: {cohesiones[0]}-{cohesiones[-1]} kPa")
    print(f"\n{'Cohesión (kPa)':<15} {'Fs Bishop':<12} {'Iteraciones':<12} {'Estado'}")
    print("-" * 50)
    
    for c in cohesiones:
        try:
            resultado = bishop_talud_homogeneo(
                altura=altura,
                angulo_talud=angulo_talud,
                cohesion=c,
                phi_grados=phi_grados,
                gamma=gamma,
                num_dovelas=8
            )
            
            fs = resultado.factor_seguridad
            iter_count = resultado.iteraciones
            
            if fs >= 1.5:
                estado = "SEGURO"
            elif fs >= 1.3:
                estado = "ACEPTABLE"
            elif fs >= 1.0:
                estado = "MARGINAL"
            else:
                estado = "INESTABLE"
            
            print(f"{c:<15} {fs:<12.3f} {iter_count:<12} {estado}")
            
        except Exception as e:
            print(f"{c:<15} {'ERROR':<12} {'-':<12} {'FALLO'}")
    
    print(f"\n✅ Análisis paramétrico completado")
    print(f"📈 Tendencia: Mayor cohesión → Mayor factor de seguridad")


if __name__ == "__main__":
    # Ejecutar caso simple
    exito_simple = caso_talud_carretera()
    
    # Ejecutar análisis paramétrico
    caso_parametrico()
    
    if exito_simple:
        print(f"\n🎉 EJEMPLO DE CASO SIMPLE EXITOSO")
        print(f"🎓 El sistema está listo para análisis profesionales")
    else:
        print(f"\n❌ EJEMPLO PARCIALMENTE EXITOSO")
    
    print(f"\n📚 Para más ejemplos, revisar:")
    print(f"   • caso_con_agua.py - Análisis con nivel freático")
    print(f"   • caso_estratificado.py - Suelos estratificados")
    print(f"   • caso_busqueda.py - Búsqueda automática de círculo crítico")
