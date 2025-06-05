import math
from core.circle_constraints import aplicar_limites_inteligentes, validar_circulo_geometricamente
from data.models import CirculoFalla


def test_validar_circulo_geometricamente():
    perfil = [(0, 0), (10, 5), (20, 10)]
    limites = aplicar_limites_inteligentes(perfil, "talud_empinado")
    circulo = CirculoFalla(xc=-5.0, yc=-5.0, radio=50.0)

    resultado = validar_circulo_geometricamente(circulo, limites, True)

    assert resultado.circulo_corregido is not None
    c = resultado.circulo_corregido
    assert limites.centro_x_min <= c.xc <= limites.centro_x_max
    assert limites.centro_y_min <= c.yc <= limites.centro_y_max
    assert limites.radio_min <= c.radio <= limites.radio_max
