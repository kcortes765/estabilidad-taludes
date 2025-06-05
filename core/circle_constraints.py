"""
Sistema de Restricciones y Límites Inteligentes para Círculos de Falla

Este módulo implementa límites automáticos e inteligentes para:
- Posicionamiento del centro del círculo
- Rango de radios válidos según geometría del talud
- Restricciones geométricas para evitar fallos
- Validación previa antes de cálculos
- Corrección automática de parámetros inválidos

Objetivo: Garantizar que NUNCA fallen los cálculos por configuraciones imposibles
"""

import math
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import logging

from data.models import CirculoFalla, Estrato


class TipoRestriccion(Enum):
    """Tipos de restricciones geométricas"""

    CENTRO_X_MIN = "centro_x_min"
    CENTRO_X_MAX = "centro_x_max"
    CENTRO_Y_MIN = "centro_y_min"
    CENTRO_Y_MAX = "centro_y_max"
    RADIO_MIN = "radio_min"
    RADIO_MAX = "radio_max"
    DISTANCIA_TALUD_MIN = "distancia_talud_min"
    COBERTURA_MIN = "cobertura_min"


@dataclass
class LimitesGeometricos:
    """Límites geométricos calculados automáticamente"""

    # Límites del centro
    centro_x_min: float
    centro_x_max: float
    centro_y_min: float
    centro_y_max: float

    # Límites del radio
    radio_min: float
    radio_max: float

    # Restricciones adicionales
    distancia_minima_talud: float
    cobertura_minima_requerida: float

    # Metadatos
    ancho_talud: float
    altura_talud: float
    longitud_diagonal: float
    pendiente_talud: float


@dataclass
class ResultadoValidacion:
    """Resultado de validación con límites"""

    es_valido: bool
    violaciones: List[str]
    circulo_corregido: Optional[CirculoFalla]
    limites_aplicados: LimitesGeometricos
    sugerencias: List[str]


