"""
Casos con círculos críticos ajustados manualmente para obtener FS realistas
"""

from gui_examples import calcular_perfil_terreno

# Casos de ejemplo con círculos críticos más realistas
CASOS_EJEMPLO_CRITICOS = {
    "Talud Estable - Carretera": {
        "descripcion": "Talud típico de carretera con factor de seguridad alto",
        "altura": 8.0,
        "angulo_talud": 35.0,
        "cohesion": 35.0,
        "phi_grados": 30.0,
        "gamma": 19.0,
        "con_agua": False,
        "nivel_freatico": 0.0,
        # Círculo más crítico (más cerca del talud)
        "centro_x": 18.0,  # Más cerca del centro del talud
        "centro_y": 6.0,   # Más bajo, más crítico
        "radio": 15.0,    # Radio menor, más crítico
        "esperado": "Fs > 1.5 (ESTABLE)",
        "perfil_terreno": calcular_perfil_terreno(8.0, 35.0)
    },
    
    "Talud Marginal - Arcilla Blanda": {
        "descripcion": "Talud en arcilla blanda con factor de seguridad límite",
        "altura": 10.0,
        "angulo_talud": 45.0,
        "cohesion": 12.0,   # Cohesión baja
        "phi_grados": 20.0, # Ángulo de fricción bajo
        "gamma": 18.0,
        "con_agua": False,
        "nivel_freatico": 0.0,
        # Círculo crítico para suelo débil
        "centro_x": 16.0,
        "centro_y": 8.0,   # Más bajo para ser más crítico
        "radio": 14.0,    # Radio menor
        "esperado": "1.2 < Fs < 1.4 (MARGINAL)",
        "perfil_terreno": calcular_perfil_terreno(10.0, 45.0)
    },
    
    "Talud con Agua - Crítico": {
        "descripcion": "Talud con nivel freático alto, condición crítica",
        "altura": 8.0,
        "angulo_talud": 40.0,
        "cohesion": 20.0,
        "phi_grados": 25.0,
        "gamma": 18.0,
        "con_agua": True,
        "nivel_freatico": 6.0,  # Nivel freático alto
        # Círculo muy crítico para condición con agua
        "centro_x": 17.0,
        "centro_y": 5.0,   # Muy bajo, crítico
        "radio": 12.0,    # Radio pequeño, crítico
        "esperado": "Fs ≈ 1.0-1.2 (CRÍTICO)",
        "perfil_terreno": calcular_perfil_terreno(8.0, 40.0)
    },
    
    "Talud Moderado - Arena Densa": {
        "descripcion": "Talud en arena densa con parámetros moderados",
        "altura": 6.0,
        "angulo_talud": 30.0,
        "cohesion": 5.0,    # Arena con poca cohesión
        "phi_grados": 35.0, # Ángulo de fricción alto
        "gamma": 20.0,
        "con_agua": False,
        "nivel_freatico": 0.0,
        # Círculo para talud más suave pero con parámetros buenos
        "centro_x": 16.0,
        "centro_y": 4.0,   # Bajo para ser crítico
        "radio": 13.0,    # Radio moderado
        "esperado": "Fs > 2.0 (MUY ESTABLE)",
        "perfil_terreno": calcular_perfil_terreno(6.0, 30.0)
    }
}

def probar_casos_criticos():
    """Prueba los casos críticos"""
    from core.geometry import CirculoFalla, crear_dovelas, Estrato
    from core.bishop import analizar_bishop
    
    print("🎯 PRUEBA DE CASOS CRÍTICOS MANUALES")
    print("="*50)
    
    for nombre_caso, caso in CASOS_EJEMPLO_CRITICOS.items():
        print(f"\n📋 {nombre_caso}")
        print(f"   Objetivo: {caso['esperado']}")
        
        try:
            estrato = Estrato(
                cohesion=caso['cohesion'],
                phi_grados=caso['phi_grados'],
                gamma=caso['gamma']
            )
            
            circulo = CirculoFalla(
                xc=caso['centro_x'],
                yc=caso['centro_y'],
                radio=caso['radio']
            )
            
            dovelas = crear_dovelas(
                circulo=circulo,
                perfil_terreno=caso['perfil_terreno'],
                estrato=estrato,
                num_dovelas=10
            )
            
            resultado = analizar_bishop(
                circulo=circulo,
                perfil_terreno=caso['perfil_terreno'],
                estrato=estrato,
                num_dovelas=10
            )
            
            fs = resultado['factor_seguridad']
            print(f"   ✅ FS = {fs:.3f} ({len(dovelas)} dovelas)")
            
            # Evaluar si está en el rango esperado
            if "1.5" in caso['esperado'] and 1.5 <= fs <= 2.5:
                print(f"   🎯 PERFECTO: En rango esperado")
            elif "1.2" in caso['esperado'] and "1.4" in caso['esperado'] and 1.2 <= fs <= 1.4:
                print(f"   🎯 PERFECTO: En rango esperado")
            elif "1.0" in caso['esperado'] and "1.2" in caso['esperado'] and 1.0 <= fs <= 1.2:
                print(f"   🎯 PERFECTO: En rango esperado")
            elif "2.0" in caso['esperado'] and fs >= 2.0:
                print(f"   🎯 PERFECTO: En rango esperado")
            else:
                print(f"   ⚠️ AJUSTAR: Fuera del rango esperado")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")

if __name__ == "__main__":
    probar_casos_criticos()
