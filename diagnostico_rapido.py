#!/usr/bin/env python3
"""Diagnóstico rápido de problemas críticos."""

print("=== DIAGNÓSTICO RÁPIDO ===")

# Test 1: Importaciones básicas
print("\n1. Testando importaciones...")
try:
    from core.bishop import analizar_bishop
    print("✓ Bishop OK")
except Exception as e:
    print(f"✗ Bishop ERROR: {e}")

try:
    from gui_examples import get_caso_ejemplo
    caso = get_caso_ejemplo("Talud Estable - Carretera")
    print(f"✓ Ejemplo OK: {list(caso.keys())}")
except Exception as e:
    print(f"✗ Ejemplo ERROR: {e}")

# Test 2: Verificar función analizar_bishop
print("\n2. Verificando función analizar_bishop...")
import inspect
try:
    sig = inspect.signature(analizar_bishop)
    print(f"✓ Parámetros: {list(sig.parameters.keys())}")
except Exception as e:
    print(f"✗ ERROR: {e}")

# Test 3: Crear objetos básicos
print("\n3. Testando creación de objetos...")
try:
    from data.models import CirculoFalla, Estrato
    from core.geometry import crear_perfil_terreno
    
    circulo = CirculoFalla(xc=6.0, yc=12.0, radio=15.0)
    estrato = Estrato(cohesion=35.0, phi_grados=30.0, gamma=19.0)
    perfil = crear_perfil_terreno(altura=8.0, angulo_grados=35.0)
    
    print("✓ Objetos creados correctamente")
    print(f"  - Círculo: {circulo}")
    print(f"  - Estrato: {estrato}")
    print(f"  - Perfil: {len(perfil)} puntos")
    
    # Test 4: Análisis simple
    print("\n4. Testando análisis simple...")
    resultado = analizar_bishop(
        circulo=circulo,
        perfil_terreno=perfil,
        estrato=estrato,
        num_dovelas=10
    )
    print(f"✓ Análisis OK: Fs = {resultado.factor_seguridad:.3f}")
    print(f"  - Válido: {resultado.es_valido}")
    print(f"  - Dovelas: {len(resultado.dovelas)}")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Función wrapper GUI
print("\n5. Testando función wrapper GUI...")
try:
    from gui_analysis import analizar_desde_gui, validar_parametros_gui
    
    # Parámetros de prueba
    params_test = {
        'altura': 8.0,
        'angulo_talud': 35.0,
        'cohesion': 35.0,
        'phi_grados': 30.0,
        'gamma': 19.0,
        'con_agua': False,
        'nivel_freatico': 0.0,
        'centro_x': 6.0,
        'centro_y': 12.0,
        'radio': 15.0,
        'dovelas': 10
    }
    
    # Validar parámetros
    es_valido, mensaje = validar_parametros_gui(params_test)
    print(f"✓ Validación: {es_valido} - {mensaje}")
    
    # Ejecutar análisis
    resultado_gui = analizar_desde_gui(params_test)
    if resultado_gui['valido']:
        print(f"✓ Análisis GUI OK:")
        print(f"  - Bishop Fs: {resultado_gui['bishop'].factor_seguridad:.3f}")
        print(f"  - Fellenius Fs: {resultado_gui['fellenius'].factor_seguridad:.3f}")
    else:
        print(f"✗ Análisis GUI ERROR: {resultado_gui['error']}")
        
except Exception as e:
    print(f"✗ ERROR wrapper GUI: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Casos de ejemplo
print("\n6. Testando casos de ejemplo...")
try:
    from gui_examples import get_nombres_casos
    from gui_analysis import analizar_desde_gui
    
    nombres = get_nombres_casos()
    for nombre in nombres[:2]:  # Solo primeros 2
        try:
            caso = get_caso_ejemplo(nombre)
            resultado = analizar_desde_gui(caso)
            
            if resultado['valido']:
                print(f"✓ {nombre}: Bishop={resultado['bishop'].factor_seguridad:.3f}")
            else:
                print(f"✗ {nombre}: {resultado['error']}")
                
        except Exception as e:
            print(f"✗ {nombre}: ERROR - {e}")
            
except Exception as e:
    print(f"✗ ERROR casos ejemplo: {e}")

print("\n=== FIN DIAGNÓSTICO ===")