class CalculadorLimites:
    """Calculador inteligente de límites geométricos"""

    def __init__(self):
        # Factores de seguridad para límites
        self.factor_margen_lateral = 0.6  # 60% del ancho como margen lateral
        self.factor_altura_minima = 1.2  # 120% de altura mínima sobre terreno
        self.factor_altura_maxima = 3.0  # 300% de altura máxima sobre terreno
        self.factor_radio_min = 0.15  # 15% de diagonal como radio mínimo
        self.factor_radio_max = 2.5  # 250% de diagonal como radio máximo
        self.cobertura_minima = 0.3  # 30% cobertura mínima del talud

    def calcular_limites_desde_perfil(
        self,
        perfil_terreno: List[Tuple[float, float]],
        configuracion: Optional[Dict[str, float]] = None,
    ) -> LimitesGeometricos:
        """
        Calcula límites geométricos INTELIGENTES basados en la geometría REAL del talud
        """
        if not perfil_terreno:
            raise ValueError("Perfil de terreno no puede estar vacío")

        # ANÁLISIS GEOMÉTRICO DEL TALUD REAL
        x_coords = [p[0] for p in perfil_terreno]
        y_coords = [p[1] for p in perfil_terreno]

        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        # Calcular dimensiones del talud
        altura_talud = y_max - y_min
        longitud_base = x_max - x_min

        # Estimar ángulo del talud
        if altura_talud > 0 and longitud_base > 0:
            angulo_talud_rad = math.atan(altura_talud / longitud_base)
            angulo_talud_deg = math.degrees(angulo_talud_rad)
        else:
            angulo_talud_deg = 45.0

        # Obtener configuración
        if configuracion is None:
            # Detectar tipo de talud automáticamente basado en el ángulo
            tipo_talud_detectado = detectar_tipo_talud_desde_angulo(angulo_talud_deg)
            print(
                f" Tipo de talud detectado: {tipo_talud_detectado} (ángulo: {angulo_talud_deg:.1f}°)"
            )

            configuraciones_predefinidas = crear_limites_predefinidos()
            configuracion = configuraciones_predefinidas.get(
                tipo_talud_detectado, configuraciones_predefinidas["talud_empinado"]
            )

        print(f"📐 GEOMETRÍA DEL TALUD:")
        print(f"   Altura: {altura_talud:.2f}m")
        print(f"   Base: {longitud_base:.2f}m")
        print(f"   Ángulo: {angulo_talud_deg:.1f}°")
        print(f"   Rango X: [{x_min:.2f}, {x_max:.2f}]")
        print(f"   Rango Y: [{y_min:.2f}, {y_max:.2f}]")

        # LÍMITES INTELIGENTES BASADOS EN GEOMETRÍA REAL Y CONFIGURACIÓN

        # Centro X: usar factor de margen lateral de la configuración
        margen_x = altura_talud * configuracion.get("factor_margen_lateral", 0.6)
        centro_x_min = x_min - margen_x
        centro_x_max = x_max + margen_x

        # Centro Y: usar factor de altura máxima de la configuración
        altura_minima_centro = y_max + altura_talud * 0.3  # Mínimo 30% arriba
        altura_maxima_centro = y_max + altura_talud * configuracion.get(
            "factor_altura_maxima", 1.5
        )
        centro_y_min = altura_minima_centro
        centro_y_max = altura_maxima_centro

        # Radio: usar factor de radio máximo de la configuración
        radio_min = altura_talud * 0.8  # Mínimo 80% de la altura
        radio_max = altura_talud * configuracion.get("factor_radio_max", 1.5)

        print(f"🎯 LÍMITES CALCULADOS:")
        print(
            f"   Centro X: [{centro_x_min:.2f}, {centro_x_max:.2f}] (margen: ±{margen_x:.2f})"
        )
        print(
            f"   Centro Y: [{centro_y_min:.2f}, {centro_y_max:.2f}] (altura talud + {altura_talud*0.3:.2f} a +{altura_talud*configuracion.get('factor_altura_maxima', 1.5):.2f})"
        )
        print(
            f"   Radio: [{radio_min:.2f}, {radio_max:.2f}] ({altura_talud*0.8:.2f}H a {altura_talud*configuracion.get('factor_radio_max', 1.5):.2f}H)"
        )

        return LimitesGeometricos(
            centro_x_min=centro_x_min,
            centro_x_max=centro_x_max,
            centro_y_min=centro_y_min,
            centro_y_max=centro_y_max,
            radio_min=radio_min,
            radio_max=radio_max,
            distancia_minima_talud=0.0,
            cobertura_minima_requerida=0.0,
            ancho_talud=longitud_base,
            altura_talud=altura_talud,
            longitud_diagonal=math.sqrt(longitud_base**2 + altura_talud**2),
            pendiente_talud=angulo_talud_deg,
        )

    def validar_y_corregir_circulo(
        self,
        circulo: CirculoFalla,
        limites: LimitesGeometricos,
        corregir_automaticamente: bool = True,
    ) -> ResultadoValidacion:
        """
        Valida un círculo contra los límites y opcionalmente lo corrige
        """
        violaciones = []
        sugerencias = []

        # Validar límites del centro
        if circulo.xc < limites.centro_x_min:
            violaciones.append(
                f"Centro X muy a la izquierda: {circulo.xc:.2f} < {limites.centro_x_min:.2f}"
            )
            if corregir_automaticamente:
                xc_corregido = limites.centro_x_min

        if circulo.xc > limites.centro_x_max:
            violaciones.append(
                f"Centro X muy a la derecha: {circulo.xc:.2f} > {limites.centro_x_max:.2f}"
            )
            if corregir_automaticamente:
                xc_corregido = limites.centro_x_max

        if circulo.yc < limites.centro_y_min:
            violaciones.append(
                f"Centro Y muy bajo: {circulo.yc:.2f} < {limites.centro_y_min:.2f}"
            )
            if corregir_automaticamente:
                yc_corregido = limites.centro_y_min

        if circulo.yc > limites.centro_y_max:
            violaciones.append(
                f"Centro Y muy alto: {circulo.yc:.2f} > {limites.centro_y_max:.2f}"
            )
            if corregir_automaticamente:
                yc_corregido = limites.centro_y_max

        # Validar límites del radio
        if circulo.radio < limites.radio_min:
            violaciones.append(
                f"Radio muy pequeño: {circulo.radio:.2f} < {limites.radio_min:.2f}"
            )
            if corregir_automaticamente:
                radio_corregido = limites.radio_min

        if circulo.radio > limites.radio_max:
            violaciones.append(
                f"Radio muy grande: {circulo.radio:.2f} > {limites.radio_max:.2f}"
            )
            if corregir_automaticamente:
                radio_corregido = limites.radio_max

        # Generar sugerencias
        if violaciones:
            sugerencias.append(
                "Ajustar parámetros del círculo dentro de los límites permitidos"
            )
            if circulo.radio < limites.radio_min:
                sugerencias.append(f"Aumentar radio a al menos {limites.radio_min:.2f}")
            if circulo.yc < limites.centro_y_min:
                sugerencias.append(
                    f"Subir centro a al menos Y={limites.centro_y_min:.2f}"
                )

        # Corrección automática si se solicita
        circulo_corregido = None
        if corregir_automaticamente and violaciones:
            circulo_corregido = self._corregir_circulo(circulo, limites)
            sugerencias.append("Círculo corregido automáticamente")

        es_valido = len(violaciones) == 0

        logging.debug(
            f"Resultado validación: válido={es_valido}, violaciones={violaciones}, circulo_corregido={circulo_corregido}"
        )

        return ResultadoValidacion(
            es_valido=es_valido,
            violaciones=violaciones,
            circulo_corregido=circulo_corregido,
            limites_aplicados=limites,
            sugerencias=sugerencias,
        )

    def _corregir_circulo(
        self, circulo: CirculoFalla, limites: LimitesGeometricos
    ) -> CirculoFalla:
        """Corrige automáticamente un círculo para que cumpla los límites"""
        # Corregir centro X
        nuevo_cx = max(limites.centro_x_min, min(circulo.xc, limites.centro_x_max))

        # Corregir centro Y
        nuevo_cy = max(limites.centro_y_min, min(circulo.yc, limites.centro_y_max))

        # Corregir radio
        nuevo_r = max(limites.radio_min, min(circulo.radio, limites.radio_max))

        logging.debug(
            f"Círculo corregido de X={circulo.xc:.2f},Y={circulo.yc:.2f},R={circulo.radio:.2f} a X={nuevo_cx:.2f},Y={nuevo_cy:.2f},R={nuevo_r:.2f}"
        )

        return CirculoFalla(xc=nuevo_cx, yc=nuevo_cy, radio=nuevo_r)

    def generar_circulos_dentro_limites(
        self,
        limites: LimitesGeometricos,
        cantidad: int = 10,
        distribucion: str = "uniforme",
    ) -> List[CirculoFalla]:
        """
        Genera círculos automáticamente dentro de los límites establecidos
        """
        import random

        circulos = []

        for _ in range(cantidad):
            if distribucion == "uniforme":
                # Distribución uniforme
                cx = random.uniform(limites.centro_x_min, limites.centro_x_max)
                cy = random.uniform(limites.centro_y_min, limites.centro_y_max)
                r = random.uniform(limites.radio_min, limites.radio_max)

            elif distribucion == "gaussiana":
                # Distribución gaussiana centrada
                cx_medio = (limites.centro_x_min + limites.centro_x_max) / 2
                cy_medio = (limites.centro_y_min + limites.centro_y_max) / 2
                r_medio = (limites.radio_min + limites.radio_max) / 2

                # Desviación estándar como 1/4 del rango
                std_cx = (limites.centro_x_max - limites.centro_x_min) / 4
                std_cy = (limites.centro_y_max - limites.centro_y_min) / 4
                std_r = (limites.radio_max - limites.radio_min) / 4

                cx = random.gauss(cx_medio, std_cx)
                cy = random.gauss(cy_medio, std_cy)
                r = random.gauss(r_medio, std_r)

                # Asegurar que estén dentro de límites
                cx = max(limites.centro_x_min, min(cx, limites.centro_x_max))
                cy = max(limites.centro_y_min, min(cy, limites.centro_y_max))
                r = max(limites.radio_min, min(r, limites.radio_max))

            else:  # "critico" - enfocado en círculos más grandes y cercanos
                # Favorecer radios grandes y centros más cercanos al talud
                cx = random.uniform(
                    limites.centro_x_min * 0.7, limites.centro_x_max * 0.7
                )
                cy = random.uniform(
                    limites.centro_y_min,
                    limites.centro_y_min
                    + (limites.centro_y_max - limites.centro_y_min) * 0.4,
                )
                r = random.uniform(limites.radio_min * 1.2, limites.radio_max * 0.9)

            circulos.append(CirculoFalla(xc=cx, yc=cy, radio=r))

        return circulos


