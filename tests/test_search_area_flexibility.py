import math
from core.circle_constraints import aplicar_limites_inteligentes, CalculadorLimites
from data.models import CirculoFalla


def test_limites_amplios_por_defecto():
    perfil = [(0, 0), (20, 10)]
    limites = aplicar_limites_inteligentes(perfil, "talud_empinado")
    # margen lateral al menos igual a la altura
    assert limites.centro_x_min <= -limites.altura_talud
    assert limites.centro_x_max >= 20 + limites.altura_talud
    # radio mínimo más flexible que 50% de la altura
    assert limites.radio_min < 0.5 * limites.altura_talud


def test_validacion_circulo_pequeno():
    perfil = [(0, 0), (20, 10)]
    limites = aplicar_limites_inteligentes(perfil, "talud_empinado")
    calc = CalculadorLimites()
    radio_prueba = 0.4 * limites.altura_talud
    circulo = CirculoFalla(
        xc=(limites.centro_x_min + limites.centro_x_max) / 2,
        yc=limites.centro_y_min + 0.5,
        radio=radio_prueba,
    )
    res = calc.validar_y_corregir_circulo(circulo, limites, False)
    assert res.es_valido
