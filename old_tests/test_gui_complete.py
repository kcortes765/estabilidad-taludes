#!/usr/bin/env python3
"""
Test completo de la aplicación GUI de análisis de estabilidad de taludes.
Identifica y reporta todos los problemas críticos.
"""

import sys
import traceback
from typing import Dict, Any, List

def test_imports():
    """Test de importaciones críticas."""
    print("=== TEST DE IMPORTACIONES ===")
    errors = []
    
    try:
        from core.bishop import analizar_bishop
        print("✓ core.bishop importado correctamente")
    except Exception as e:
        errors.append(f"✗ Error importando core.bishop: {e}")
    
    try:
        from core.fellenius import analizar_fellenius
        print("✓ core.fellenius importado correctamente")
    except Exception as e:
        errors.append(f"✗ Error importando core.fellenius: {e}")
    
    try:
        from gui_components import ParameterPanel, ToolsPanel, ResultsPanel, PlottingPanel
        print("✓ gui_components importado correctamente")
    except Exception as e:
        errors.append(f"✗ Error importando gui_components: {e}")
    
    try:
        from gui_examples import get_caso_ejemplo, get_nombres_casos
        print("✓ gui_examples importado correctamente")
    except Exception as e:
        errors.append(f"✗ Error importando gui_examples: {e}")
    
    return errors

