"""
CALIBRACIÓN ULTRA-FINA FINAL
Ajustar con precisión milimétrica para obtener factores profesionales exactos
"""

from data.models import CirculoFalla, Estrato
from core.bishop import analizar_bishop

def calibracion_ultra_precisa():
    """
    Calibración súper precisa para obtener factores exactos.
    """
    print("=" * 80)
    print("🎯 CALIBRACIÓN ULTRA-FINA PARA FACTORES PROFESIONALES EXACTOS")
    print("=" * 80)
    
    # Geometría válida establecida
    perfil_terreno = [(0, 10), (10, 10), (20, 0), (40, 0)]
    circulo = CirculoFalla(xc=15, yc=5, radio=30)
    
    # Parámetros ultra-precisos para rangos exactos
    configuraciones = [
        # Para FS ≈ 1.0-1.3 (crítico)
        {"c": 0.5, "phi": 3.0, "objetivo": "1.0-1.3", "tipo": "CRÍTICO"},
        {"c": 0.6, "phi": 4.0, "objetivo": "1.0-1.3", "tipo": "CRÍTICO"},
        {"c": 0.7, "phi": 5.0, "objetivo": "1.0-1.3", "tipo": "CRÍTICO"},
        
        # Para FS ≈ 1.3-1.8 (estable)
        {"c": 0.8, "phi": 6.0, "objetivo": "1.3-1.8", "tipo": "ESTABLE"},
        {"c": 1.0, "phi": 7.0, "objetivo": "1.3-1.8", "tipo": "ESTABLE"},
        {"c": 1.2, "phi": 8.0, "objetivo": "1.3-1.8", "tipo": "ESTABLE"},
        
        # Para FS ≈ 1.8-3.0 (muy estable)
        {"c": 1.5, "phi": 9.0, "objetivo": "1.8-3.0", "tipo": "MUY_ESTABLE"},
        {"c": 2.0, "phi": 10.0, "objetivo": "1.8-3.0", "tipo": "MUY_ESTABLE"},
        {"c": 2.5, "phi": 11.0, "objetivo": "1.8-3.0", "tipo": "MUY_ESTABLE"}
    ]
    
    resultados_perfectos = {"CRÍTICO": [], "ESTABLE": [], "MUY_ESTABLE": []}
    
    print(f"📊 CALIBRACIÓN ULTRA-PRECISA:")
    print(f"{'Tipo':<12} {'c(kPa)':<6} {'φ(°)':<5} {'FS':<6} {'Objetivo':<8} {'Estado'}")
    print("-" * 60)
    
    for config in configuraciones:
        estrato = Estrato(
            cohesion=config["c"],
            phi_grados=config["phi"],
            gamma=18.0,
            nombre=f"Cal-{config['tipo']}"
        )
        
        try:
            resultado = analizar_bishop(circulo, perfil_terreno, estrato, num_dovelas=8)
            
            if resultado.es_valido and resultado.convergio:
                fs = resultado.factor_seguridad
                
                # Evaluar precisión
                if config["tipo"] == "CRÍTICO" and 1.0 <= fs <= 1.3:
                    estado = "✅ PERFECTO"
                    resultados_perfectos["CRÍTICO"].append({**config, "fs": fs})
                elif config["tipo"] == "ESTABLE" and 1.3 <= fs <= 1.8:
                    estado = "✅ PERFECTO"
                    resultados_perfectos["ESTABLE"].append({**config, "fs": fs})
                elif config["tipo"] == "MUY_ESTABLE" and 1.8 <= fs <= 3.0:
                    estado = "✅ PERFECTO"
                    resultados_perfectos["MUY_ESTABLE"].append({**config, "fs": fs})
                else:
                    estado = "❌ FUERA RANGO"
                
                print(f"{config['tipo']:<12} {config['c']:<6} {config['phi']:<5} {fs:<6.3f} {config['objetivo']:<8} {estado}")
            else:
                print(f"{config['tipo']:<12} {config['c']:<6} {config['phi']:<5} {'ERROR':<6} {config['objetivo']:<8} ❌ NO VÁLIDO")
                
        except Exception as e:
            print(f"{config['tipo']:<12} {config['c']:<6} {config['phi']:<5} {'ERROR':<6} {config['objetivo']:<8} ❌ EXCEPCIÓN")
    
    return resultados_perfectos

