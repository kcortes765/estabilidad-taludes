import math
from core.geometry import (
    calcular_longitud_arco,
    validar_geometria_basica,
    crear_perfil_simple,
)
from core.circle_constraints import CalculadorLimites, aplicar_limites_inteligentes


def test_longitud_arco_half_circle():
    # Semicircle from x=-r to x=r should have length pi*r
    r = 5.0
    length = calcular_longitud_arco(-r, r, 0.0, 0.0, r)
    assert math.isclose(length, math.pi * r, rel_tol=1e-6)


def test_validar_geometria_basica_variants():
    assert validar_geometria_basica(10.0, 30.0, 5.0, 15.0, 8.0)
    assert not validar_geometria_basica(10.0, 30.0, 50.0, 15.0, 8.0)


def test_generar_circulos_dentro_limites():
    perfil = crear_perfil_simple(0.0, 0.0, 10.0, 5.0, num_puntos=5)
    limites = aplicar_limites_inteligentes(perfil, "talud_empinado")
    calc = CalculadorLimites()
    circulos = calc.generar_circulos_dentro_limites(limites, cantidad=10)
    assert len(circulos) == 10
    for c in circulos:
        assert limites.centro_x_min <= c.xc <= limites.centro_x_max
        assert limites.centro_y_min <= c.yc <= limites.centro_y_max
        assert limites.radio_min <= c.radio <= limites.radio_max
