from core.geometry import CirculoFalla
from data.validation import validar_geometria_circulo_avanzada

def test_simple_geometry_validation():
    print("\n--- Ejecutando test de validación de geometría simple ---")
    
    # Definir un perfil de terreno simple
    perfil = [
        (0, 10),
        (10, 10),
        (20, 0),
        (40, 0)
    ]
    
    # Geometría del caso 'Talud Simple Optimizado' de gui_examples.py
    circulo = CirculoFalla(xc=20, yc=-5, radio=20)
    
    print(f"Perfil de terreno: {perfil}")
    print(f"Círculo de falla: xc={circulo.xc}, yc={circulo.yc}, radio={circulo.radio}")
    
    resultado = validar_geometria_circulo_avanzada(circulo, perfil)
    
    if resultado.es_valido:
        print(f"✅ Validación exitosa: {resultado.mensaje}")
    else:
        print(f"❌ Validación fallida: {resultado.mensaje} (Código: {resultado.codigo_error})")
        
    assert resultado.es_valido, f"La geometría simple debería ser válida: {resultado.mensaje}"

if __name__ == "__main__":
    test_simple_geometry_validation()