def detectar_tipo_talud_desde_angulo(angulo_grados: float) -> str:
    """
    Detecta automáticamente el tipo de talud basado en el ángulo calculado
    """
    if angulo_grados <= 15:
        return "talud_suave"
    elif angulo_grados <= 30:
        return "talud_empinado"
    elif angulo_grados <= 50:
        return "talud_critico"
    else:
        return "talud_conservador"  # Para ángulos muy altos, ser conservador


def crear_limites_predefinidos() -> Dict[str, Dict[str, float]]:
    """Crear límites predefinidos para casos típicos"""

    return {
        "talud_suave": {
            "factor_margen_lateral": 0.8,  # Más margen lateral para taludes suaves
            "factor_altura_maxima": 2.0,  # Centro más alto permitido
            "factor_radio_max": 2.0,  # Radios más grandes permitidos
            "cobertura_minima": 0.25,  # Menos cobertura requerida
        },
        "talud_empinado": {
            "factor_margen_lateral": 0.5,
            "factor_altura_maxima": 2.5,
            "factor_radio_max": 1.8,
            "cobertura_minima": 0.4,
        },
        "talud_critico": {
            "factor_margen_lateral": 0.3,
            "factor_altura_maxima": 2.0,
            "factor_radio_max": 1.5,
            "cobertura_minima": 0.5,
        },
        "talud_conservador": {
            "factor_margen_lateral": 0.2,
            "factor_altura_maxima": 1.5,
            "factor_radio_max": 1.2,
            "cobertura_minima": 0.6,
        },
    }


