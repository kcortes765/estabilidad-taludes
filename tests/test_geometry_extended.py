import math
import pytest
from core.geometry import (
    calcular_y_circulo,
    interpolar_terreno,
    calcular_angulo_alpha,
    calcular_longitud_arco,
    calcular_altura_dovela,
    calcular_peso_dovela,
    crear_perfil_simple,
)


@pytest.mark.parametrize("x,parte_superior,expected", [
    (0.0, True, 5.0),
    (0.0, False, -5.0),
])
def test_calcular_y_circulo_basic(x, parte_superior, expected):
    assert math.isclose(
        calcular_y_circulo(x, 0.0, 0.0, 5.0, parte_superior),
        expected,
        rel_tol=1e-6,
    )


def test_calcular_y_circulo_outside():
    assert calcular_y_circulo(10.0, 0.0, 0.0, 5.0) is None


@pytest.mark.parametrize("x", [-1.0, 11.0])
def test_interpolar_terreno_out_of_bounds(x):
    perfil = [(0.0, 0.0), (10.0, 5.0)]
    with pytest.raises(ValueError):
        interpolar_terreno(x, perfil)


def test_calcular_angulo_alpha_value():
    ang = calcular_angulo_alpha(1.0, 0.0, 0.0, 2.0)
    assert math.isclose(ang, math.asin(0.5), rel_tol=1e-6)


def test_calcular_longitud_arco_half():
    length = calcular_longitud_arco(-1.0, 1.0, 0.0, 0.0, 1.0)
    assert math.isclose(length, math.pi, rel_tol=1e-6)


def test_calcular_altura_y_peso_dovela():
    perfil = [(0.0, 0.0), (10.0, 10.0)]
    altura = calcular_altura_dovela(5.0, 1.0, perfil, 5.0, 5.0, 5.0)
    peso = calcular_peso_dovela(altura, 1.0, 18.0)
    assert altura > 0
    assert math.isclose(peso, 18.0 * altura, rel_tol=1e-6)


def test_crear_perfil_simple_points():
    perfil = crear_perfil_simple(0.0, 0.0, 10.0, 5.0, num_puntos=6)
    assert len(perfil) == 6
    assert perfil[0] == (0.0, 0.0)