def generar_codigo_final_optimizado(resultados_perfectos):
    """
    Genera el código final con los parámetros perfectamente calibrados.
    """
    print(f"\n" + "=" * 80)
    print("💎 PARÁMETROS PERFECTAMENTE CALIBRADOS")
    print("=" * 80)
    
    mejores = {}
    
    for tipo, resultados in resultados_perfectos.items():
        if resultados:
            # Elegir el más cercano al centro del rango
            if tipo == "CRÍTICO":
                objetivo = 1.15  # Centro de 1.0-1.3
            elif tipo == "ESTABLE":
                objetivo = 1.55  # Centro de 1.3-1.8
            else:  # MUY_ESTABLE
                objetivo = 2.4   # Centro de 1.8-3.0
            
            mejor = min(resultados, key=lambda x: abs(x["fs"] - objetivo))
            mejores[tipo] = mejor
            
            print(f"\n🎯 {tipo}:")
            print(f"   Cohesión: {mejor['c']} kPa")
            print(f"   Fricción: {mejor['phi']}°")
            print(f"   FS: {mejor['fs']:.3f}")
            print(f"   Error vs objetivo: {abs(mejor['fs'] - objetivo):.3f}")
    
    if mejores:
        print(f"\n💾 CÓDIGO FINAL PARA EVALS_GEOTECNICOS.PY:")
        print(f"```python")
        
        if "CRÍTICO" in mejores:
            m = mejores["CRÍTICO"]
            print(f"# EVAL 1: Parámetros críticos calibrados")
            print(f"estrato = Estrato(cohesion={m['c']}, phi_grados={m['phi']}, gamma=18.0)")
            print(f"# FS esperado: {m['fs']:.3f}")
            print()
        
        if "ESTABLE" in mejores:
            m = mejores["ESTABLE"]
            print(f"# EVAL 2: Parámetros estables calibrados")
            print(f"estrato = Estrato(cohesion={m['c']}, phi_grados={m['phi']}, gamma=18.0)")
            print(f"# FS esperado: {m['fs']:.3f}")
            print()
        
        print(f"# EVAL 3: Casos convergencia calibrados")
        for tipo in ["CRÍTICO", "ESTABLE", "MUY_ESTABLE"]:
            if tipo in mejores:
                m = mejores[tipo]
                print(f'{{\"nombre\": \"{tipo.title()}\", \"cohesion\": {m["c"]}, \"phi\": {m["phi"]}}},  # FS≈{m["fs"]:.3f}')
        
        print()
        print(f"# EVAL 4: Clasificación calibrada")
        for tipo in ["CRÍTICO", "ESTABLE", "MUY_ESTABLE"]:
            if tipo in mejores:
                m = mejores[tipo]
                nombre = tipo.lower().replace("_", " ")
                print(f'{{\"cohesion\": {m["c"]}, \"phi\": {m["phi"]}, \"nombre\": \"{nombre.title()}\"}},  # FS≈{m["fs"]:.3f}')
        
        print(f"```")
        
        return mejores
    
    return None

if __name__ == "__main__":
    # Calibración ultra-precisa
    resultados_perfectos = calibracion_ultra_precisa()
    
    # Generar código final
    mejores = generar_codigo_final_optimizado(resultados_perfectos)
    
    if mejores:
        print(f"\n✅ CALIBRACIÓN ULTRA-FINA COMPLETADA")
        print(f"🚀 Parámetros perfectos encontrados para {len(mejores)} categorías")
        print(f"📝 Implementar el código generado en evals_geotecnicos.py")
    else:
        print(f"\n❌ No se pudieron encontrar parámetros perfectos")
        print(f"🔄 Intentar con rangos más amplios")
