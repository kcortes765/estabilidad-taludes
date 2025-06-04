#!/usr/bin/env python3
"""
Diagnóstico preciso de los errores en la GUI de análisis de estabilidad.
"""

import sys
import traceback
from gui_examples import get_caso_ejemplo, get_nombres_casos
from gui_analysis import analizar_desde_gui

def diagnosticar_caso_especifico(nombre_caso):
    """Diagnosticar un caso específico paso a paso."""
    print(f"\n{'='*60}")
    print(f"DIAGNÓSTICO: {nombre_caso}")
    print(f"{'='*60}")
    
    try:
        # 1. Obtener parámetros
        print("1. Obteniendo parámetros del caso...")
        caso = get_caso_ejemplo(nombre_caso)
        
        print("   Parámetros:")
        for key, value in caso.items():
            if key != 'descripcion':
                print(f"     {key}: {value}")
        
        # 2. Intentar análisis con wrapper GUI
        print("\n2. Ejecutando análisis con wrapper GUI...")
        resultado = analizar_desde_gui(caso)
        
        # 3. Verificar resultado
        if resultado['valido']:
            print("   ✅ ANÁLISIS EXITOSO")
            print(f"     Bishop FS: {resultado['bishop'].factor_seguridad:.3f}")
            print(f"     Fellenius FS: {resultado['fellenius'].factor_seguridad:.3f}")
            return True
        else:
            print("   ❌ ANÁLISIS FALLÓ")
            print(f"     Error: {resultado.get('error', 'Error desconocido')}")
            
            # Mostrar detalles del error si están disponibles
            if 'detalles' in resultado:
                print(f"     Detalles: {resultado['detalles']}")
            
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR CRÍTICO: {str(e)}")
        print("   Traceback completo:")
        traceback.print_exc()
        return False

def analizar_error_suma_fuerzas():
    """Analizar específicamente el error de suma de fuerzas."""
    print(f"\n{'='*60}")
    print("ANÁLISIS DEL ERROR: Suma de fuerzas actuantes ≤ 0")
    print(f"{'='*60}")
    
    print("Este error indica que:")
    print("1. El círculo de falla no intersecta correctamente el terreno")
    print("2. Las dovelas no tienen peso suficiente (geometría inválida)")
    print("3. El círculo está mal posicionado respecto al talud")
    
    print("\nCausas comunes:")
    print("- Centro del círculo muy alto o muy bajo")
    print("- Radio muy pequeño o muy grande")
    print("- Círculo fuera del rango del perfil del terreno")
    print("- Ángulo del talud muy empinado para el círculo dado")

def proponer_correcciones():
    """Proponer correcciones para los casos problemáticos."""
    print(f"\n{'='*60}")
    print("PROPUESTAS DE CORRECCIÓN")
    print(f"{'='*60}")
    
    # Caso problemático identificado: Talud Marginal - Arcilla Blanda
    caso_original = get_caso_ejemplo("Talud Marginal - Arcilla Blanda")
    
    print("Caso problemático: Talud Marginal - Arcilla Blanda")
    print("Parámetros actuales:")
    print(f"  Altura: {caso_original['altura']} m")
    print(f"  Ángulo: {caso_original['angulo_talud']}°")
    print(f"  Centro: ({caso_original['centro_x']}, {caso_original['centro_y']})")
    print(f"  Radio: {caso_original['radio']} m")
    
    # Calcular correcciones basadas en la geometría del talud
    altura = caso_original['altura']
    angulo = caso_original['angulo_talud']
    
    # Nuevos parámetros más conservadores
    nuevo_centro_x = altura * 0.8  # Más cerca del pie del talud
    nuevo_centro_y = altura * 1.6  # Más bajo que el original
    nuevo_radio = altura * 1.8     # Radio más conservador
    
    print("\nParámetros corregidos propuestos:")
    print(f"  Centro: ({nuevo_centro_x:.1f}, {nuevo_centro_y:.1f})")
    print(f"  Radio: {nuevo_radio:.1f} m")
    
    return {
        'centro_x': nuevo_centro_x,
        'centro_y': nuevo_centro_y,
        'radio': nuevo_radio
    }

def main():
    """Función principal de diagnóstico."""
    print("DIAGNÓSTICO PRECISO DE ERRORES EN GUI")
    print("Análisis de Estabilidad de Taludes")
    print(f"{'='*60}")
    
    # 1. Diagnosticar todos los casos
    nombres_casos = get_nombres_casos()
    casos_exitosos = []
    casos_fallidos = []
    
    for nombre in nombres_casos:
        if diagnosticar_caso_especifico(nombre):
            casos_exitosos.append(nombre)
        else:
            casos_fallidos.append(nombre)
    
    # 2. Resumen de resultados
    print(f"\n{'='*60}")
    print("RESUMEN DE RESULTADOS")
    print(f"{'='*60}")
    
    print(f"Casos exitosos ({len(casos_exitosos)}):")
    for caso in casos_exitosos:
        print(f"  ✅ {caso}")
    
    print(f"\nCasos fallidos ({len(casos_fallidos)}):")
    for caso in casos_fallidos:
        print(f"  ❌ {caso}")
    
    # 3. Análisis del error principal
    if casos_fallidos:
        analizar_error_suma_fuerzas()
        
        # 4. Proponer correcciones
        correcciones = proponer_correcciones()
        
        print(f"\n{'='*60}")
        print("ACCIÓN REQUERIDA")
        print(f"{'='*60}")
        print("1. Corregir parámetros en gui_examples.py")
        print("2. Actualizar casos problemáticos con nuevos parámetros")
        print("3. Verificar que todos los casos pasen el diagnóstico")
        print("4. Probar la GUI nuevamente")
        
        return False
    else:
        print(f"\n🎉 TODOS LOS CASOS FUNCIONAN CORRECTAMENTE")
        print("La GUI debería funcionar sin errores.")
        return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nError inesperado en diagnóstico: {e}")
        traceback.print_exc()
        sys.exit(1)
