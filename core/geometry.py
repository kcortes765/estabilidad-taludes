"""
Funciones geométricas para análisis de estabilidad de taludes.

Este módulo contiene las funciones fundamentales para:
- Cálculos de intersección círculo-terreno
- Interpolación de perfiles de terreno
- Cálculo de ángulos y geometría de dovelas
- Discretización de círculos de falla en dovelas
"""

import math
from typing import List, Tuple, Optional
import numpy as np

from data.models import Dovela, CirculoFalla, Estrato


def calcular_y_circulo(x: float, xc: float, yc: float, radio: float, 
                      parte_superior: bool = True) -> Optional[float]:
    """
    Calcula la coordenada Y de un círculo para una coordenada X dada.
    
    Ecuación del círculo: (x - xc)² + (y - yc)² = r²
    Despejando y: y = yc ± √(r² - (x - xc)²)
    
    Args:
        x: Coordenada X donde calcular Y
        xc: Coordenada X del centro del círculo
        yc: Coordenada Y del centro del círculo
        radio: Radio del círculo
        parte_superior: Si True, devuelve la parte superior del círculo
        
    Returns:
        Coordenada Y del círculo, o None si X está fuera del círculo
    """
    # Verificar que X esté dentro del rango del círculo
    distancia_x = abs(x - xc)
    if distancia_x > radio:
        return None
    
    # Calcular discriminante
    discriminante = radio**2 - (x - xc)**2
    if discriminante < 0:
        return None
    
    # Calcular Y
    sqrt_discriminante = math.sqrt(discriminante)
    if parte_superior:
        return yc + sqrt_discriminante
    else:
        return yc - sqrt_discriminante


def interpolar_terreno(x: float, perfil_terreno: List[Tuple[float, float]]) -> float:
    """
    Interpola la elevación del terreno en una coordenada X dada.
    
    Usa interpolación lineal entre los puntos del perfil.
    
    Args:
        x: Coordenada X donde interpolar
        perfil_terreno: Lista de tuplas (x, y) que definen el perfil
        
    Returns:
        Elevación Y interpolada del terreno
        
    Raises:
        ValueError: Si X está fuera del rango del perfil o perfil inválido
    """
    if len(perfil_terreno) < 2:
        raise ValueError("El perfil debe tener al menos 2 puntos")
    
    # Ordenar perfil por X (por si acaso)
    perfil_ordenado = sorted(perfil_terreno, key=lambda punto: punto[0])
    
    x_min = perfil_ordenado[0][0]
    x_max = perfil_ordenado[-1][0]
    
    # Verificar que X esté dentro del rango
    if x < x_min or x > x_max:
        raise ValueError(f"X={x} está fuera del rango del perfil [{x_min}, {x_max}]")
    
    # Buscar el segmento donde está X
    for i in range(len(perfil_ordenado) - 1):
        x1, y1 = perfil_ordenado[i]
        x2, y2 = perfil_ordenado[i + 1]
        
        if x1 <= x <= x2:
            # Interpolación lineal
            if x2 == x1:  # Evitar división por cero
                return y1
            
            factor = (x - x1) / (x2 - x1)
            return y1 + factor * (y2 - y1)
    
    # Si llegamos aquí, algo salió mal
    raise ValueError(f"No se pudo interpolar para X={x}")


def calcular_angulo_alpha(x: float, xc: float, yc: float, radio: float) -> float:
    """
    Calcula el ángulo α de la tangente al círculo en un punto X.
    
    El ángulo α es el ángulo que forma la tangente al círculo con la horizontal.
    Se mide positivo en sentido antihorario desde la horizontal.
    
    Args:
        x: Coordenada X del punto en el círculo
        xc: Coordenada X del centro del círculo
        yc: Coordenada Y del centro del círculo
        radio: Radio del círculo
        
    Returns:
        Ángulo α en radianes
        
    Raises:
        ValueError: Si el punto está fuera del círculo
    """
    # Verificar que X esté dentro del círculo
    distancia_x = abs(x - xc)
    if distancia_x > radio:
        raise ValueError(f"X={x} está fuera del círculo (centro={xc}, radio={radio})")
    
    # Calcular el ángulo del radio desde el centro hasta el punto
    # θ = arcsin((x - xc) / r)
    sin_theta = (x - xc) / radio
    
    # Limitar el valor para evitar errores numéricos
    sin_theta = max(-1.0, min(1.0, sin_theta))
    
    theta = math.asin(sin_theta)
    
    # El ángulo α de la tangente es θ + π/2 (perpendicular al radio)
    # Pero necesitamos el ángulo medido desde la horizontal hacia abajo
    alpha = theta
    
    return alpha


