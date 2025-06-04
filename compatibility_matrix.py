"""
FASE 3: ANÁLISIS DE COMPATIBILIDAD GEOMÉTRICA
Encontrar geometrías que funcionen tanto para validación como para Bishop
"""

import math
from typing import List, Tuple, Optional
from data.models import CirculoFalla, Estrato, Dovela
from core.geometry import crear_dovelas
from core.bishop import calcular_fuerza_actuante_bishop, analizar_bishop

def probar_geometria_sistematica():
    """
    Prueba sistemáticamente diferentes geometrías para encontrar una que funcione.
    """
    print("=" * 100)
    print("🔍 BÚSQUEDA SISTEMÁTICA DE GEOMETRÍA VÁLIDA")
    print("=" * 100)
    
    # Perfil base simple
    perfil_base = [(0, 10), (10, 10), (20, 0), (40, 0)]
    estrato_base = Estrato(cohesion=15.0, phi_grados=20.0, gamma=18.0, nombre="Test")
    
    print("🏔️ Perfil del terreno fijo:")
    for x, y in perfil_base:
        print(f"   ({x}, {y})")
    
    # Matrices de búsqueda
    centros_x = [10, 15, 20, 25, 30]
    centros_y = [5, 10, 15, 20, 25]
    radios = [10, 15, 20, 25, 30]
    
    geometrias_validas = []
    
    print(f"\n🔬 TESTANDO {len(centros_x) * len(centros_y) * len(radios)} COMBINACIONES...")
    print(f"{'XC':<3} {'YC':<3} {'R':<3} {'Dovelas':<8} {'Suma_F':<8} {'FS':<6} {'Estado'}")
    print("-" * 50)
    
    contador = 0
    for xc in centros_x:
        for yc in centros_y:
            for radio in radios:
                contador += 1
                
                circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
                
                try:
                    # Verificar si puede generar dovelas
                    dovelas = crear_dovelas(circulo, perfil_base, estrato_base, num_dovelas=8)
                    
                    if len(dovelas) < 3:  # Muy pocas dovelas
                        estado = "❌ Pocas"
                        suma_f = "N/A"
                        fs = "N/A"
                    else:
                        # Calcular suma de fuerzas actuantes
                        fuerzas = [calcular_fuerza_actuante_bishop(d) for d in dovelas]
                        suma_f = sum(fuerzas)
                        
                        if suma_f <= 0:
                            estado = "❌ F≤0"
                            fs = "N/A"
                        else:
                            # Intentar análisis Bishop completo
                            try:
                                resultado = analizar_bishop(circulo, perfil_base, estrato_base, num_dovelas=8)
                                if resultado.es_valido and resultado.convergio:
                                    fs = resultado.factor_seguridad
                                    estado = "✅ VÁLIDA"
                                    geometrias_validas.append((xc, yc, radio, suma_f, fs, len(dovelas)))
                                else:
                                    estado = "❌ NoConv"
                                    fs = "N/A"
                            except Exception as e:
                                estado = f"❌ Error"
                                fs = "N/A"
                
                    print(f"{xc:<3} {yc:<3} {radio:<3} {len(dovelas) if 'dovelas' in locals() else 0:<8} "
                          f"{suma_f if isinstance(suma_f, (int, float)) else suma_f:<8} {fs:<6} {estado}")
                
                except Exception as e:
                    print(f"{xc:<3} {yc:<3} {radio:<3} {'0':<8} {'N/A':<8} {'N/A':<6} ❌ Error")
    
    # Reporte de geometrías válidas
    print(f"\n✅ GEOMETRÍAS VÁLIDAS ENCONTRADAS: {len(geometrias_validas)}")
    
    if geometrias_validas:
        print(f"\n🎯 MEJORES GEOMETRÍAS:")
        print(f"{'#':<2} {'Centro':<12} {'Radio':<6} {'Suma_F':<8} {'FS':<8} {'Dovelas':<8} {'Evaluación'}")
        print("-" * 70)
        
        # Ordenar por factor de seguridad realista (1.0-2.5)
        geometrias_ordenadas = sorted(geometrias_validas, 
                                    key=lambda x: abs(x[4] - 1.5) if 0.8 <= x[4] <= 3.0 else 999)
        
        for i, (xc, yc, radio, suma_f, fs, ndov) in enumerate(geometrias_ordenadas[:5]):
            # Evaluar realismo
            if 0.8 <= fs <= 3.0:
                evaluacion = "⭐ EXCELENTE"
            elif 0.5 <= fs <= 4.0:
                evaluacion = "✅ BUENO"
            else:
                evaluacion = "⚠️ Extremo"
                
            print(f"{i+1:<2} ({xc},{yc}){'':<7} {radio:<6} {suma_f:<8.1f} {fs:<8.3f} {ndov:<8} {evaluacion}")
        
        # Retornar la mejor geometría
        mejor = geometrias_ordenadas[0]
        return CirculoFalla(xc=mejor[0], yc=mejor[1], radio=mejor[2]), perfil_base, estrato_base
    
    else:
        print("❌ NO SE ENCONTRARON GEOMETRÍAS VÁLIDAS")
        return None, None, None

