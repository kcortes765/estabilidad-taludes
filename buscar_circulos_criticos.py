"""
Script para encontrar círculos críticos (factor de seguridad mínimo) para cada caso
"""

from gui_examples import CASOS_EJEMPLO
from core.geometry import CirculoFalla, crear_dovelas, Estrato
from core.fellenius import analizar_fellenius
from core.bishop import analizar_bishop
import math

def buscar_circulo_critico(caso, metodo='bishop'):
    """
    Busca el círculo crítico (FS mínimo) para un caso dado
    """
    print(f"\n🎯 Buscando círculo crítico para: {caso.get('descripcion', 'Sin descripción')}")
    
    estrato = Estrato(
        cohesion=caso['cohesion'],
        phi_grados=caso['phi_grados'],
        gamma=caso['gamma']
    )
    
    # Analizar el perfil para determinar límites de búsqueda
    perfil = caso['perfil_terreno']
    altura_max = max(p[1] for p in perfil)
    x_min = min(p[0] for p in perfil)
    x_max = max(p[0] for p in perfil)
    
    print(f"   Perfil: X={x_min:.1f} a {x_max:.1f}, altura_max={altura_max:.1f}")
    
    mejor_fs = float('inf')
    mejor_circulo = None
    
    # Búsqueda en grilla más fina para encontrar el círculo crítico
    for centro_x in range(int(x_min + 5), int(x_max - 5), 2):  # Cada 2m en X
        for centro_y in range(int(altura_max - 2), int(altura_max + 15), 2):  # Cada 2m en Y
            for radio in range(15, 35, 2):  # Cada 2m en radio
                
                try:
                    circulo = CirculoFalla(
                        xc=float(centro_x),
                        yc=float(centro_y),
                        radio=float(radio)
                    )
                    
                    # Verificar que el círculo intersecte bien el talud
                    dovelas = crear_dovelas(
                        circulo=circulo,
                        perfil_terreno=perfil,
                        estrato=estrato,
                        num_dovelas=10
                    )
                    
                    if len(dovelas) < 5:  # Necesitamos suficientes dovelas
                        continue
                    
                    # Ejecutar análisis
                    if metodo == 'bishop':
                        resultado = analizar_bishop(
                            circulo=circulo,
                            perfil_terreno=perfil,
                            estrato=estrato,
                            num_dovelas=10
                        )
                    else:
                        resultado = analizar_fellenius(
                            circulo=circulo,
                            perfil_terreno=perfil,
                            estrato=estrato,
                            num_dovelas=10
                        )
                    
                    fs = resultado['factor_seguridad']
                    
                    # Buscar el factor de seguridad mínimo (círculo crítico)
                    if 0.5 < fs < mejor_fs:  # FS razonable
                        mejor_fs = fs
                        mejor_circulo = {
                            'centro_x': float(centro_x),
                            'centro_y': float(centro_y),
                            'radio': float(radio),
                            'factor_seguridad': fs,
                            'num_dovelas': len(dovelas)
                        }
                
                except Exception:
                    continue
    
    if mejor_circulo:
        print(f"   ✅ Círculo crítico encontrado:")
        print(f"      Centro: ({mejor_circulo['centro_x']:.1f}, {mejor_circulo['centro_y']:.1f})")
        print(f"      Radio: {mejor_circulo['radio']:.1f}")
        print(f"      Factor de seguridad: {mejor_circulo['factor_seguridad']:.3f}")
        print(f"      Dovelas: {mejor_circulo['num_dovelas']}")
        return mejor_circulo
    else:
        print(f"   ❌ No se encontró círculo crítico válido")
        return None

def main():
    """Función principal"""
    print("🎯 BÚSQUEDA DE CÍRCULOS CRÍTICOS")
    print("="*60)
    
    casos_criticos = {}
    
    for nombre_caso, caso in CASOS_EJEMPLO.items():
        circulo_critico = buscar_circulo_critico(caso, metodo='bishop')
        
        if circulo_critico:
            # Crear caso con círculo crítico
            caso_critico = caso.copy()
            caso_critico['centro_x'] = circulo_critico['centro_x']
            caso_critico['centro_y'] = circulo_critico['centro_y']
            caso_critico['radio'] = circulo_critico['radio']
            
            casos_criticos[nombre_caso] = caso_critico
            
            # Mostrar cambios respecto al actual
            dx = abs(caso['centro_x'] - circulo_critico['centro_x'])
            dy = abs(caso['centro_y'] - circulo_critico['centro_y'])
            dr = abs(caso['radio'] - circulo_critico['radio'])
            
            print(f"      🎯 CÍRCULO CRÍTICO: FS={circulo_critico['factor_seguridad']:.3f}")
            print(f"         Cambios: Δx={dx:.1f}, Δy={dy:.1f}, Δr={dr:.1f}")
        else:
            casos_criticos[nombre_caso] = caso
            print(f"      ⚠️ MANTENER ACTUAL")
    
    # Generar código con círculos críticos
    print(f"\n{'='*60}")
    print("📝 CÓDIGO CON CÍRCULOS CRÍTICOS PARA gui_examples.py")
    print("="*60)
    
    print("# Casos de ejemplo con círculos críticos (FS mínimo)")
    print("CASOS_EJEMPLO = {")
    
    for nombre_caso, caso in casos_criticos.items():
        print(f"    '{nombre_caso}': {{")
        print(f"        'descripcion': '{caso['descripcion']}',")
        print(f"        'altura': {caso['altura']},")
        print(f"        'angulo_talud': {caso['angulo_talud']},")
        print(f"        'cohesion': {caso['cohesion']},")
        print(f"        'phi_grados': {caso['phi_grados']},")
        print(f"        'gamma': {caso['gamma']},")
        print(f"        'con_agua': {caso['con_agua']},")
        print(f"        'nivel_freatico': {caso['nivel_freatico']},")
        print(f"        # Círculo crítico (FS mínimo)")
        print(f"        'centro_x': {caso['centro_x']:.1f},")
        print(f"        'centro_y': {caso['centro_y']:.1f},")
        print(f"        'radio': {caso['radio']:.1f},")
        print(f"        'esperado': '{caso.get('esperado', 'N/A')}',")
        print(f"        'perfil_terreno': {caso['perfil_terreno']}")
        print("    },")
    
    print("}")

if __name__ == "__main__":
    main()
