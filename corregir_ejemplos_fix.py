"""
Script para corregir los casos de ejemplo usando validación geométrica avanzada
"""

from validacion_geometrica import ValidadorGeometrico, validar_caso_ejemplo
from gui_examples import CASOS_EJEMPLO
import json

def corregir_caso(caso_original):
    """Corrige un caso usando validación geométrica"""
    print(f"\n=== Corrigiendo caso: {caso_original['nombre']} ===")
    
    # Validar caso original
    resultado_original = validar_caso_ejemplo(caso_original)
    print(f"Estado original: {resultado_original.mensaje}")
    print(f"Dovelas válidas estimadas: {resultado_original.dovelas_validas_estimadas}")
    
    if resultado_original.es_valido:
        print("✅ El caso ya es válido, no necesita corrección")
        return caso_original
    
    # Crear validador geométrico
    validador = ValidadorGeometrico(caso_original['perfil_terreno'])
    
    # Obtener rangos válidos
    rangos = validador.obtener_rangos_validos()
    print(f"Rangos válidos calculados:")
    print(f"  Centro X: {rangos['centro_x_min']:.2f} - {rangos['centro_x_max']:.2f}")
    print(f"  Centro Y: {rangos['centro_y_min']:.2f} - {rangos['centro_y_max']:.2f}")
    print(f"  Radio: {rangos['radio_min']:.2f} - {rangos['radio_max']:.2f}")
    
    # Generar parámetros válidos automáticamente
    params_validos = validador.generar_parametros_validos()
    
    # Crear caso corregido
    caso_corregido = caso_original.copy()
    caso_corregido.update({
        'centro_x': params_validos['centro_x'],
        'centro_y': params_validos['centro_y'],
        'radio': params_validos['radio']
    })
    
    # Validar caso corregido
    resultado_corregido = validar_caso_ejemplo(caso_corregido)
    print(f"Estado corregido: {resultado_corregido.mensaje}")
    print(f"Dovelas válidas estimadas: {resultado_corregido.dovelas_validas_estimadas}")
    
    if resultado_corregido.es_valido:
        print("✅ Corrección exitosa")
    else:
        print("❌ La corrección no fue suficiente")
    
    return caso_corregido

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN AUTOMÁTICA DE CASOS DE EJEMPLO")
    print("=" * 50)
    
    casos_corregidos = {}
    
    for nombre_caso, caso in CASOS_EJEMPLO.items():
        print(f"\n=== Procesando: {nombre_caso} ===")
        caso_con_nombre = caso.copy()
        caso_con_nombre['nombre'] = nombre_caso
        
        caso_corregido = corregir_caso(caso_con_nombre)
        casos_corregidos[nombre_caso] = caso_corregido
    
    # Mostrar resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE CORRECCIONES")
    print("=" * 50)
    
    for nombre_caso in CASOS_EJEMPLO.keys():
        original = CASOS_EJEMPLO[nombre_caso]
        corregido = casos_corregidos[nombre_caso]
        
        cambio_centro_x = abs(original['centro_x'] - corregido['centro_x'])
        cambio_centro_y = abs(original['centro_y'] - corregido['centro_y'])
        cambio_radio = abs(original['radio'] - corregido['radio'])
        
        if cambio_centro_x > 0.1 or cambio_centro_y > 0.1 or cambio_radio > 0.1:
            print(f"🔧 {nombre_caso}: CORREGIDO")
        else:
            print(f"✅ {nombre_caso}: YA VÁLIDO")
    
    # Generar código para gui_examples.py
    print("\n" + "=" * 50)
    print("📝 CÓDIGO CORREGIDO PARA gui_examples.py")
    print("=" * 50)
    
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
        print(f"        'centro_x': {caso['centro_x']:.2f},")
        print(f"        'centro_y': {caso['centro_y']:.2f},")
        print(f"        'radio': {caso['radio']:.2f},")
        print(f"        'esperado': '{caso.get('esperado', 'N/A')}',")
        print(f"        'perfil_terreno': {caso['perfil_terreno']}")
        print("    },")
    print("}")

if __name__ == "__main__":
    main()
