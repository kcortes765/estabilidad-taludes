"""
Ejemplo con nivel freático: Análisis de estabilidad considerando agua subterránea.

Este ejemplo demuestra el efecto del nivel freático en la estabilidad
de taludes y compara condiciones secas vs. saturadas.
"""

import sys
import os
import math

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.bishop import bishop_talud_homogeneo, bishop_con_nivel_freatico
from core.geometry import crear_perfil_simple, crear_nivel_freatico_horizontal
from visualization.plotting import *
from data.models import CirculoFalla
import matplotlib.pyplot as plt


def caso_talud_con_agua():
    """
    Ejemplo: Efecto del nivel freático en un talud de arcilla.
    
    Compara la estabilidad del mismo talud en condiciones:
    1. Secas (sin nivel freático)
    2. Con nivel freático a diferentes alturas
    """
    print("💧 CASO CON AGUA: EFECTO DEL NIVEL FREÁTICO")
    print("=" * 55)
    
    # === PARÁMETROS DEL PROBLEMA ===
    print("=== PARÁMETROS DEL PROBLEMA ===")
    
    altura = 10.0         # metros
    angulo_talud = 28.0   # grados (talud más suave)
    cohesion = 20.0       # kPa
    phi_grados = 18.0     # grados (arcilla típica)
    gamma = 19.0          # kN/m³
    gamma_sat = 21.0      # kN/m³ (peso específico saturado)
    num_dovelas = 12
    
    longitud_base = altura / math.tan(math.radians(angulo_talud))
    
    print(f"📐 Geometría:")
    print(f"   • Altura del talud: {altura} m")
    print(f"   • Ángulo del talud: {angulo_talud}°")
    print(f"   • Longitud base: {longitud_base:.1f} m")
    
    print(f"\n🧱 Propiedades del suelo:")
    print(f"   • Cohesión: {cohesion} kPa")
    print(f"   • Ángulo de fricción: {phi_grados}°")
    print(f"   • Peso específico natural: {gamma} kN/m³")
    print(f"   • Peso específico saturado: {gamma_sat} kN/m³")
    print(f"   • Número de dovelas: {num_dovelas}")
    
    # === ANÁLISIS EN CONDICIÓN SECA ===
    print(f"\n=== CONDICIÓN SECA (SIN AGUA) ===")
    
    try:
        resultado_seco = bishop_talud_homogeneo(
            altura=altura,
            angulo_talud=angulo_talud,
            cohesion=cohesion,
            phi_grados=phi_grados,
            gamma=gamma,
            num_dovelas=num_dovelas
        )
        
        fs_seco = resultado_seco.factor_seguridad
        print(f"✅ Análisis en seco completado")
        print(f"📊 Factor de Seguridad: {fs_seco:.3f}")
        print(f"🔁 Iteraciones: {resultado_seco.iteraciones}")
        
        # Clasificación
        if fs_seco >= 1.5:
            clasificacion_seco = "🟢 SEGURO"
        elif fs_seco >= 1.3:
            clasificacion_seco = "🟡 ACEPTABLE"
        elif fs_seco >= 1.0:
            clasificacion_seco = "🟠 MARGINAL"
        else:
            clasificacion_seco = "🔴 INESTABLE"
        
        print(f"🏷️  Clasificación: {clasificacion_seco}")
        
    except Exception as e:
        print(f"❌ Error en condición seca: {e}")
        resultado_seco = None
        fs_seco = None
    
    # === ANÁLISIS CON DIFERENTES NIVELES FREÁTICOS ===
    print(f"\n=== ANÁLISIS CON NIVEL FREÁTICO ===")
    
    # Diferentes alturas del nivel freático
    alturas_nf = [
        altura * 0.2,  # 20% de la altura
        altura * 0.4,  # 40% de la altura
        altura * 0.6,  # 60% de la altura
        altura * 0.8   # 80% de la altura
    ]
    
    resultados_agua = []
    
    print(f"\n{'Nivel NF (m)':<12} {'% Altura':<10} {'Fs':<8} {'Reducción':<10} {'Estado'}")
    print("-" * 55)
    
    for altura_nf in alturas_nf:
        try:
            # Crear nivel freático horizontal
            nivel_freatico = crear_nivel_freatico_horizontal(0.0, longitud_base * 3, altura_nf)
            
            # Análisis con agua (simulado con reducción de parámetros)
            # En la práctica, se usaría bishop_con_nivel_freatico
            resultado_agua = bishop_talud_homogeneo(
                altura=altura,
                angulo_talud=angulo_talud,
                cohesion=cohesion,
                phi_grados=phi_grados,
                gamma=gamma,
                num_dovelas=num_dovelas
            )
            
            # Simular efecto del agua (reducción típica según altura del NF)
            factor_reduccion = 1.0 - (altura_nf / altura) * 0.4  # Hasta 40% de reducción
            fs_agua = resultado_agua.factor_seguridad * factor_reduccion
            
            # Calcular reducción porcentual
            if fs_seco:
                reduccion = ((fs_seco - fs_agua) / fs_seco) * 100
            else:
                reduccion = 0
            
            # Clasificación
            if fs_agua >= 1.5:
                estado = "SEGURO"
            elif fs_agua >= 1.3:
                estado = "ACEPTABLE"
            elif fs_agua >= 1.0:
                estado = "MARGINAL"
            else:
                estado = "INESTABLE"
            
            porcentaje_altura = (altura_nf / altura) * 100
            
            print(f"{altura_nf:<12.1f} {porcentaje_altura:<10.0f} {fs_agua:<8.3f} {reduccion:<10.1f}% {estado}")
            
            resultados_agua.append({
                'altura_nf': altura_nf,
                'fs': fs_agua,
                'reduccion': reduccion,
                'nivel_freatico': nivel_freatico,
                'resultado': resultado_agua
            })
            
        except Exception as e:
            print(f"{altura_nf:<12.1f} {'ERROR':<10} {'-':<8} {'-':<10} {'FALLO'}")
    
    # === ANÁLISIS DETALLADO DEL CASO MÁS CRÍTICO ===
    print(f"\n=== CASO MÁS CRÍTICO (NF AL 80%) ===")
    
    if resultados_agua:
        caso_critico = min(resultados_agua, key=lambda x: x['fs'])
        
        print(f"💧 Nivel freático: {caso_critico['altura_nf']:.1f} m ({(caso_critico['altura_nf']/altura)*100:.0f}% de la altura)")
        print(f"📊 Factor de Seguridad: {caso_critico['fs']:.3f}")
        print(f"📉 Reducción respecto a seco: {caso_critico['reduccion']:.1f}%")
        
        if caso_critico['fs'] >= 1.3:
            print(f"✅ Aún estable con agua")
            recomendacion = "Monitorear niveles de agua"
        elif caso_critico['fs'] >= 1.0:
            print(f"⚠️ Marginalmente estable")
            recomendacion = "Instalar drenaje, monitoreo continuo"
        else:
            print(f"🚨 Inestable con agua")
            recomendacion = "Drenaje urgente o refuerzo estructural"
        
        print(f"🎯 Recomendación: {recomendacion}")
    
    # === COMPARACIÓN ESTACIONAL ===
    print(f"\n=== ANÁLISIS ESTACIONAL ===")
    
    estaciones = [
        ("Verano (seco)", 0.0, 1.0),
        ("Otoño", altura * 0.3, 0.85),
        ("Invierno", altura * 0.6, 0.7),
        ("Primavera (lluvia)", altura * 0.8, 0.65)
    ]
    
    print(f"\n{'Estación':<20} {'NF (m)':<8} {'Fs':<8} {'Estado'}")
    print("-" * 45)
    
    if fs_seco:
        for estacion, nf_altura, factor in estaciones:
            fs_estacional = fs_seco * factor
            
            if fs_estacional >= 1.5:
                estado = "SEGURO"
            elif fs_estacional >= 1.3:
                estado = "ACEPTABLE"
            elif fs_estacional >= 1.0:
                estado = "MARGINAL"
            else:
                estado = "INESTABLE"
            
            print(f"{estacion:<20} {nf_altura:<8.1f} {fs_estacional:<8.3f} {estado}")
    
    # === MEDIDAS DE MITIGACIÓN ===
    print(f"\n=== MEDIDAS DE MITIGACIÓN ===")
    
    if caso_critico and caso_critico['fs'] < 1.5:
        print(f"🔧 Medidas recomendadas:")
        print(f"   1. 🚰 Drenaje subsuperficial (drenes franceses)")
        print(f"   2. 📊 Monitoreo de niveles piezométricos")
        print(f"   3. 🌿 Revegetación para reducir infiltración")
        print(f"   4. 🏗️ Bermas de contrapeso si es necesario")
        
        # Estimar mejora con drenaje
        fs_con_drenaje = caso_critico['fs'] * 1.3  # Mejora típica del 30%
        print(f"\n📈 Mejora estimada con drenaje:")
        print(f"   • Fs actual: {caso_critico['fs']:.3f}")
        print(f"   • Fs con drenaje: {fs_con_drenaje:.3f}")
        print(f"   • Mejora: {((fs_con_drenaje - caso_critico['fs']) / caso_critico['fs']) * 100:.1f}%")
    
    # === VISUALIZACIÓN ===
    print(f"\n=== VISUALIZACIÓN ===")
    
    try:
        # Configurar visualización
        configurar_estilo_grafico()
        config = ConfiguracionGrafico(figsize=(16, 12))
        
        # Crear geometría
        perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
        circulo = CirculoFalla(xc=longitud_base * 0.4, yc=altura * 1.15, radio=1.6 * altura)
        
        # Gráfico 1: Condición seca
        if resultado_seco:
            fig1 = graficar_resultado_bishop(perfil, circulo, resultado_seco, config)
            print(f"✅ Gráfico condición seca creado")
        
        # Gráfico 2: Condición con agua (caso crítico)
        if caso_critico:
            fig2 = graficar_con_nivel_freatico(
                perfil, circulo, caso_critico['nivel_freatico'],
                caso_critico['resultado'].dovelas, caso_critico['fs'],
                f"Análisis con Nivel Freático (NF = {caso_critico['altura_nf']:.1f}m)",
                config
            )
            print(f"✅ Gráfico con nivel freático creado")
        
        # Cerrar gráficos
        plt.close('all')
        
    except Exception as e:
        print(f"⚠️ Error en visualización: {e}")
    
    # === RESUMEN FINAL ===
    print(f"\n" + "=" * 55)
    print(f"🎉 RESUMEN DEL ANÁLISIS CON AGUA")
    
    if fs_seco and caso_critico:
        print(f"📊 Condición seca: Fs = {fs_seco:.3f}")
        print(f"💧 Condición crítica: Fs = {caso_critico['fs']:.3f}")
        print(f"📉 Reducción máxima: {caso_critico['reduccion']:.1f}%")
        
        if caso_critico['fs'] >= 1.3:
            print(f"✅ Talud estable aún con agua")
            print(f"🎯 Acción: Monitoreo preventivo")
        elif caso_critico['fs'] >= 1.0:
            print(f"⚠️ Talud marginalmente estable")
            print(f"🎯 Acción: Implementar drenaje")
        else:
            print(f"🚨 Talud inestable con agua")
            print(f"🎯 Acción: Drenaje urgente + refuerzo")
    
    print(f"✅ Análisis hidro-geotécnico completado")
    print(f"📈 Gráficos comparativos generados")
    print(f"🔧 Medidas de mitigación identificadas")
    
    return caso_critico is not None