def aplicar_limites_inteligentes(
    perfil_terreno: List[Tuple[float, float]],
    tipo_talud: str = "talud_empinado",
    factor_seguridad_objetivo: float = 1.5,
) -> LimitesGeometricos:
    """
    Función de conveniencia para aplicar límites inteligentes
    """
    calculador = CalculadorLimites()

    # Aplicar configuración predefinida si existe
    configuraciones = crear_limites_predefinidos()
    if tipo_talud in configuraciones:
        config = configuraciones[tipo_talud]
        for attr, valor in config.items():
            if hasattr(calculador, attr):
                setattr(calculador, attr, valor)

    return calculador.calcular_limites_desde_perfil(perfil_terreno)


def validar_circulo_geometricamente(
    circulo: CirculoFalla,
    limites: LimitesGeometricos,
    corregir_automaticamente: bool = True,
) -> ResultadoValidacion:
    """Valida un círculo usando límites pre-calculados."""

    calculador = CalculadorLimites()
    return calculador.validar_y_corregir_circulo(
        circulo, limites, corregir_automaticamente
    )


# Función de conveniencia para validación rápida
def validar_circulo_con_limites(
    circulo: CirculoFalla,
    perfil_terreno: List[Tuple[float, float]],
    tipo_talud: str = "talud_empinado",
) -> ResultadoValidacion:
    """Validación rápida de círculo con límites automáticos"""

    print(
        f" Validando círculo X={circulo.xc:.2f}, Y={circulo.yc:.2f}, R={circulo.radio:.2f} para {tipo_talud}"
    )

    limites = aplicar_limites_inteligentes(perfil_terreno, tipo_talud)

    print(f" Límites calculados:")
    print(f"   Centro X: [{limites.centro_x_min:.2f}, {limites.centro_x_max:.2f}]")
    print(f"   Centro Y: [{limites.centro_y_min:.2f}, {limites.centro_y_max:.2f}]")
    print(f"   Radio: [{limites.radio_min:.2f}, {limites.radio_max:.2f}]")

    calculador = CalculadorLimites()
    resultado = calculador.validar_y_corregir_circulo(
        circulo, limites, corregir_automaticamente=True
    )

    print(f" Resultado validación: válido={resultado.es_valido}")
    if resultado.circulo_corregido:
        print(
            f" Círculo CORREGIDO de X={circulo.xc:.2f},Y={circulo.yc:.2f},R={circulo.radio:.2f}"
        )
        print(
            f"                     a X={resultado.circulo_corregido.xc:.2f},Y={resultado.circulo_corregido.yc:.2f},R={resultado.circulo_corregido.radio:.2f}"
        )
    if resultado.violaciones:
        print(f"  Violaciones: {resultado.violaciones}")

    return resultado


def main():
    logging.basicConfig(level=logging.DEBUG)

    # Ejemplo de uso
    perfil_terreno = [(0, 0), (10, 5), (20, 10)]
    circulo = CirculoFalla(xc=5, yc=5, radio=3)

    resultado = validar_circulo_con_limites(circulo, perfil_terreno)

    print(resultado)


if __name__ == "__main__":
    main()
