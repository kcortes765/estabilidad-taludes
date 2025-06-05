import math
from core.bishop import bishop_con_nivel_freatico
from core.fellenius import fellenius_con_nivel_freatico


def test_bishop_with_water():
    res = bishop_con_nivel_freatico(
        altura=10.0,
        angulo_talud=30.0,
        cohesion=15.0,
        phi_grados=25.0,
        gamma=18.0,
        altura_nivel_freatico=5.0,
        num_dovelas=6,
    )
    assert res.convergio
    assert res.es_valido


def test_fellenius_with_water():
    res = fellenius_con_nivel_freatico(
        altura=10.0,
        angulo_talud=30.0,
        cohesion=15.0,
        phi_grados=25.0,
        gamma=18.0,
        gamma_sat=20.0,
        profundidad_freatico=5.0,
        num_dovelas=6,
    )
    assert res.es_valido
    assert 0.5 < res.factor_seguridad < 10.0