def calcular_longitud_arco(x1: float, x2: float, xc: float, yc: float, radio: float) -> float:
    """
    Calcula la longitud del arco de círculo entre dos coordenadas X.
    
    Args:
        x1: Coordenada X inicial
        x2: Coordenada X final
        xc: Coordenada X del centro del círculo
        yc: Coordenada Y del centro del círculo
        radio: Radio del círculo
        
    Returns:
        Longitud del arco en metros
    """
    # Calcular ángulos correspondientes a x1 y x2
    try:
        # Ángulos desde el centro del círculo
        theta1 = math.asin((x1 - xc) / radio)
        theta2 = math.asin((x2 - xc) / radio)
        
        # Diferencia angular
        delta_theta = abs(theta2 - theta1)
        
        # Longitud del arco = radio * ángulo
        longitud_arco = radio * delta_theta
        
        return longitud_arco
        
    except (ValueError, ZeroDivisionError):
        # Si hay problemas, usar aproximación lineal
        return abs(x2 - x1)


def calcular_altura_dovela(x: float, ancho: float, perfil_terreno: List[Tuple[float, float]], 
                          xc: float, yc: float, radio: float) -> float:
    """
    Calcula la altura de una dovela desde el terreno hasta el círculo de falla.
    
    Args:
        x: Coordenada X del centro de la dovela
        ancho: Ancho de la dovela
        perfil_terreno: Perfil del terreno
        xc: Centro X del círculo
        yc: Centro Y del círculo
        radio: Radio del círculo
        
    Returns:
        Altura de la dovela en metros
        
    Raises:
        ValueError: Si no se puede calcular la altura
    """
    # Calcular elevación del terreno en el centro de la dovela
    y_terreno = interpolar_terreno(x, perfil_terreno)
    
    # Calcular elevación del círculo (parte inferior)
    y_circulo = calcular_y_circulo(x, xc, yc, radio, parte_superior=False)
    
    if y_circulo is None:
        raise ValueError(f"La dovela en X={x} está fuera del círculo de falla")
    
    # La altura es la diferencia
    altura = y_terreno - y_circulo
    
    if altura <= 0:
        raise ValueError(f"Altura inválida en X={x}: terreno={y_terreno}, círculo={y_circulo}")
    
    return altura


def calcular_peso_dovela(altura: float, ancho: float, gamma: float) -> float:
    """
    Calcula el peso de una dovela.
    
    W = γ * V = γ * altura * ancho * espesor_unitario
    (Asumiendo espesor unitario = 1 metro)
    
    Args:
        altura: Altura de la dovela en m
        ancho: Ancho de la dovela en m
        gamma: Peso específico en kN/m³
        
    Returns:
        Peso de la dovela en kN
    """
    return gamma * altura * ancho


def calcular_presion_poros(x: float, altura_dovela: float, perfil_terreno: List[Tuple[float, float]], 
                          nivel_freatico: Optional[List[Tuple[float, float]]] = None) -> float:
    """
    Calcula la presión de poros en la base de una dovela.
    
    Args:
        x: Coordenada X de la dovela
        altura_dovela: Altura de la dovela
        perfil_terreno: Perfil del terreno
        nivel_freatico: Perfil del nivel freático (opcional)
        
    Returns:
        Presión de poros u en kPa
    """
    if nivel_freatico is None:
        return 0.0  # Sin agua subterránea
    
    try:
        # Elevación del terreno y del nivel freático
        y_terreno = interpolar_terreno(x, perfil_terreno)
        y_freatico = interpolar_terreno(x, nivel_freatico)
        
        # Elevación de la base de la dovela (donde actúa la presión)
        y_base_dovela = y_terreno - altura_dovela
        
        # Altura de agua sobre la base de la dovela
        if y_freatico > y_base_dovela:
            altura_agua = y_freatico - y_base_dovela
            # Presión de poros = γw * hw
            return 9.81 * altura_agua  # γw = 9.81 kN/m³
        else:
            return 0.0  # Base de dovela por encima del nivel freático
            
    except ValueError:
        # Si hay problemas con la interpolación, asumir sin agua
        return 0.0


