"""
OPTIMIZACIÓN FINAL: GEOMETRÍA CRÍTICA PARA FACTORES REALISTAS
Crear una geometría que produzca factores de seguridad profesionales (1.0-3.0)
"""

from data.models import CirculoFalla, Estrato
from core.bishop import analizar_bishop

def encontrar_geometria_critica():
    """
    Encuentra una geometría más crítica que genere factores de seguridad realistas.
    """
    print("=" * 80)
    print("🎯 BÚSQUEDA DE GEOMETRÍA CRÍTICA OPTIMIZADA")
    print("=" * 80)
    
    # Geometrías más críticas (círculos más grandes, masas más inestables)
    geometrias_test = [
        {
            "perfil": [(0, 20), (5, 20), (25, 0), (40, 0)],  # Talud más alto y empinado
            "circulo": CirculoFalla(xc=15, yc=10, radio=25),
            "descripcion": "Talud alto empinado"
        },
        {
            "perfil": [(0, 15), (10, 15), (30, 0), (40, 0)],  # Talud intermedio
            "circulo": CirculoFalla(xc=20, yc=8, radio=22),
            "descripcion": "Talud intermedio crítico"
        },
        {
            "perfil": [(0, 12), (8, 12), (28, 0), (40, 0)],   # Talud más crítico
            "circulo": CirculoFalla(xc=18, yc=6, radio=20),
            "descripcion": "Talud crítico optimizado"
        },
        {
            "perfil": [(0, 25), (3, 25), (23, 0), (40, 0)],   # Talud muy empinado
            "circulo": CirculoFalla(xc=12, yc=12, radio=20),
            "descripcion": "Talud muy empinado"
        },
        {
            "perfil": [(0, 18), (6, 18), (26, 2), (40, 2)],   # Talud con berma pequeña
            "circulo": CirculoFalla(xc=16, yc=10, radio=18),
            "descripcion": "Talud con berma crítica"
        }
    ]
    
    # Parámetros de suelo estándar para testing
    estrato_test = Estrato(cohesion=10.0, phi_grados=20.0, gamma=18.0, nombre="Test")
    
    geometrias_validas = []
    
    print(f"📊 ANÁLISIS DE GEOMETRÍAS CRÍTICAS:")
    print(f"{'Descripción':<25} {'Centro':<12} {'Radio':<6} {'FS':<6} {'Estado'}")
    print("-" * 70)
    
    for geom in geometrias_test:
        try:
            resultado = analizar_bishop(geom["circulo"], geom["perfil"], estrato_test, num_dovelas=8)
            
            if resultado.es_valido and resultado.convergio:
                fs = resultado.factor_seguridad
                
                # Evaluar si el factor es más realista
                if 1.0 <= fs <= 5.0:
                    estado = "✅ REALISTA"
                    geometrias_validas.append({
                        **geom,
                        "fs": fs,
                        "estrato": estrato_test
                    })
                elif fs < 1.0:
                    estado = "⚠️ INESTABLE"
                else:
                    estado = "❌ EXCESIVO"
                    
                print(f"{geom['descripcion']:<25} ({geom['circulo'].xc},{geom['circulo'].yc}){'':<3} {geom['circulo'].radio:<6} {fs:<6.3f} {estado}")
            else:
                print(f"{geom['descripcion']:<25} {'N/A':<12} {'N/A':<6} {'ERROR':<6} ❌ NO VÁLIDO")
                
        except Exception as e:
            print(f"{geom['descripcion']:<25} {'N/A':<12} {'N/A':<6} {'ERROR':<6} ❌ EXCEPCIÓN")
    
    return geometrias_validas

