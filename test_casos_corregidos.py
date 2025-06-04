"""
Script de prueba para verificar que los casos de ejemplo corregidos funcionan sin errores
"""

import sys
import os

# Agregar el directorio actual al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_casos_corregidos():
    """
    Prueba todos los casos de ejemplo corregidos
    """
    print(" PRUEBA DE CASOS DE EJEMPLO CORREGIDOS")
    print("=" * 50)
    
    try:
        # Importar módulos necesarios
        from gui_examples import CASOS_EJEMPLO, get_nombres_casos
        from gui_analysis import analizar_desde_gui
        
        print(f" Casos disponibles: {len(CASOS_EJEMPLO)}")
        
        resultados = []
        
        for nombre_caso in get_nombres_casos():
            print(f"\n Probando caso: {nombre_caso}")
            
            try:
                # Obtener parámetros del caso
                caso = CASOS_EJEMPLO[nombre_caso]
                
                # Convertir a formato esperado por analizar_desde_gui
                parametros_gui = {
                    'altura': caso['altura'],
                    'angulo_talud': caso['angulo_talud'],
                    'cohesion': caso['cohesion'],
                    'phi_grados': caso['phi_grados'],
                    'gamma': caso['gamma'],
                    'con_agua': caso['con_agua'],
                    'nivel_freatico': caso['nivel_freatico'],
                    'centro_x': caso['centro_x'],
                    'centro_y': caso['centro_y'],
                    'radio': caso['radio'],
                    'perfil_terreno': caso['perfil_terreno']  # Usar el perfil precalculado
                }
                
                # Ejecutar análisis
                resultado = analizar_desde_gui(parametros_gui)
                
                if resultado['valido']:
                    fs_bishop = resultado['bishop']['factor_seguridad']
                    fs_fellenius = resultado['fellenius']['factor_seguridad']
                    
                    print(f" ")
                    print(f"   Factor de Seguridad Bishop: {fs_bishop:.3f}")
                    print(f"   Factor de Seguridad Fellenius: {fs_fellenius:.3f}")
                    print(f"   Esperado: {caso['esperado']}")
                    
                    # Clasificar resultado
                    if fs_bishop >= 1.5:
                        clasificacion = "ESTABLE"
                    elif fs_bishop >= 1.2:
                        clasificacion = "MARGINAL"
                    else:
                        clasificacion = "CRÍTICO"
                    
                    print(f"   Clasificación: {clasificacion}")
                    
                    resultados.append({
                        'nombre': nombre_caso,
                        'exito': True,
                        'fs_bishop': fs_bishop,
                        'fs_fellenius': fs_fellenius,
                        'clasificacion': clasificacion
                    })
                    
                else:
                    print(f"❌ ERROR: {resultado.get('error', 'Error desconocido')}")
                    resultados.append({
                        'nombre': nombre_caso,
                        'exito': False,
                        'error': resultado.get('error', 'Error desconocido')
                    })
                    
            except Exception as e:
                print(f" EXCEPCIÓN: {str(e)}")
                resultados.append({
                    'nombre': nombre_caso,
                    'exito': False,
                    'error': str(e)
                })
        
        # Resumen de resultados
        print("\n" + "=" * 50)
        print(" RESUMEN DE RESULTADOS")
        print("=" * 50)
        
        exitosos = sum(1 for r in resultados if r['exito'])
        total = len(resultados)
        
        print(f"Casos exitosos: {exitosos}/{total}")
        print(f"Tasa de éxito: {(exitosos/total)*100:.1f}%")
        
        if exitosos == total:
            print(" ¡TODOS LOS CASOS FUNCIONAN CORRECTAMENTE!")
        else:
            print("  Algunos casos requieren atención")
        
        # Detalles de casos exitosos
        print(f"\n CASOS EXITOSOS ({exitosos}):")
        for resultado in resultados:
            if resultado['exito']:
                print(f"  • {resultado['nombre']}: FS={resultado['fs_bishop']:.3f} ({resultado['clasificacion']})")
        
        # Detalles de casos fallidos
        casos_fallidos = [r for r in resultados if not r['exito']]
        if casos_fallidos:
            print(f"\n CASOS FALLIDOS ({len(casos_fallidos)}):")
            for resultado in casos_fallidos:
                print(f"  • {resultado['nombre']}: {resultado['error']}")
        
        return exitosos == total
        
    except ImportError as e:
        print(f" Error de importación: {e}")
        print("Verifique que todos los módulos estén disponibles")
        return False
    
    except Exception as e:
        print(f" Error inesperado: {e}")
        return False

def test_validacion_geometrica():
    """
    Prueba el sistema de validación geométrica
    """
    print("\n PRUEBA DE VALIDACIÓN GEOMÉTRICA")
    print("=" * 50)
    
    try:
        from validacion_geometrica import ValidadorGeometrico
        from gui_examples import CASOS_EJEMPLO
        
        for nombre_caso, caso in CASOS_EJEMPLO.items():
            print(f"\n Validando geometría: {nombre_caso}")
            
            # Crear validador con el perfil del caso
            validador = ValidadorGeometrico(caso['perfil_terreno'])
            
            # Validar parámetros del círculo
            resultado = validador.validar_parametros(
                caso['centro_x'],
                caso['centro_y'],
                caso['radio']
            )
            
            if resultado.es_valido:
                print(f" Geometría válida - {resultado.dovelas_validas_estimadas} dovelas estimadas")
            else:
                print(f" Geometría inválida - {resultado.mensaje}")
        
        return True
        
    except ImportError:
        print("  Módulo de validación geométrica no disponible")
        return False
    except Exception as e:
        print(f" Error en validación geométrica: {e}")
        return False

if __name__ == "__main__":
    print(" INICIANDO PRUEBAS COMPLETAS")
    print("=" * 60)
    
    # Ejecutar pruebas
    test1_ok = test_casos_corregidos()
    test2_ok = test_validacion_geometrica()
    
    print("\n" + "=" * 60)
    print(" RESULTADO FINAL")
    print("=" * 60)
    
    if test1_ok and test2_ok:
        print(" ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print(" Los casos de ejemplo están corregidos y funcionando")
        print(" La validación geométrica está operativa")
        print("\n La GUI debería funcionar sin errores de dovelas inválidas")
    else:
        print("  Algunas pruebas fallaron:")
        if not test1_ok:
            print(" Casos de ejemplo tienen problemas")
        if not test2_ok:
            print(" Validación geométrica tiene problemas")
        print("\n Revise los errores reportados arriba")