def crear_dovelas(circulo: CirculoFalla, perfil_terreno: List[Tuple[float, float]], 
                 estrato: Estrato, num_dovelas: int,
                 nivel_freatico: Optional[List[Tuple[float, float]]] = None) -> List[Dovela]:
    """
    Crea las dovelas que discretizan un círculo de falla.
    
    Args:
        circulo: Círculo de falla
        perfil_terreno: Perfil del terreno
        estrato: Propiedades del suelo
        num_dovelas: Número de dovelas a crear
        nivel_freatico: Nivel freático (opcional)
        
    Returns:
        Lista de dovelas creadas
        
    Raises:
        ValueError: Si no se pueden crear las dovelas
    """
    print(f"\n--- DEBUG: Iniciando crear_dovelas ---")
    print(f"DEBUG: Círculo: Centro=({circulo.xc}, {circulo.yc}), Radio={circulo.radio}")
    print(f"DEBUG: Perfil: {perfil_terreno}")
    print(f"DEBUG: Estrato: c={estrato.cohesion}, φ={estrato.phi_grados}, γ={estrato.gamma}")
    print(f"DEBUG: Num Dovelas: {num_dovelas}")
    print(f"DEBUG: Nivel Freático: {'Sí' if nivel_freatico else 'No'}")

    if num_dovelas < 3:
        print("DEBUG: Error - Se necesitan al menos 3 dovelas")
        raise ValueError("Se necesitan al menos 3 dovelas")
    
    # Determinar el rango X del círculo que intersecta el terreno
    x_min_circulo_abs = circulo.xc - circulo.radio
    x_max_circulo_abs = circulo.xc + circulo.radio
    print(f"DEBUG: Rango X absoluto del círculo: [{x_min_circulo_abs:.2f}, {x_max_circulo_abs:.2f}]")
    
    # Ajustar al rango del perfil del terreno
    perfil_x_min = min(punto[0] for punto in perfil_terreno)
    perfil_x_max = max(punto[0] for punto in perfil_terreno)
    print(f"DEBUG: Rango X del perfil: [{perfil_x_min:.2f}, {perfil_x_max:.2f}]")
    
    x_min_efectivo = max(x_min_circulo_abs, perfil_x_min)
    x_max_efectivo = min(x_max_circulo_abs, perfil_x_max)
    print(f"DEBUG: Rango X efectivo para dovelas: [{x_min_efectivo:.2f}, {x_max_efectivo:.2f}]")
    
    if x_min_efectivo >= x_max_efectivo:
        print("DEBUG: Error - El círculo no intersecta el perfil del terreno en el rango efectivo")
        raise ValueError("El círculo no intersecta el perfil del terreno")
    
    # Crear dovelas uniformemente espaciadas
    ancho_dovela = (x_max_efectivo - x_min_efectivo) / num_dovelas
    print(f"DEBUG: Ancho de cada dovela: {ancho_dovela:.2f}")
    dovelas = []
    
    for i in range(num_dovelas):
        # Coordenada X del centro de la dovela
        x_centro = x_min_efectivo + (i + 0.5) * ancho_dovela
        print(f"\nDEBUG: Intentando crear dovela {i} en X_centro = {x_centro:.2f}")
        
        try:
            # Calcular propiedades geométricas
            print(f"DEBUG:   Llamando calcular_altura_dovela(x_centro={x_centro:.2f}, ancho_dovela={ancho_dovela:.2f}, ...)")
            altura = calcular_altura_dovela(x_centro, ancho_dovela, perfil_terreno, 
                                          circulo.xc, circulo.yc, circulo.radio)
            print(f"DEBUG:     Altura calculada: {altura:.2f}")
            
            print(f"DEBUG:   Llamando calcular_angulo_alpha(x_centro={x_centro:.2f}, ...)")
            angulo_alpha = calcular_angulo_alpha(x_centro, circulo.xc, circulo.yc, circulo.radio)
            print(f"DEBUG:     Ángulo α calculado: {angulo_alpha:.2f}°")
            
            x_izq_dovela = x_centro - ancho_dovela/2
            x_der_dovela = x_centro + ancho_dovela/2
            print(f"DEBUG:   Llamando calcular_longitud_arco(x_izq={x_izq_dovela:.2f}, x_der={x_der_dovela:.2f}, ...)")
            longitud_arco = calcular_longitud_arco(
                x_izq_dovela, x_der_dovela,
                circulo.xc, circulo.yc, circulo.radio
            )
            print(f"DEBUG:     Longitud de arco calculada: {longitud_arco:.2f}")
            
            # Calcular peso
            print(f"DEBUG:   Llamando calcular_peso_dovela(altura={altura:.2f}, ancho_dovela={ancho_dovela:.2f}, gamma={estrato.gamma})")
            peso = calcular_peso_dovela(altura, ancho_dovela, estrato.gamma)
            print(f"DEBUG:     Peso calculado: {peso:.2f}")
            
            # Calcular presión de poros
            print(f"DEBUG:   Llamando calcular_presion_poros(x_centro={x_centro:.2f}, altura={altura:.2f}, ...)")
            presion_poros = calcular_presion_poros(x_centro, altura, perfil_terreno, nivel_freatico)
            print(f"DEBUG:     Presión de poros calculada: {presion_poros:.2f}")

            # Calcular y_base y y_superficie para la dovela
            y_superficie = interpolar_terreno(x_centro, perfil_terreno)
            y_base = calcular_y_circulo(x_centro, circulo.xc, circulo.yc, circulo.radio, parte_superior=False)
            
            # Crear dovela
            dovela = Dovela(
                x_centro=x_centro,
                ancho=ancho_dovela,
                altura=altura,
                angulo_alpha=angulo_alpha,
                cohesion=estrato.cohesion,
                phi_grados=estrato.phi_grados,
                gamma=estrato.gamma,
                peso=peso,
                presion_poros=presion_poros,
                longitud_arco=longitud_arco,
                y_base=y_base,
                y_superficie=y_superficie
            )
            print(f"DEBUG:   Dovela {i} CREADA con éxito.")
            dovelas.append(dovela)
            
        except Exception as e:
            print(f"DEBUG:   ERROR al crear dovela {i} en X={x_centro:.2f}: {e}. Saltando dovela.")
            continue
    
    if len(dovelas) == 0:
        print("DEBUG: Error - No se pudo crear ninguna dovela válida.")
        raise ValueError("No se pudo crear ninguna dovela válida.")
        
    print(f"--- DEBUG: crear_dovelas finalizado. {len(dovelas)} dovelas creadas. ---")
    return dovelas