def optimizar_parametros_con_geometria_critica(geometrias_validas):
    """
    Optimiza parámetros de suelo usando las geometrías críticas encontradas.
    """
    if not geometrias_validas:
        print("❌ No hay geometrías válidas para optimizar")
        return None
    
    print(f"\n" + "=" * 80)
    print("🔧 OPTIMIZACIÓN DE PARÁMETROS CON GEOMETRÍA CRÍTICA")
    print("=" * 80)
    
    # Usar la mejor geometría (factor más bajo pero > 1.0)
    mejor_geometria = min(geometrias_validas, key=lambda x: x["fs"])
    
    print(f"🎯 Usando geometría: {mejor_geometria['descripcion']}")
    print(f"   Centro: ({mejor_geometria['circulo'].xc}, {mejor_geometria['circulo'].yc})")
    print(f"   Radio: {mejor_geometria['circulo'].radio}")
    print(f"   FS base: {mejor_geometria['fs']:.3f}")
    
    # Parámetros para obtener diferentes rangos de FS
    parametros_criticos = [
        # Para FS crítico (1.0-1.3)
        {"cohesion": 3.0, "phi": 12.0, "categoria": "CRÍTICO"},
        {"cohesion": 4.0, "phi": 15.0, "categoria": "CRÍTICO"},
        {"cohesion": 5.0, "phi": 16.0, "categoria": "CRÍTICO"},
        
        # Para FS estable (1.3-1.8)
        {"cohesion": 6.0, "phi": 18.0, "categoria": "ESTABLE"},
        {"cohesion": 8.0, "phi": 20.0, "categoria": "ESTABLE"},
        {"cohesion": 10.0, "phi": 22.0, "categoria": "ESTABLE"},
        
        # Para FS muy estable (1.8-3.0)
        {"cohesion": 12.0, "phi": 25.0, "categoria": "MUY_ESTABLE"},
        {"cohesion": 15.0, "phi": 28.0, "categoria": "MUY_ESTABLE"},
        {"cohesion": 18.0, "phi": 30.0, "categoria": "MUY_ESTABLE"}
    ]
    
    resultados_finales = {}
    
    print(f"\n📊 OPTIMIZACIÓN DE PARÁMETROS:")
    print(f"{'Categoría':<12} {'c(kPa)':<7} {'φ(°)':<5} {'FS':<6} {'Estado'}")
    print("-" * 50)
    
    for params in parametros_criticos:
        estrato = Estrato(
            cohesion=params["cohesion"],
            phi_grados=params["phi"],
            gamma=18.0,
            nombre=f"Optimizado {params['categoria']}"
        )
        
        try:
            resultado = analizar_bishop(
                mejor_geometria["circulo"], 
                mejor_geometria["perfil"], 
                estrato, 
                num_dovelas=8
            )
            
            if resultado.es_valido and resultado.convergio:
                fs = resultado.factor_seguridad
                
                # Clasificar resultado
                if params["categoria"] == "CRÍTICO" and 1.0 <= fs <= 1.3:
                    estado = "✅ PERFECTO"
                elif params["categoria"] == "ESTABLE" and 1.3 <= fs <= 1.8:
                    estado = "✅ PERFECTO"
                elif params["categoria"] == "MUY_ESTABLE" and 1.8 <= fs <= 3.0:
                    estado = "✅ PERFECTO"
                elif 1.0 <= fs <= 3.0:
                    estado = "✅ BUENO"
                else:
                    estado = "❌ FUERA RANGO"
                
                if estado.startswith("✅"):
                    if params["categoria"] not in resultados_finales or abs(fs - 1.5) < abs(resultados_finales[params["categoria"]]["fs"] - 1.5):
                        resultados_finales[params["categoria"]] = {
                            **params,
                            "fs": fs,
                            "geometria": mejor_geometria
                        }
                
                print(f"{params['categoria']:<12} {params['cohesion']:<7} {params['phi']:<5} {fs:<6.3f} {estado}")
            else:
                print(f"{params['categoria']:<12} {params['cohesion']:<7} {params['phi']:<5} {'ERROR':<6} ❌ NO VÁLIDO")
                
        except Exception as e:
            print(f"{params['categoria']:<12} {params['cohesion']:<7} {params['phi']:<5} {'ERROR':<6} ❌ EXCEPCIÓN")
    
    return resultados_finales

def generar_evaluaciones_finales(resultados_finales):
    """
    Genera el código final optimizado para las evaluaciones.
    """
    if not resultados_finales:
        print("❌ No se pudieron generar evaluaciones optimizadas")
        return
    
    print(f"\n" + "=" * 80)
    print("📝 EVALUACIONES GEOTÉCNICAS FINALES OPTIMIZADAS")
    print("=" * 80)
    
    # Mostrar resumen de parámetros optimizados
    print(f"🎯 PARÁMETROS FINALES OPTIMIZADOS:")
    for categoria, datos in resultados_finales.items():
        print(f"\n{categoria}:")
        print(f"   Cohesión: {datos['cohesion']} kPa")
        print(f"   Fricción: {datos['phi']}°")
        print(f"   FS: {datos['fs']:.3f}")
        print(f"   Geometría: {datos['geometria']['descripcion']}")
    
    # Generar código para implementar
    if "CRÍTICO" in resultados_finales:
        datos_critico = resultados_finales["CRÍTICO"]
        geometria = datos_critico["geometria"]
        
        print(f"\n💾 IMPLEMENTAR EN EVALS_GEOTECNICOS.PY:")
        print(f"```python")
        print(f"# GEOMETRÍA CRÍTICA OPTIMIZADA")
        print(f"perfil_terreno = {geometria['perfil']}")
        print(f"circulo = CirculoFalla(xc={geometria['circulo'].xc}, yc={geometria['circulo'].yc}, radio={geometria['circulo'].radio})")
        print(f"")
        print(f"# PARÁMETROS OPTIMIZADOS")
        print(f"estrato_critico = Estrato(cohesion={datos_critico['cohesion']}, phi_grados={datos_critico['phi']}, gamma=18.0, nombre='Crítico')")
        print(f"# FS esperado: {datos_critico['fs']:.3f}")
        print(f"```")
        
        return geometria, datos_critico
    
    return None, None

if __name__ == "__main__":
    # Fase 1: Encontrar geometrías críticas
    geometrias_validas = encontrar_geometria_critica()
    
    if geometrias_validas:
        # Fase 2: Optimizar parámetros
        resultados_finales = optimizar_parametros_con_geometria_critica(geometrias_validas)
        
        if resultados_finales:
            # Fase 3: Generar implementación final
            geometria_final, parametros_final = generar_evaluaciones_finales(resultados_finales)
            
            if geometria_final:
                print(f"\n✅ OPTIMIZACIÓN COMPLETADA EXITOSAMENTE")
                print(f"🚀 Listo para implementar en evaluaciones geotécnicas")
            else:
                print(f"\n⚠️ Optimización parcial completada")
        else:
            print(f"\n❌ No se pudieron optimizar parámetros")
    else:
        print(f"\n❌ No se encontraron geometrías críticas válidas")
