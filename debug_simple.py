"""
Debug simple para entender exactamente qué está pasando
"""

from gui_examples import CASOS_EJEMPLO
from core.geometry import CirculoFalla, crear_dovelas, Estrato
from core.bishop import analizar_bishop
from core.fellenius import calcular_fuerza_actuante_dovela

# Tomar el primer caso
primer_caso = list(CASOS_EJEMPLO.items())[0]
nombre_caso, caso = primer_caso

print(f"🔍 DEBUG SIMPLE: {nombre_caso}")
print("="*50)

# Parámetros actuales
print(f"Centro actual: ({caso['centro_x']}, {caso['centro_y']})")
print(f"Radio actual: {caso['radio']}")
print(f"Perfil: {caso['perfil_terreno']}")

# Crear objetos
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

print(f"\n📐 ANÁLISIS GEOMÉTRICO:")
print(f"Círculo: centro=({circulo.xc}, {circulo.yc}), radio={circulo.radio}")

# Verificar intersección básica
perfil = caso['perfil_terreno']
x_min_perfil = min(p[0] for p in perfil)
x_max_perfil = max(p[0] for p in perfil)
y_max_perfil = max(p[1] for p in perfil)

x_min_circulo = circulo.xc - circulo.radio
x_max_circulo = circulo.xc + circulo.radio
y_min_circulo = circulo.yc - circulo.radio

print(f"Perfil X: {x_min_perfil} a {x_max_perfil}")
print(f"Círculo X: {x_min_circulo:.1f} a {x_max_circulo:.1f}")
print(f"Perfil Y máx: {y_max_perfil}")
print(f"Círculo Y mín: {y_min_circulo:.1f}")

# Verificar si hay intersección
interseccion_x = not (x_max_circulo < x_min_perfil or x_min_circulo > x_max_perfil)
interseccion_y = y_min_circulo < y_max_perfil

print(f"Intersección X: {interseccion_x}")
print(f"Intersección Y: {interseccion_y}")

if interseccion_x and interseccion_y:
    print("✅ Intersección básica OK")
else:
    print("❌ No hay intersección básica")

# Intentar crear dovelas
print(f"\n🔧 CREACIÓN DE DOVELAS:")
try:
    dovelas = crear_dovelas(
        circulo=circulo,
        perfil_terreno=perfil,
        estrato=estrato,
        num_dovelas=10
    )
    
    print(f"✅ Se crearon {len(dovelas)} dovelas")
    
    # Analizar cada dovela
    print(f"\nDETALLE DE DOVELAS:")
    suma_actuantes = 0
    for i, dovela in enumerate(dovelas):
        f_act = calcular_fuerza_actuante_dovela(dovela)
        suma_actuantes += f_act
        print(f"  Dovela {i}: X={dovela.x_centro:.1f}, h={dovela.altura:.2f}, α={dovela.angulo_alpha:.1f}°, F_act={f_act:.1f}")
    
    print(f"\nSuma fuerzas actuantes: {suma_actuantes:.1f}")
    
    if suma_actuantes > 0:
        print("✅ Fuerzas actuantes positivas")
        
        # Intentar análisis completo
        try:
            resultado = analizar_bishop(
                circulo=circulo,
                perfil_terreno=perfil,
                estrato=estrato,
                num_dovelas=10
            )
            print(f"✅ Análisis exitoso: FS = {resultado['factor_seguridad']:.3f}")
        except Exception as e:
            print(f"❌ Análisis falló: {e}")
    else:
        print("❌ Fuerzas actuantes negativas o cero")

except Exception as e:
    print(f"❌ Error creando dovelas: {e}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")

print(f"\n🎯 SUGERENCIAS:")
print(f"- Si no hay intersección: mover círculo")
print(f"- Si fuerzas negativas: bajar centro Y o cambiar radio")
print(f"- Si FS muy alto: círculo más crítico (más cerca del talud)")