def validar_geometria_circulo(circulo: CirculoFalla, perfil_terreno: List[Tuple[float, float]]) -> bool:
    """
    Valida que un círculo de falla tenga geometría válida respecto al terreno.
    
    Args:
        circulo: Círculo de falla a validar
        perfil_terreno: Perfil del terreno
        
    Returns:
        True si la geometría es válida
    """
    try:
        # Verificar que el círculo intersecte el terreno
        x_min = circulo.xc - circulo.radio
        x_max = circulo.xc + circulo.radio
        
        perfil_x_min = min(punto[0] for punto in perfil_terreno)
        perfil_x_max = max(punto[0] for punto in perfil_terreno)
        
        # Debe haber intersección
        if x_max <= perfil_x_min or x_min >= perfil_x_max:
            return False
        
        # Verificar que el círculo tenga una parte por debajo del terreno
        # Esto se hace comprobando que el punto más bajo del círculo es menor que el punto más alto del terreno
        # y que el punto más alto del círculo es mayor que el punto más bajo del terreno.
        # Además, el centro Y del círculo debe ser mayor que el Y más bajo del perfil para que sea una superficie de falla.
        
        y_min_perfil = min(p[1] for p in perfil_terreno)
        y_max_perfil = max(p[1] for p in perfil_terreno)

        # El punto más bajo del círculo debe estar por debajo de alguna parte del terreno
        if (circulo.yc - circulo.radio) >= y_max_perfil:
            return False

        # El centro del círculo debe estar por encima del punto más bajo del terreno
        if circulo.yc <= y_min_perfil:
            return False

        # El círculo debe tener un radio positivo y razonable
        if circulo.radio <= 0:
            return False
        
        return True
        
    except Exception:
        return False


# Funciones auxiliares para casos comunes

def crear_perfil_simple(x_inicio: float, y_inicio: float, x_fin: float, y_fin: float, 
                       num_puntos: int = 10) -> List[Tuple[float, float]]:
    """
    Crea un perfil de terreno simple (línea recta).
    
    Args:
        x_inicio: Coordenada X inicial
        y_inicio: Coordenada Y inicial
        x_fin: Coordenada X final
        y_fin: Coordenada Y final
        num_puntos: Número de puntos del perfil
        
    Returns:
        Lista de puntos del perfil
    """
    puntos = []
    for i in range(num_puntos):
        factor = i / (num_puntos - 1)
        x = x_inicio + factor * (x_fin - x_inicio)
        y = y_inicio + factor * (y_fin - y_inicio)
        puntos.append((x, y))
    
    return puntos


