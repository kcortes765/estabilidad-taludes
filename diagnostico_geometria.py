#!/usr/bin/env python3
"""
Diagnóstico específico de problemas geométricos en análisis de estabilidad.
"""

import sys
import numpy as np
from data.models import CirculoFalla, Estrato
from core.geometry import crear_perfil_terreno, calcular_intersecciones_circulo_perfil
from core.bishop import analizar_bishop
from gui_examples import get_caso_ejemplo

def diagnosticar_caso(nombre_caso):
    """Diagnosticar un caso específico."""
    print(f"\n=== DIAGNÓSTICO: {nombre_caso} ===")
    
    try:
        # Obtener parámetros del caso
        caso = get_caso_ejemplo(nombre_caso)
        print(f"Parámetros del caso:")
        for key, value in caso.items():
            print(f"  {key}: {value}")
        
        # Crear objetos
        circulo = CirculoFalla(
            xc=caso['centro_x'],
            yc=caso['centro_y'], 
            radio=caso['radio']
        )
        
        estrato = Estrato(
            cohesion=caso['cohesion'],
            phi_grados=caso['phi_grados'],
            gamma=caso['gamma']
        )
        
        perfil = crear_perfil_terreno(
            altura=caso['altura'],
            angulo_grados=caso['angulo_talud']
        )
        
        print(f"\nObjetos creados:")
        print(f"  Círculo: centro=({circulo.xc:.1f}, {circulo.yc:.1f}), radio={circulo.radio:.1f}")
        print(f"  Perfil: {len(perfil.puntos)} puntos")
        print(f"  Estrato: c={estrato.cohesion}, φ={estrato.phi_grados}°, γ={estrato.gamma}")
        
        # Verificar intersecciones
        intersecciones = calcular_intersecciones_circulo_perfil(circulo, perfil)
        print(f"\nIntersecciones círculo-perfil: {len(intersecciones)}")
        for i, punto in enumerate(intersecciones):
            print(f"  {i+1}: ({punto.x:.2f}, {punto.y:.2f})")
        
        if len(intersecciones) < 2:
            print("❌ ERROR: Círculo no intersecta suficientemente el perfil")
            return False
        
        # Verificar geometría del círculo
        x_min = min(p.x for p in perfil.puntos)
        x_max = max(p.x for p in perfil.puntos)
        y_min = min(p.y for p in perfil.puntos)
        y_max = max(p.y for p in perfil.puntos)
        
        print(f"\nRangos del perfil:")
        print(f"  X: [{x_min:.1f}, {x_max:.1f}]")
        print(f"  Y: [{y_min:.1f}, {y_max:.1f}]")
        
        # Verificar si el círculo está bien posicionado
        if circulo.xc < x_min - circulo.radio or circulo.xc > x_max + circulo.radio:
            print("⚠️  ADVERTENCIA: Centro X del círculo muy alejado del perfil")
        
        if circulo.yc < y_max:
            print("⚠️  ADVERTENCIA: Centro Y del círculo muy bajo")
        
        # Intentar análisis
        print(f"\nIntentando análisis...")
        resultado = analizar_bishop(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            num_dovelas=10,
            validar_entrada=True
        )
        
        if resultado.es_valido:
            print(f"✅ ANÁLISIS EXITOSO")
            print(f"   Factor de Seguridad: {resultado.factor_seguridad:.3f}")
            print(f"   Dovelas válidas: {len(resultado.dovelas)}")
            print(f"   Convergencia: {resultado.convergencia_bishop} iteraciones")
        else:
            print(f"❌ ANÁLISIS FALLÓ")
            if hasattr(resultado, 'error'):
                print(f"   Error: {resultado.error}")
        
        return resultado.es_valido
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False

def proponer_correccion(nombre_caso):
    """Proponer corrección para un caso problemático."""
    print(f"\n=== PROPUESTA DE CORRECCIÓN: {nombre_caso} ===")
    
    caso = get_caso_ejemplo(nombre_caso)
    
    # Calcular geometría del perfil
    altura = caso['altura']
    angulo = caso['angulo_talud']
    
    # Calcular dimensiones aproximadas del talud
    base_talud = altura / np.tan(np.radians(angulo))
    
    # Proponer nuevo centro y radio
    nuevo_centro_x = base_talud * 0.6  # 60% de la base
    nuevo_centro_y = altura * 1.8      # 180% de la altura
    nuevo_radio = altura * 2.2         # 220% de la altura
    
    print(f"Parámetros actuales:")
    print(f"  Centro: ({caso['centro_x']:.1f}, {caso['centro_y']:.1f})")
    print(f"  Radio: {caso['radio']:.1f}")
    
    print(f"\nParámetros propuestos:")
    print(f"  Centro: ({nuevo_centro_x:.1f}, {nuevo_centro_y:.1f})")
    print(f"  Radio: {nuevo_radio:.1f}")
    
    return {
        'centro_x': nuevo_centro_x,
        'centro_y': nuevo_centro_y,
        'radio': nuevo_radio
    }

def main():
    """Función principal."""
    print("=== DIAGNÓSTICO COMPLETO DE GEOMETRÍA ===")
    
    casos_problematicos = []
    
    # Diagnosticar todos los casos
    from gui_examples import get_nombres_casos
    nombres = get_nombres_casos()
    
    for nombre in nombres:
        if diagnosticar_caso(nombre):
            print(f"✅ {nombre}: OK")
        else:
            print(f"❌ {nombre}: PROBLEMÁTICO")
            casos_problematicos.append(nombre)
    
    # Proponer correcciones
    if casos_problematicos:
        print(f"\n=== CASOS PROBLEMÁTICOS ENCONTRADOS ===")
        for nombre in casos_problematicos:
            correccion = proponer_correccion(nombre)
            print(f"\nCorreción para {nombre}:")
            print(f"  centro_x: {caso['centro_x']:.1f} → {correccion['centro_x']:.1f}")
            print(f"  centro_y: {caso['centro_y']:.1f} → {correccion['centro_y']:.1f}")
            print(f"  radio: {caso['radio']:.1f} → {correccion['radio']:.1f}")
    else:
        print(f"\n✅ TODOS LOS CASOS FUNCIONAN CORRECTAMENTE")

if __name__ == "__main__":
    main()
