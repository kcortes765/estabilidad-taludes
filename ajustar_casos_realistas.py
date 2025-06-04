"""
Script para ajustar manualmente los casos a factores de seguridad realistas
"""

from gui_examples import CASOS_EJEMPLO
from core.geometry import CirculoFalla, crear_dovelas, Estrato
from core.bishop import analizar_bishop

def probar_configuracion(caso, centro_x, centro_y, radio):
    """Prueba una configuración específica de círculo"""
    try:
        estrato = Estrato(
            cohesion=caso['cohesion'],
            phi_grados=caso['phi_grados'],
            gamma=caso['gamma']
        )
        
        circulo = CirculoFalla(xc=centro_x, yc=centro_y, radio=radio)
        
        dovelas = crear_dovelas(
            circulo=circulo,
            perfil_terreno=caso['perfil_terreno'],
            estrato=estrato,
            num_dovelas=10
        )
        
        if len(dovelas) < 5:
            return None
        
        resultado = analizar_bishop(
            circulo=circulo,
            perfil_terreno=caso['perfil_terreno'],
            estrato=estrato,
            num_dovelas=10
        )
        
        return {
            'centro_x': centro_x,
            'centro_y': centro_y,
            'radio': radio,
            'factor_seguridad': resultado['factor_seguridad'],
            'num_dovelas': len(dovelas)
        }
    except:
        return None

def ajustar_caso_realista(nombre_caso, caso):
    """Ajusta un caso para obtener un factor de seguridad realista"""
    print(f"\n🔧 Ajustando: {nombre_caso}")
    print(f"   Objetivo: {caso['esperado']}")
    
    # Configuraciones candidatas basadas en el objetivo esperado
    if "ESTABLE" in caso['esperado'] and "MUY" not in caso['esperado']:
        # FS objetivo: 1.5-2.5
        configuraciones = [
            (18, 6, 20), (20, 7, 22), (16, 5, 18), (22, 8, 24),
            (17, 6, 19), (19, 7, 21), (21, 8, 23), (15, 5, 17)
        ]
    elif "MARGINAL" in caso['esperado']:
        # FS objetivo: 1.2-1.4
        configuraciones = [
            (18, 5, 18), (20, 6, 20), (16, 4, 16), (22, 7, 22),
            (17, 5, 17), (19, 6, 19), (21, 7, 21), (15, 4, 15)
        ]
    elif "CRÍTICO" in caso['esperado']:
        # FS objetivo: 1.0-1.2
        configuraciones = [
            (18, 4, 16), (20, 5, 18), (16, 3, 14), (22, 6, 20),
            (17, 4, 15), (19, 5, 17), (21, 6, 19), (15, 3, 13)
        ]
    elif "MUY ESTABLE" in caso['esperado']:
        # FS objetivo: 2.0-3.0
        configuraciones = [
            (18, 8, 24), (20, 9, 26), (16, 7, 22), (22, 10, 28),
            (17, 8, 23), (19, 9, 25), (21, 10, 27), (15, 7, 21)
        ]
    else:
        # Configuración por defecto
        configuraciones = [(18, 6, 20), (20, 7, 22), (16, 5, 18)]
    
    mejor_config = None
    mejor_diferencia = float('inf')
    
    # Determinar FS objetivo numérico
    if "1.5" in caso['esperado']:
        fs_objetivo = 1.8
    elif "1.2" in caso['esperado'] and "1.4" in caso['esperado']:
        fs_objetivo = 1.3
    elif "1.0" in caso['esperado'] and "1.2" in caso['esperado']:
        fs_objetivo = 1.1
    elif "2.0" in caso['esperado']:
        fs_objetivo = 2.5
    else:
        fs_objetivo = 1.5
    
    print(f"   FS objetivo: {fs_objetivo:.1f}")
    
    for centro_x, centro_y, radio in configuraciones:
        resultado = probar_configuracion(caso, centro_x, centro_y, radio)
        
        if resultado:
            diferencia = abs(resultado['factor_seguridad'] - fs_objetivo)
            print(f"   Probando ({centro_x}, {centro_y}, {radio}): FS={resultado['factor_seguridad']:.3f}")
            
            if diferencia < mejor_diferencia:
                mejor_diferencia = diferencia
                mejor_config = resultado
    
    if mejor_config:
        print(f"   ✅ Mejor configuración: FS={mejor_config['factor_seguridad']:.3f}")
        print(f"      Centro: ({mejor_config['centro_x']}, {mejor_config['centro_y']})")
        print(f"      Radio: {mejor_config['radio']}")
        return mejor_config
    else:
        print(f"   ❌ No se encontró configuración válida")
        return None

def main():
    """Función principal"""
    print("🔧 AJUSTE DE CASOS A FACTORES DE SEGURIDAD REALISTAS")
    print("="*70)
    
    casos_ajustados = {}
    
    for nombre_caso, caso in CASOS_EJEMPLO.items():
        config_ajustada = ajustar_caso_realista(nombre_caso, caso)
        
        if config_ajustada:
            caso_ajustado = caso.copy()
            caso_ajustado['centro_x'] = config_ajustada['centro_x']
            caso_ajustado['centro_y'] = config_ajustada['centro_y']
            caso_ajustado['radio'] = config_ajustada['radio']
            casos_ajustados[nombre_caso] = caso_ajustado
        else:
            casos_ajustados[nombre_caso] = caso
    
    # Generar código final
    print(f"\n{'='*70}")
    print("📝 CÓDIGO FINAL CON FACTORES DE SEGURIDAD REALISTAS")
    print("="*70)
    
    print("# Casos de ejemplo con factores de seguridad realistas")
    print("CASOS_EJEMPLO = {")
    
    for nombre_caso, caso in casos_ajustados.items():
        print(f"    '{nombre_caso}': {{")
        print(f"        'descripcion': '{caso['descripcion']}',")
        print(f"        'altura': {caso['altura']},")
        print(f"        'angulo_talud': {caso['angulo_talud']},")
        print(f"        'cohesion': {caso['cohesion']},")
        print(f"        'phi_grados': {caso['phi_grados']},")
        print(f"        'gamma': {caso['gamma']},")
        print(f"        'con_agua': {caso['con_agua']},")
        print(f"        'nivel_freatico': {caso['nivel_freatico']},")
        print(f"        # Círculo ajustado para FS realista")
        print(f"        'centro_x': {caso['centro_x']:.1f},")
        print(f"        'centro_y': {caso['centro_y']:.1f},")
        print(f"        'radio': {caso['radio']:.1f},")
        print(f"        'esperado': '{caso.get('esperado', 'N/A')}',")
        print(f"        'perfil_terreno': {caso['perfil_terreno']}")
        print("    },")
    
    print("}")

if __name__ == "__main__":
    main()