def crear_nivel_freatico_horizontal(x_inicio: float, x_fin: float, elevacion: float, 
                                   num_puntos: int = 10) -> List[Tuple[float, float]]:
    """
    Crea un nivel freático horizontal.
    
    Args:
        x_inicio: Coordenada X inicial
        x_fin: Coordenada X final
        elevacion: Elevación constante del nivel freático
        num_puntos: Número de puntos
        
    Returns:
        Lista de puntos del nivel freático
    """
    puntos = []
    for i in range(num_puntos):
        factor = i / (num_puntos - 1)
        x = x_inicio + factor * (x_fin - x_inicio)
        puntos.append((x, elevacion))
    
    return puntos


def crear_perfil_terreno(altura: float, angulo_grados: float, 
                         longitud_base: float = None, num_puntos: int = 50) -> List[Tuple[float, float]]:
    """
    Crea un perfil de terreno simple para un talud.
    
    Args:
        altura: Altura del talud en metros
        angulo_grados: Ángulo del talud en grados
        longitud_base: Longitud de la base horizontal (si None, se calcula automáticamente)
        num_puntos: Número de puntos para definir el perfil
        
    Returns:
        Lista de puntos (x, y) que definen el perfil del terreno
    """
    if longitud_base is None:
        # Calcular longitud base basada en la altura y ángulo
        angulo_rad = math.radians(angulo_grados)
        longitud_base = altura / math.tan(angulo_rad) if angulo_grados > 0 else altura * 2
    
    # Crear perfil: base horizontal + talud inclinado + corona horizontal
    perfil = []
    
    # Base horizontal (antes del talud)
    base_extension = longitud_base * 0.5
    for i in range(num_puntos // 4):
        x = -base_extension + i * (base_extension / (num_puntos // 4))
        y = 0.0
        perfil.append((x, y))
    
    # Talud inclinado
    for i in range(num_puntos // 2):
        progress = i / (num_puntos // 2)
        x = progress * longitud_base
        y = progress * altura
        perfil.append((x, y))
    
    # Corona horizontal (después del talud)
    corona_extension = longitud_base * 0.5
    for i in range(num_puntos // 4):
        x = longitud_base + i * (corona_extension / (num_puntos // 4))
        y = altura
        perfil.append((x, y))
    
    return perfil


def crear_nivel_freatico(altura_nf: float, perfil_terreno: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Crea un nivel freático horizontal a una altura específica.
    
    Args:
        altura_nf: Altura del nivel freático
        perfil_terreno: Perfil del terreno para determinar el rango X
        
    Returns:
        Lista de puntos que definen el nivel freático
    """
    if not perfil_terreno:
        return []
    
    x_min = min(punto[0] for punto in perfil_terreno)
    x_max = max(punto[0] for punto in perfil_terreno)
    
    # Crear nivel freático horizontal
    nivel_freatico = []
    num_puntos = 20
    for i in range(num_puntos):
        x = x_min + i * (x_max - x_min) / (num_puntos - 1)
        y = altura_nf
        nivel_freatico.append((x, y))
    
    return nivel_freatico


def validar_geometria_basica(altura: float, angulo_grados: float, 
                            centro_x: float, centro_y: float, radio: float) -> bool:
    """
    Valida que la geometría básica sea coherente.
    
    Args:
        altura: Altura del talud
        angulo_grados: Ángulo del talud
        centro_x: Centro X del círculo
        centro_y: Centro Y del círculo
        radio: Radio del círculo
        
    Returns:
        True si la geometría es válida
    """
    # Validaciones básicas
    if altura <= 0 or altura > 100:
        return False
    
    if angulo_grados <= 0 or angulo_grados >= 90:
        return False
    
    if radio <= 0 or radio > altura * 5:
        return False
    
    if centro_y < altura * 0.5 or centro_y > altura * 3:
        return False
    
    # El círculo debe intersectar razonablemente con el talud
    angulo_rad = math.radians(angulo_grados)
    longitud_base = altura / math.tan(angulo_rad)
    
    # Centro X debe estar en un rango razonable
    if centro_x < -longitud_base or centro_x > longitud_base * 2:
        return False
    
    return True
