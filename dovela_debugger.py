"""
FASE 1: DIAGNÓSTICO PROFUNDO DE DOVELAS
Herramienta de debugging para identificar la causa raíz de errores geométricos
"""

import math
from typing import List, Tuple
from data.models import CirculoFalla, Estrato, Dovela
from core.geometry import crear_dovelas
from core.bishop import calcular_m_alpha

def debug_dovelas_completo(circulo: CirculoFalla, perfil_terreno: List[Tuple[float, float]], 
                          estrato: Estrato, num_dovelas: int = 10) -> None:
    """
    Analiza en detalle todas las dovelas generadas para identificar problemas geométricos.
    """
    print("=" * 80)
    print("🔬 DIAGNÓSTICO PROFUNDO DE DOVELAS")
    print("=" * 80)
    
    print(f"📐 GEOMETRÍA DEL CÍRCULO:")
    print(f"   Centro: ({circulo.xc}, {circulo.yc})")
    print(f"   Radio: {circulo.radio}")
    print(f"   Rango X teórico: [{circulo.xc - circulo.radio:.1f}, {circulo.xc + circulo.radio:.1f}]")
    
    print(f"\n🏔️ PERFIL DEL TERRENO:")
    for i, (x, y) in enumerate(perfil_terreno):
        print(f"   Punto {i+1}: ({x}, {y})")
    
    print(f"\n⚙️ PARÁMETROS DEL SUELO:")
    print(f"   Cohesión: {estrato.cohesion} kPa")
    print(f"   Ángulo de fricción: {estrato.phi_grados}°")
    print(f"   Peso específico: {estrato.gamma} kN/m³")
    
    try:
        # Generar dovelas
        print(f"\n🔧 GENERANDO {num_dovelas} DOVELAS...")
        dovelas = crear_dovelas(circulo, perfil_terreno, estrato, num_dovelas)
        
        print(f"✅ Se generaron {len(dovelas)} dovelas exitosamente")
        
        print(f"\n📊 ANÁLISIS DETALLADO DE DOVELAS:")
        print("-" * 120)
        print(f"{'#':<3} {'X_Centro':<8} {'Ancho':<6} {'Altura':<7} {'α(°)':<8} {'sin(α)':<8} {'cos(α)':<8} {'Peso':<8} {'Long_Arco':<9} {'mα@Fs=1':<8} {'Estado'}")
        print("-" * 120)
        
        dovelas_problematicas = []
        
        for i, dovela in enumerate(dovelas):
            angulo_grados = math.degrees(dovela.angulo_alpha)
            
            # Calcular mα con Fs=1.0 para diagnóstico
            try:
                m_alpha_test = calcular_m_alpha(dovela, 1.0)
                estado = "✅ OK" if m_alpha_test > 0 else "❌ mα≤0"
                if m_alpha_test <= 0:
                    dovelas_problematicas.append((i, dovela, m_alpha_test))
            except Exception as e:
                m_alpha_test = "ERROR"
                estado = f"❌ {str(e)[:20]}"
                dovelas_problematicas.append((i, dovela, "ERROR"))
            
            print(f"{i+1:<3} {dovela.x_centro:<8.2f} {dovela.ancho:<6.2f} {dovela.altura:<7.2f} "
                  f"{angulo_grados:<8.1f} {dovela.sin_alpha:<8.3f} {dovela.cos_alpha:<8.3f} "
                  f"{dovela.peso:<8.1f} {dovela.longitud_arco:<9.2f} {m_alpha_test:<8} {estado}")
        
        # Análisis estadístico
        print("\n📈 ESTADÍSTICAS GENERALES:")
        angulos = [math.degrees(d.angulo_alpha) for d in dovelas]
        print(f"   Ángulos α: min={min(angulos):.1f}°, max={max(angulos):.1f}°, promedio={sum(angulos)/len(angulos):.1f}°")
        
        alturas = [d.altura for d in dovelas]
        print(f"   Alturas: min={min(alturas):.2f}m, max={max(alturas):.2f}m, promedio={sum(alturas)/len(alturas):.2f}m")
        
        pesos = [d.peso for d in dovelas]
        print(f"   Pesos: min={min(pesos):.1f}kN, max={max(pesos):.1f}kN, total={sum(pesos):.1f}kN")
        
        # Análisis de dovelas problemáticas
        if dovelas_problematicas:
            print(f"\n⚠️ DOVELAS PROBLEMÁTICAS DETECTADAS: {len(dovelas_problematicas)}")
            print("-" * 80)
            for i, dovela, m_alpha in dovelas_problematicas:
                angulo_grados = math.degrees(dovela.angulo_alpha)
                print(f"   Dovela #{i+1}: X={dovela.x_centro:.2f}, α={angulo_grados:.1f}°, mα={m_alpha}")
                
                # Diagnóstico específico
                if angulo_grados < -45:
                    print(f"      🔍 PROBLEMA: Ángulo demasiado negativo ({angulo_grados:.1f}°)")
                elif angulo_grados > 45:
                    print(f"      🔍 PROBLEMA: Ángulo demasiado positivo ({angulo_grados:.1f}°)")
                    
                if dovela.altura <= 0:
                    print(f"      🔍 PROBLEMA: Altura inválida ({dovela.altura:.3f}m)")
        else:
            print(f"\n✅ TODAS LAS DOVELAS SON GEOMÉTRICAMENTE VÁLIDAS")
            
        # Análisis de fuerzas actuantes total
        print(f"\n⚖️ ANÁLISIS DE FUERZAS:")
        fuerzas_actuantes = [d.peso * d.sin_alpha for d in dovelas]
        suma_actuantes = sum(fuerzas_actuantes)
        print(f"   Fuerzas actuantes individuales: {[f'{f:.2f}' for f in fuerzas_actuantes]}")
        print(f"   Suma total de fuerzas actuantes: {suma_actuantes:.2f} kN")
        
        if suma_actuantes <= 0:
            print(f"   ❌ PROBLEMA CRÍTICO: Suma de fuerzas actuantes ≤ 0")
            # Identificar dovelas con fuerzas negativas
            dovelas_fuerza_negativa = [(i, d, f) for i, (d, f) in enumerate(zip(dovelas, fuerzas_actuantes)) if f < 0]
            if dovelas_fuerza_negativa:
                print(f"   Dovelas con fuerzas negativas:")
                for i, dovela, fuerza in dovelas_fuerza_negativa:
                    print(f"      Dovela #{i+1}: X={dovela.x_centro:.2f}, F_act={fuerza:.2f}kN, α={math.degrees(dovela.angulo_alpha):.1f}°")
        else:
            print(f"   ✅ Suma de fuerzas actuantes es positiva")
            
    except Exception as e:
        print(f"❌ ERROR AL GENERAR DOVELAS: {e}")
        return


def test_geometria_actual():
    """
    Prueba la geometría actual que está causando problemas.
    """
    # Geometría que actualmente causa problemas
    perfil = [
        (0, 10),
        (10, 10),
        (20, 0),
        (40, 0)
    ]
    circulo = CirculoFalla(xc=20, yc=-5, radio=20)
    estrato = Estrato(cohesion=15.0, phi_grados=20.0, gamma=18.0, nombre="Test")
    
    debug_dovelas_completo(circulo, perfil, estrato, num_dovelas=10)


if __name__ == "__main__":
    test_geometria_actual()