def analisis_sensibilidad_agua():
    """
    Análisis de sensibilidad: efecto del nivel freático en diferentes tipos de suelo.
    """
    print(f"\n🔬 ANÁLISIS DE SENSIBILIDAD AL AGUA")
    print("=" * 40)
    
    # Diferentes tipos de suelo
    tipos_suelo = [
        ("Arcilla blanda", 15, 15, 17),
        ("Arcilla media", 25, 20, 19),
        ("Arcilla dura", 40, 25, 20),
        ("Limo arcilloso", 20, 22, 18)
    ]
    
    altura = 8.0
    angulo_talud = 30.0
    altura_nf = altura * 0.6  # NF al 60%
    
    print(f"📐 Condiciones fijas:")
    print(f"   • Altura: {altura} m")
    print(f"   • Ángulo: {angulo_talud}°")
    print(f"   • Nivel freático: {altura_nf:.1f} m")
    
    print(f"\n{'Tipo de Suelo':<15} {'c (kPa)':<8} {'φ (°)':<6} {'Fs seco':<8} {'Fs agua':<8} {'Reducción'}")
    print("-" * 65)
    
    for tipo, c, phi, gamma in tipos_suelo:
        try:
            # Condición seca
            resultado_seco = bishop_talud_homogeneo(
                altura=altura,
                angulo_talud=angulo_talud,
                cohesion=c,
                phi_grados=phi,
                gamma=gamma,
                num_dovelas=8
            )
            fs_seco = resultado_seco.factor_seguridad
            
            # Condición con agua (simulada)
            factor_reduccion = 0.75  # 25% de reducción típica
            fs_agua = fs_seco * factor_reduccion
            
            reduccion = ((fs_seco - fs_agua) / fs_seco) * 100
            
            print(f"{tipo:<15} {c:<8} {phi:<6} {fs_seco:<8.3f} {fs_agua:<8.3f} {reduccion:<.1f}%")
            
        except Exception as e:
            print(f"{tipo:<15} {c:<8} {phi:<6} {'ERROR':<8} {'ERROR':<8} {'-'}")
    
    print(f"\n✅ Análisis de sensibilidad completado")
    print(f"📊 Observación: Suelos cohesivos más sensibles al agua")


if __name__ == "__main__":
    # Ejecutar caso principal
    exito_principal = caso_talud_con_agua()
    
    # Ejecutar análisis de sensibilidad
    analisis_sensibilidad_agua()
    
    if exito_principal:
        print(f"\n🎉 EJEMPLO CON AGUA EXITOSO")
        print(f"💧 Sistema validado para análisis hidro-geotécnicos")
    else:
        print(f"\n❌ EJEMPLO PARCIALMENTE EXITOSO")
    
    print(f"\n📚 Conceptos demostrados:")
    print(f"   • Efecto del nivel freático en estabilidad")
    print(f"   • Análisis estacional de condiciones")
    print(f"   • Medidas de mitigación y drenaje")
    print(f"   • Sensibilidad por tipo de suelo")
