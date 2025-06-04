"""
Módulo de análisis para la GUI.
Convierte parámetros de la GUI al formato requerido por el core.
"""

from typing import Dict, Any, Optional, List, Tuple
from data.models import CirculoFalla, Estrato
from core.geometry import crear_perfil_terreno, crear_nivel_freatico, validar_geometria_basica
from core.bishop import analizar_bishop
from core.fellenius import analizar_fellenius

# INTEGRACIÓN CON SISTEMA DE LÍMITES AUTOMÁTICOS
try:
    from core.circle_constraints import aplicar_limites_inteligentes, validar_circulo_con_limites
    LIMITES_DISPONIBLES = True
except ImportError:
    LIMITES_DISPONIBLES = False
    print(" Advertencia: Sistema de límites automáticos no disponible")


def validar_parametros_gui(params: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Valida parámetros de la GUI antes del análisis.
    
    Args:
        params: Diccionario con parámetros de la GUI
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    try:
        # Campos requeridos
        campos_requeridos = [
            'altura', 'angulo_talud', 'cohesion', 'phi_grados', 'gamma',
            'centro_x', 'centro_y', 'radio'
        ]
        
        for campo in campos_requeridos:
            if campo not in params:
                return False, f"Falta el campo requerido: {campo}"
            
            if not isinstance(params[campo], (int, float)):
                return False, f"El campo {campo} debe ser numérico"
        
        # Validaciones de rango
        if params['altura'] <= 0 or params['altura'] > 100:
            return False, "La altura debe estar entre 0 y 100 metros"
        
        if params['angulo_talud'] <= 0 or params['angulo_talud'] >= 90:
            return False, "El ángulo del talud debe estar entre 0 y 90 grados"
        
        if params['cohesion'] < 0 or params['cohesion'] > 200:
            return False, "La cohesión debe estar entre 0 y 200 kPa"
        
        if params['phi_grados'] < 0 or params['phi_grados'] > 50:
            return False, "El ángulo de fricción debe estar entre 0 y 50 grados"
        
        if params['gamma'] <= 0 or params['gamma'] > 30:
            return False, "El peso específico debe estar entre 0 y 30 kN/m³"
        
        if params['radio'] <= 0 or params['radio'] > params['altura'] * 5:
            return False, f"El radio debe estar entre 0 y {params['altura'] * 5} metros"
        
        # Validación geométrica
        if not validar_geometria_basica(
            params['altura'], params['angulo_talud'],
            params['centro_x'], params['centro_y'], params['radio']
        ):
            return False, "La geometría del círculo no es compatible con el talud"
        
        return True, "Parámetros válidos"
        
    except Exception as e:
        return False, f"Error validando parámetros: {e}"


def analizar_desde_gui(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta análisis completo desde parámetros de la GUI.
    
    NUEVO: Integra límites automáticos para evitar errores de configuración.
    
    Args:
        params: Diccionario con parámetros de la GUI
        
    Returns:
        Diccionario con resultados del análisis o error
    """
    try:
        # Validación inicial
        es_valido, mensaje = validar_parametros_gui(params)
        if not es_valido:
            return {
                'valido': False,
                'error': mensaje,
                'tipo_error': 'validacion'
            }
        
        # Crear perfil de terreno
        if 'perfil_terreno' in params and params['perfil_terreno']:
            perfil = params['perfil_terreno']
        else:
            perfil = crear_perfil_terreno(
                altura=params['altura'],
                angulo_grados=params['angulo_talud']
            )
        
        # APLICAR LÍMITES AUTOMÁTICOS ANTES DEL ANÁLISIS
        circulo_original = CirculoFalla(
            xc=params['centro_x'],
            yc=params['centro_y'],
            radio=params['radio']
        )
        
        circulo_final = circulo_original
        mensaje_limites = ""
        
        if LIMITES_DISPONIBLES:
            try:
                print(f" Aplicando límites automáticos para círculo: X={circulo_original.xc:.2f}, Y={circulo_original.yc:.2f}, R={circulo_original.radio:.2f}")
                
                # Determinar tipo de talud según ángulo
                angulo = params['angulo_talud']
                if angulo <= 30:
                    tipo_talud = "talud_suave"
                elif angulo <= 45:
                    tipo_talud = "talud_empinado"
                else:
                    tipo_talud = "talud_critico"
                
                print(f" Tipo de talud detectado: {tipo_talud} (ángulo: {angulo}°)")
                
                # Validar y corregir círculo usando el sistema automático
                resultado_validacion = validar_circulo_con_limites(
                    circulo=circulo_original,
                    perfil_terreno=perfil,
                    tipo_talud=tipo_talud
                )
                
                print(f" Resultado validación: válido={resultado_validacion.es_valido}")
                
                # Usar círculo corregido si es necesario
                if resultado_validacion.circulo_corregido:
                    circulo_final = resultado_validacion.circulo_corregido
                    print(f" Círculo CORREGIDO: X={circulo_final.xc:.2f}, Y={circulo_final.yc:.2f}, R={circulo_final.radio:.2f}")
                    mensaje_limites = "  Círculo corregido automáticamente para evitar errores geométricos"
                elif not resultado_validacion.es_valido:
                    print(f"  Violaciones detectadas: {resultado_validacion.violaciones}")
                    mensaje_limites = f"  Advertencias: {'; '.join(resultado_validacion.violaciones)}"
                else:
                    print(" Círculo original OK, no necesita corrección")
                
            except Exception as e:
                # Si falla el sistema de límites, continuar con círculo original
                print(f" Error en límites automáticos: {e}")
                import traceback
                traceback.print_exc()
                mensaje_limites = f"  No se pudieron aplicar límites automáticos: {e}"
        else:
            print("  Sistema de límites automáticos no disponible")
        
        # Crear objetos para análisis
        estrato = Estrato(
            cohesion=params['cohesion'],
            phi_grados=params['phi_grados'],
            gamma=params['gamma']
        )
        
        # Nivel freático si aplica
        nivel_freatico = None
        if params.get('con_agua', False) and params.get('nivel_freatico', 0) > 0:
            nivel_freatico = crear_nivel_freatico(
                altura_nf=params['nivel_freatico'],
                perfil_terreno=perfil
            )
        
        # Ejecutar análisis Bishop
        resultado_bishop = analizar_bishop(
            circulo=circulo_final,
            perfil_terreno=perfil,
            estrato=estrato,
            nivel_freatico=nivel_freatico,
            num_dovelas=params.get('dovelas', 10)
        )
        
        # Ejecutar análisis Fellenius
        resultado_fellenius = analizar_fellenius(
            circulo=circulo_final,
            perfil_terreno=perfil,
            estrato=estrato,
            nivel_freatico=nivel_freatico,
            num_dovelas=params.get('dovelas', 10)
        )
        
        # Preparar respuesta con información de límites
        respuesta = {
            'valido': True,
            'bishop': resultado_bishop,
            'fellenius': resultado_fellenius,
            'perfil_terreno': perfil,
            'nivel_freatico': nivel_freatico,
            'circulo': circulo_final,
            'estrato': estrato
        }
        
        # Agregar información sobre correcciones automáticas
        if mensaje_limites:
            respuesta['mensaje_limites'] = mensaje_limites
            respuesta['circulo_original'] = circulo_original
            respuesta['circulo_corregido'] = circulo_final != circulo_original
        
        return respuesta
        
    except Exception as e:
        import traceback
        return {
            'valido': False,
            'error': str(e),
            'tipo_error': 'analisis',
            'traceback': traceback.format_exc()
        }


def analizar_parametrico_gui(params_base: Dict[str, Any], 
                           parametro: str, 
                           valores: List[float]) -> Dict[str, Any]:
    """
    Ejecuta análisis paramétrico variando un parámetro.
    
    Args:
        params_base: Parámetros base
        parametro: Nombre del parámetro a variar
        valores: Lista de valores para el parámetro
        
    Returns:
        Diccionario con resultados del análisis paramétrico
    """
    resultados = []
    
    for valor in valores:
        # Crear copia de parámetros
        params_temp = params_base.copy()
        params_temp[parametro] = valor
        
        # Ejecutar análisis
        resultado = analizar_desde_gui(params_temp)
        
        if resultado['valido']:
            resultados.append({
                'valor': valor,
                'fs_bishop': resultado['bishop'].factor_seguridad,
                'fs_fellenius': resultado['fellenius'].factor_seguridad,
                'valido': True
            })
        else:
            resultados.append({
                'valor': valor,
                'error': resultado['error'],
                'valido': False
            })
    
    return {
        'parametro': parametro,
        'resultados': resultados,
        'valido': len([r for r in resultados if r['valido']]) > 0
    }


def buscar_fs_critico_gui(params_base: Dict[str, Any],
                         rango_centro_x: Tuple[float, float],
                         rango_centro_y: Tuple[float, float],
                         rango_radio: Tuple[float, float],
                         num_iteraciones: int = 100) -> Dict[str, Any]:
    """
    Busca el factor de seguridad crítico variando la posición del círculo.
    
    Args:
        params_base: Parámetros base
        rango_centro_x: Rango para centro X (min, max)
        rango_centro_y: Rango para centro Y (min, max)
        rango_radio: Rango para radio (min, max)
        num_iteraciones: Número de iteraciones
        
    Returns:
        Diccionario con el resultado de la búsqueda
    """
    import random
    
    min_fs = float('inf')
    mejor_config = None
    resultados_validos = 0
    
    for i in range(num_iteraciones):
        # Generar configuración aleatoria
        centro_x = random.uniform(rango_centro_x[0], rango_centro_x[1])
        centro_y = random.uniform(rango_centro_y[0], rango_centro_y[1])
        radio = random.uniform(rango_radio[0], rango_radio[1])
        
        # Crear parámetros temporales
        params_temp = params_base.copy()
        params_temp.update({
            'centro_x': centro_x,
            'centro_y': centro_y,
            'radio': radio
        })
        
        # Ejecutar análisis
        resultado = analizar_desde_gui(params_temp)
        
        if resultado['valido']:
            resultados_validos += 1
            fs_bishop = resultado['bishop'].factor_seguridad
            
            if fs_bishop < min_fs:
                min_fs = fs_bishop
                mejor_config = {
                    'centro_x': centro_x,
                    'centro_y': centro_y,
                    'radio': radio,
                    'fs_bishop': fs_bishop,
                    'fs_fellenius': resultado['fellenius'].factor_seguridad,
                    'resultado': resultado
                }
    
    return {
        'valido': mejor_config is not None,
        'fs_critico': min_fs if mejor_config else None,
        'mejor_config': mejor_config,
        'iteraciones_totales': num_iteraciones,
        'resultados_validos': resultados_validos,
        'tasa_exito': resultados_validos / num_iteraciones if num_iteraciones > 0 else 0
    }