def test_parameter_conversion():
    """Test de conversión de parámetros GUI a formato core."""
    print("\n=== TEST DE CONVERSIÓN DE PARÁMETROS ===")
    errors = []
    
    # Parámetros típicos de la GUI
    gui_params = {
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
    
    try:
        # Intentar conversión
        from data.models import CirculoFalla, Estrato
        from core.geometry import crear_perfil_terreno
        
        # Crear objetos necesarios
        circulo = CirculoFalla(
            centro_x=gui_params['centro_x'],
            centro_y=gui_params['centro_y'],
            radio=gui_params['radio']
        )
        
        estrato = Estrato(
            cohesion=gui_params['cohesion'],
            phi_grados=gui_params['phi_grados'],
            gamma=gui_params['gamma']
        )
        
        perfil = crear_perfil_terreno(
            altura=gui_params['altura'],
            angulo_grados=gui_params['angulo_talud']
        )
        
        print("✓ Conversión de parámetros exitosa")
        
        # Test de análisis Bishop
        from core.bishop import analizar_bishop
        resultado = analizar_bishop(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            num_dovelas=gui_params['dovelas']
        )
        
        print(f"✓ Análisis Bishop exitoso: Fs = {resultado.factor_seguridad:.3f}")
        
    except Exception as e:
        errors.append(f"✗ Error en conversión/análisis: {e}")
        traceback.print_exc()
    
    return errors

def test_gui_examples():
    """Test de casos de ejemplo de la GUI."""
    print("\n=== TEST DE CASOS DE EJEMPLO ===")
    errors = []
    
    try:
        from gui_examples import get_caso_ejemplo, get_nombres_casos
        
        nombres = get_nombres_casos()
        print(f"✓ Casos disponibles: {len(nombres)}")
        
        for nombre in nombres:
            try:
                caso = get_caso_ejemplo(nombre)
                if not caso:
                    errors.append(f"✗ Caso '{nombre}' retorna vacío")
                    continue
                
                # Verificar campos requeridos
                campos_requeridos = [
                    'altura', 'angulo_talud', 'cohesion', 'phi_grados', 'gamma',
                    'con_agua', 'nivel_freatico', 'centro_x', 'centro_y', 'radio'
                ]
                
                for campo in campos_requeridos:
                    if campo not in caso:
                        errors.append(f"✗ Caso '{nombre}' falta campo '{campo}'")
                
                print(f"✓ Caso '{nombre}' tiene estructura correcta")
                
            except Exception as e:
                errors.append(f"✗ Error procesando caso '{nombre}': {e}")
    
    except Exception as e:
        errors.append(f"✗ Error general en casos de ejemplo: {e}")
    
    return errors

def test_analysis_with_examples():
    """Test de análisis con casos de ejemplo."""
    print("\n=== TEST DE ANÁLISIS CON EJEMPLOS ===")
    errors = []
    
    try:
        from gui_examples import get_caso_ejemplo, get_nombres_casos
        from data.models import CirculoFalla, Estrato
        from core.geometry import crear_perfil_terreno
        from core.bishop import analizar_bishop
        
        nombres = get_nombres_casos()
        
        for nombre in nombres[:2]:  # Test solo primeros 2 casos
            try:
                caso = get_caso_ejemplo(nombre)
                
                # Crear objetos
                circulo = CirculoFalla(
                    centro_x=caso['centro_x'],
                    centro_y=caso['centro_y'],
                    radio=caso['radio']
                )
                
                estrato = Estrato(
                    cohesion=caso['cohesion'],
                    phi_grados=caso['phi_grados'],
                    gamma=caso['gamma']
                )
                
                perfil = crear_perfil_terreno(
                    altura=caso['altura'],
                    angulo_grados=caso['angulo_talud']
                )
                
                # Análisis
                resultado = analizar_bishop(
                    circulo=circulo,
                    perfil_terreno=perfil,
                    estrato=estrato,
                    num_dovelas=10
                )
                
                print(f"✓ Caso '{nombre}': Fs = {resultado.factor_seguridad:.3f}")
                
            except Exception as e:
                errors.append(f"✗ Error analizando caso '{nombre}': {e}")
                traceback.print_exc()
    
    except Exception as e:
        errors.append(f"✗ Error general en análisis: {e}")
    
    return errors

def test_plotting_compatibility():
    """Test de compatibilidad con plotting."""
    print("\n=== TEST DE COMPATIBILIDAD PLOTTING ===")
    errors = []
    
    try:
        # Crear resultado mock
        from data.models import CirculoFalla, Estrato, Dovela
        from core.geometry import crear_perfil_terreno
        
        # Crear dovelas mock
        dovelas = []
        for i in range(5):
            dovela = Dovela(
                x_centro=i * 2.0,
                ancho=2.0,
                altura_izq=5.0,
                altura_der=4.0,
                peso=100.0,
                angulo_base=30.0,
                area=10.0
            )
            dovelas.append(dovela)
        
        # Verificar que dovelas tienen atributo 'puntos' o similar
        if hasattr(dovelas[0], 'puntos'):
            print("✓ Dovelas tienen atributo 'puntos'")
        else:
            errors.append("✗ Dovelas no tienen atributo 'puntos' - problema plotting")
        
        print("✓ Test de plotting completado")
        
    except Exception as e:
        errors.append(f"✗ Error en test plotting: {e}")
    
    return errors

def create_wrapper_function():
    """Crear función wrapper para análisis desde GUI."""
    print("\n=== CREANDO FUNCIÓN WRAPPER ===")
    
    wrapper_code = '''
def analizar_desde_gui(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Wrapper para ejecutar análisis desde la GUI.
    Convierte parámetros de GUI al formato requerido por core.
    """
    from data.models import CirculoFalla, Estrato
    from core.geometry import crear_perfil_terreno
    from core.bishop import analizar_bishop
    from core.fellenius import analizar_fellenius
    
    try:
        # Crear objetos estructurados
        circulo = CirculoFalla(
            centro_x=params['centro_x'],
            centro_y=params['centro_y'],
            radio=params['radio']
        )
        
        estrato = Estrato(
            cohesion=params['cohesion'],
            phi_grados=params['phi_grados'],
            gamma=params['gamma']
        )
        
        perfil = crear_perfil_terreno(
            altura=params['altura'],
            angulo_grados=params['angulo_talud']
        )
        
        # Nivel freático si aplica
        nivel_freatico = None
        if params.get('con_agua', False) and params.get('nivel_freatico', 0) > 0:
            # Crear nivel freático
            pass  # Implementar según necesidad
        
        # Ejecutar análisis
        resultado_bishop = analizar_bishop(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            nivel_freatico=nivel_freatico,
            num_dovelas=params.get('dovelas', 10)
        )
        
        resultado_fellenius = analizar_fellenius(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            nivel_freatico=nivel_freatico,
            num_dovelas=params.get('dovelas', 10)
        )
        
        return {
            'bishop': resultado_bishop,
            'fellenius': resultado_fellenius,
            'valido': True
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'valido': False
        }
'''
    
    print("✓ Función wrapper creada")
    return wrapper_code

def main():
    """Ejecutar todos los tests."""
    print("INICIANDO TESTS COMPLETOS DE LA GUI")
    print("=" * 50)
    
    all_errors = []
    
    # Ejecutar tests
    all_errors.extend(test_imports())
    all_errors.extend(test_parameter_conversion())
    all_errors.extend(test_gui_examples())
    all_errors.extend(test_analysis_with_examples())
    all_errors.extend(test_plotting_compatibility())
    
    # Crear wrapper
    wrapper_code = create_wrapper_function()
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE TESTS")
    print("=" * 50)
    
    if all_errors:
        print(f"❌ ENCONTRADOS {len(all_errors)} ERRORES:")
        for i, error in enumerate(all_errors, 1):
            print(f"{i}. {error}")
    else:
        print("✅ TODOS LOS TESTS PASARON")
    
    print(f"\nFunción wrapper generada para integración GUI-Core")
    
    return all_errors, wrapper_code

if __name__ == "__main__":
    errors, wrapper = main()
    
    if errors:
        print(f"\n⚠️  SE REQUIERE CORRECCIÓN DE {len(errors)} PROBLEMAS")
        sys.exit(1)
    else:
        print("\n✅ SISTEMA LISTO PARA PRODUCCIÓN")
        sys.exit(0)
