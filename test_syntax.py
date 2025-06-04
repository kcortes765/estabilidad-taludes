#!/usr/bin/env python3
"""
Test de sintaxis para verificar que todos los módulos se importan correctamente.
"""

try:
    from gui_examples import get_caso_ejemplo, get_nombres_casos
    print("✓ gui_examples importado correctamente")
    
    # Probar casos
    nombres = get_nombres_casos()
    print(f"✓ Casos disponibles: {len(nombres)}")
    for nombre in nombres:
        print(f"  - {nombre}")
    
    # Probar obtener caso
    caso = get_caso_ejemplo("Talud Estable - Carretera")
    if caso:
        print("✓ Caso de ejemplo obtenido correctamente")
        print(f"  Altura: {caso['altura']}")
        print(f"  Cohesión: {caso['cohesion']}")
        print(f"  Descripción: {caso['descripcion']}")
    
except Exception as e:
    print(f"✗ Error en gui_examples: {e}")

try:
    import gui_components
    print("✓ gui_components importado correctamente")
except Exception as e:
    print(f"✗ Error en gui_components: {e}")

try:
    import gui_dialogs
    print("✓ gui_dialogs importado correctamente")
except Exception as e:
    print(f"✗ Error en gui_dialogs: {e}")

print("\nTest completado.")
