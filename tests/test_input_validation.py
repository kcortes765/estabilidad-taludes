import pytest

from core.bishop import analizar_bishop
from core.fellenius import analizar_fellenius
from core.geometry import crear_perfil_simple
from data.models import CirculoFalla, Estrato
from data.validation import ValidacionError


def _make_basic_inputs():
    perfil = crear_perfil_simple(0.0, 0.0, 10.0, 5.0, num_puntos=5)
    estrato = Estrato(cohesion=10.0, phi_grados=30.0, gamma=18.0)
    circulo = CirculoFalla(xc=5.0, yc=8.0, radio=10.0)
    return circulo, perfil, estrato


def test_bishop_invalid_num_dovelas():
    circ, perfil, estrato = _make_basic_inputs()
    with pytest.raises(ValidacionError):
        analizar_bishop(circ, perfil, estrato, num_dovelas=2)


def test_bishop_invalid_factor_inicial():
    circ, perfil, estrato = _make_basic_inputs()
    with pytest.raises(ValidacionError):
        analizar_bishop(circ, perfil, estrato, factor_inicial=0)


def test_bishop_invalid_tolerancia():
    circ, perfil, estrato = _make_basic_inputs()
    with pytest.raises(ValidacionError):
        analizar_bishop(circ, perfil, estrato, tolerancia=-0.1)


def test_bishop_invalid_iteraciones():
    circ, perfil, estrato = _make_basic_inputs()
    with pytest.raises(ValidacionError):
        analizar_bishop(circ, perfil, estrato, max_iteraciones=0)


def test_fellenius_invalid_inputs():
    circ, perfil, estrato = _make_basic_inputs()
    with pytest.raises(ValidacionError):
        analizar_fellenius(circ, "no-list", estrato)

    with pytest.raises(ValidacionError):
        analizar_fellenius(circ, perfil, estrato, num_dovelas=1)


def test_bishop_valid_inputs():
    circ, perfil, estrato = _make_basic_inputs()
    res = analizar_bishop(circ, perfil, estrato, num_dovelas=5)
    assert res.convergio
