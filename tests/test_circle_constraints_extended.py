import pytest
from core.circle_constraints import (
    CalculadorLimites,
    aplicar_limites_inteligentes,
    detectar_tipo_talud_desde_angulo,
)
from data.models import CirculoFalla


@pytest.mark.parametrize("angulo,expected", [
    (10, "talud_suave"),
    (25, "talud_empinado"),
    (40, "talud_critico"),
    (60, "talud_conservador"),
])
def test_detectar_tipo_talud(angulo, expected):
    assert detectar_tipo_talud_desde_angulo(angulo) == expected


def test_calcular_limites_basicos():
    perfil = [(0.0, 0.0), (10.0, 5.0), (20.0, 0.0)]
    calc = CalculadorLimites()
    limites = calc.calcular_limites_desde_perfil(perfil)
    assert limites.centro_x_min < limites.centro_x_max
    assert limites.radio_min < limites.radio_max


def test_validar_y_corregir_ajusta():
    perfil = [(0.0, 0.0), (10.0, 5.0), (20.0, 0.0)]
    limites = aplicar_limites_inteligentes(perfil)
    calc = CalculadorLimites()
    c = CirculoFalla(xc=-100.0, yc=0.0, radio=1.0)
    res = calc.validar_y_corregir_circulo(c, limites, corregir_automaticamente=True)
    assert res.circulo_corregido is not None

def test_generar_circulos_cantidad():
    perfil = [(0.0, 0.0), (10.0, 5.0), (20.0, 0.0)]
    limites = aplicar_limites_inteligentes(perfil)
    calc = CalculadorLimites()
    circulos = calc.generar_circulos_dentro_limites(limites, cantidad=5)
    assert len(circulos) == 5
    for c in circulos:
        assert limites.centro_x_min <= c.xc <= limites.centro_x_max