def probar_geometrias_alternativas():
    """
    Prueba geometrías con perfiles de terreno alternativos.
    """
    print(f"\n" + "=" * 100)
    print("🔄 PROBANDO PERFILES DE TERRENO ALTERNATIVOS")
    print("=" * 100)
    
    perfiles_test = [
        {
            "nombre": "Talud suave 3:1",
            "perfil": [(0, 15), (5, 15), (35, 5), (40, 5)],
            "circulo": CirculoFalla(xc=20, yc=25, radio=25)
        },
        {
            "nombre": "Talud escalonado",
            "perfil": [(0, 20), (10, 20), (15, 15), (25, 10), (40, 10)],
            "circulo": CirculoFalla(xc=20, yc=30, radio=25)
        },
        {
            "nombre": "Talud muy suave",
            "perfil": [(0, 12), (20, 8), (40, 8)],
            "circulo": CirculoFalla(xc=20, yc=20, radio=20)
        }
    ]
    
    estrato = Estrato(cohesion=15.0, phi_grados=20.0, gamma=18.0, nombre="Test")
    
    for config in perfiles_test:
        print(f"\n📊 {config['nombre']}:")
        
        try:
            resultado = analizar_bishop(config['circulo'], config['perfil'], estrato, num_dovelas=8)
            
            if resultado.es_valido and resultado.convergio:
                print(f"   ✅ VÁLIDO: FS = {resultado.factor_seguridad:.3f}")
                
                # Verificar suma de fuerzas
                dovelas = crear_dovelas(config['circulo'], config['perfil'], estrato, num_dovelas=8)
                fuerzas = [calcular_fuerza_actuante_bishop(d) for d in dovelas]
                suma = sum(fuerzas)
                print(f"   Suma fuerzas: {suma:.1f} kN")
                print(f"   Dovelas: {len(dovelas)}")
                
                if suma > 0:
                    print(f"   🎯 GEOMETRÍA ALTERNATIVA VÁLIDA ENCONTRADA!")
                    return config['circulo'], config['perfil'], estrato
            else:
                print(f"   ❌ Inválido o no convergió")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None, None, None

if __name__ == "__main__":
    # Búsqueda sistemática
    geometria_valida = probar_geometria_sistematica()
    
    if geometria_valida[0] is None:
        # Intentar perfiles alternativos
        geometria_valida = probar_geometrias_alternativas()
    
    if geometria_valida[0] is not None:
        print(f"\n🎉 GEOMETRÍA VÁLIDA FINAL ENCONTRADA:")
        print(f"   Centro: ({geometria_valida[0].xc}, {geometria_valida[0].yc})")
        print(f"   Radio: {geometria_valida[0].radio}")
        print(f"   Perfil: {geometria_valida[1]}")
        
        # Guardar para uso en evaluaciones
        print(f"\n💾 Esta geometría puede usarse en evals_geotecnicos.py")
    else:
        print(f"\n❌ NO SE ENCONTRÓ NINGUNA GEOMETRÍA VÁLIDA")
        print(f"💡 Posible problema en la implementación del método Bishop")
