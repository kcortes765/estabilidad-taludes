"""
Script para corregir los casos de ejemplo usando validación geométrica avanzada.

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
    
    # Crear validador para este perfil
    validador = ValidadorGeometrico(caso_original['perfil_terreno'])
    
    # Generar parámetros válidos
    params_validos = validador.generar_parametros_validos_ejemplo()
    
    # Crear caso corregido
    caso_corregido = caso_original.copy()
    caso_corregido['centro_x'] = params_validos['centro_x']
    caso_corregido['centro_y'] = params_validos['centro_y']
    caso_corregido['radio'] = params_validos['radio']
    
    # Validar caso corregido
    resultado_corregido = validar_caso_ejemplo(caso_corregido)
    print(f"Estado corregido: {resultado_corregido.mensaje}")
    print(f"Dovelas válidas estimadas: {resultado_corregido.dovelas_validas_estimadas}")
    
    print(f"Cambios realizados:")
    print(f"  Centro X: {caso_original['centro_x']:.2f} → {caso_corregido['centro_x']:.2f}")
    print(f"  Centro Y: {caso_original['centro_y']:.2f} → {caso_corregido['centro_y']:.2f}")
    print(f"  Radio: {caso_original['radio']:.2f} → {caso_corregido['radio']:.2f}")
    
    if resultado_corregido.es_valido:
        print("✅ Caso corregido exitosamente")
        return caso_corregido
    else:
        print("❌ No se pudo corregir el caso")
        return caso_original

def main():
    """Función principal para corregir todos los casos"""
    print("🔧 CORRECCIÓN AUTOMÁTICA DE CASOS DE EJEMPLO")
    print("=" * 50)
    
    casos_corregidos = []
    
    for caso in CASOS_EJEMPLO:
        caso_corregido = corregir_caso(caso)
        casos_corregidos.append(caso_corregido)
    
    # Mostrar resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE CORRECCIONES")
    print("=" * 50)
    
    for i, (original, corregido) in enumerate(zip(CASOS_EJEMPLO, casos_corregidos)):
        nombre = original['nombre']
        cambio_centro_x = abs(original['centro_x'] - corregido['centro_x'])
        cambio_centro_y = abs(original['centro_y'] - corregido['centro_y'])
        cambio_radio = abs(original['radio'] - corregido['radio'])
        
        if cambio_centro_x > 0.1 or cambio_centro_y > 0.1 or cambio_radio > 0.1:
            print(f"🔧 {nombre}: CORREGIDO")
        else:
            print(f"✅ {nombre}: YA VÁLIDO")
    
    # Generar código para gui_examples.py
    print("\n" + "=" * 50)
    print("📝 CÓDIGO CORREGIDO PARA gui_examples.py")
    print("=" * 50)
    
    print("CASOS_EJEMPLO = [")
    for caso in casos_corregidos:
        print("    {")
        print(f"        'nombre': '{caso['nombre']}',")
        print(f"        'descripcion': '{caso['descripcion']}',")
        print(f"        'perfil_terreno': {caso['perfil_terreno']},")
        print(f"        'cohesion': {caso['cohesion']},")
        print(f"        'angulo_friccion': {caso['angulo_friccion']},")
        print(f"        'peso_especifico': {caso['peso_especifico']},")
        print(f"        'centro_x': {caso['centro_x']:.2f},")
        print(f"        'centro_y': {caso['centro_y']:.2f},")
        print(f"        'radio': {caso['radio']:.2f},")
        print(f"        'nivel_freatico': {caso.get('nivel_freatico', 'None')}")
        print("    },")
    print("]")

if __name__ == "__main__":
    main()
