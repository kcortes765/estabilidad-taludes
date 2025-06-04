"""
Script para corregir automáticamente la posición de los círculos de falla
para evitar fuerzas actuantes negativas
"""

from gui_examples import CASOS_EJEMPLO
from core.geometry import CirculoFalla, crear_dovelas, Estrato
from core.fellenius import calcular_fuerza_actuante_dovela
import math

def encontrar_circulo_valido(caso):
    """
    Encuentra un círculo válido que genere fuerzas actuantes positivas
    """
    print(f"\n🔍 Buscando círculo válido para: {caso.get('descripcion', 'Sin descripción')}")
    
    # Parámetros originales
    centro_x_orig = caso['centro_x']
    centro_y_orig = caso['centro_y']
    radio_orig = caso['radio']
    
    # Analizar el perfil para determinar límites
    perfil = caso['perfil_terreno']
    altura_max = max(p[1] for p in perfil)
    x_min = min(p[0] for p in perfil)
    x_max = max(p[0] for p in perfil)
    
    print(f"   Perfil: X={x_min:.1f} a {x_max:.1f}, altura_max={altura_max:.1f}")
    print(f"   Original: centro=({centro_x_orig}, {centro_y_orig}), radio={radio_orig}")
    
    estrato = Estrato(
        cohesion=caso['cohesion'],
        phi_grados=caso['phi_grados'],
        gamma=caso['gamma']
    )
    
    mejores_parametros = None
    mejor_suma_actuantes = -float('inf')
    
    # Buscar en una grilla de posiciones
    for dy in [-8, -6, -4, -2, 0, 2, 4]:  # Mover centro hacia abajo
        for dx in [-4, -2, 0, 2, 4]:  # Mover centro lateralmente
            for dr in [-4, -2, 0, 2, 4, 6]:  # Cambiar radio
                
                nuevo_centro_x = centro_x_orig + dx
                nuevo_centro_y = centro_y_orig + dy
                nuevo_radio = radio_orig + dr
                
                # Validaciones básicas
                if nuevo_radio < 10 or nuevo_radio > 50:
                    continue
                if nuevo_centro_y < 0 or nuevo_centro_y > altura_max + 20:
                    continue
                
                try:
                    # Crear círculo de prueba
                    circulo = CirculoFalla(
                        xc=nuevo_centro_x,
                        yc=nuevo_centro_y,
                        radio=nuevo_radio
                    )
                    
                    # Crear dovelas
                    dovelas = crear_dovelas(
                        circulo=circulo,
                        perfil_terreno=perfil,
                        estrato=estrato,
                        num_dovelas=10
                    )
                    
                    if len(dovelas) < 5:  # Necesitamos al menos 5 dovelas
                        continue
                    
                    # Calcular suma de fuerzas actuantes
                    suma_actuantes = sum(calcular_fuerza_actuante_dovela(d) for d in dovelas)
                    
                    # Buscar la mejor configuración (fuerzas actuantes más positivas)
                    if suma_actuantes > mejor_suma_actuantes:
                        mejor_suma_actuantes = suma_actuantes
                        mejores_parametros = {
                            'centro_x': nuevo_centro_x,
                            'centro_y': nuevo_centro_y,
                            'radio': nuevo_radio,
                            'suma_actuantes': suma_actuantes,
                            'num_dovelas': len(dovelas)
                        }
                
                except Exception:
                    continue
    
    if mejores_parametros and mejores_parametros['suma_actuantes'] > 0:
        print(f"   ✅ Círculo válido encontrado:")
        print(f"      Centro: ({mejores_parametros['centro_x']:.1f}, {mejores_parametros['centro_y']:.1f})")
        print(f"      Radio: {mejores_parametros['radio']:.1f}")
        print(f"      Fuerzas actuantes: {mejores_parametros['suma_actuantes']:.1f}")
        print(f"      Dovelas: {mejores_parametros['num_dovelas']}")
        return mejores_parametros
    else:
        print(f"   ❌ No se encontró círculo válido")
        return None

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN AUTOMÁTICA DE CÍRCULOS DE FALLA")
    print("="*60)
    
    casos_corregidos = {}
    
    for nombre_caso, caso in CASOS_EJEMPLO.items():
        parametros_validos = encontrar_circulo_valido(caso)
        
        if parametros_validos:
            # Crear caso corregido
            caso_corregido = caso.copy()
            caso_corregido['centro_x'] = parametros_validos['centro_x']
            caso_corregido['centro_y'] = parametros_validos['centro_y']
            caso_corregido['radio'] = parametros_validos['radio']
            
            casos_corregidos[nombre_caso] = caso_corregido
            
            # Mostrar cambios
            dx = abs(caso['centro_x'] - parametros_validos['centro_x'])
            dy = abs(caso['centro_y'] - parametros_validos['centro_y'])
            dr = abs(caso['radio'] - parametros_validos['radio'])
            
            if dx > 0.1 or dy > 0.1 or dr > 0.1:
                print(f"      🔧 CORREGIDO: Δx={dx:.1f}, Δy={dy:.1f}, Δr={dr:.1f}")
            else:
                print(f"      ✅ YA VÁLIDO")
        else:
            casos_corregidos[nombre_caso] = caso
            print(f"      ⚠️ MANTENER ORIGINAL")
    
    # Generar código corregido
    print(f"\n{'='*60}")
    print("📝 CÓDIGO CORREGIDO PARA gui_examples.py")
    print("="*60)
    
    print("# Casos de ejemplo con círculos corregidos")
    print("CASOS_EJEMPLO = {")
    
    for nombre_caso, caso in casos_corregidos.items():
        print(f"    '{nombre_caso}': {{")
        print(f"        'descripcion': '{caso['descripcion']}',")
        print(f"        'altura': {caso['altura']},")
        print(f"        'angulo_talud': {caso['angulo_talud']},")
        print(f"        'cohesion': {caso['cohesion']},")
        print(f"        'phi_grados': {caso['phi_grados']},")
        print(f"        'gamma': {caso['gamma']},")
        print(f"        'con_agua': {caso['con_agua']},")
        print(f"        'nivel_freatico': {caso['nivel_freatico']},")
        print(f"        # Parámetros del círculo corregidos para fuerzas válidas")
        print(f"        'centro_x': {caso['centro_x']:.1f},")
        print(f"        'centro_y': {caso['centro_y']:.1f},")
        print(f"        'radio': {caso['radio']:.1f},")
        print(f"        'esperado': '{caso.get('esperado', 'N/A')}',")
        print(f"        'perfil_terreno': {caso['perfil_terreno']}")
        print("    },")
    
    print("}")

if __name__ == "__main__":
    main()
