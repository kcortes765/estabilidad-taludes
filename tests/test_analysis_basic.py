from core.bishop import bishop_talud_homogeneo
from core.fellenius import fellenius_talud_homogeneo


def test_bishop_and_fellenius():
    res_b = bishop_talud_homogeneo(
        altura=8.0,
        angulo_talud=30.0,
        cohesion=20.0,
        phi_grados=20.0,
        gamma=18.0,
        num_dovelas=8,
    )
    assert res_b.convergio
    assert res_b.es_valido
    assert 0.5 < res_b.factor_seguridad < 5.0

    res_f = fellenius_talud_homogeneo(
        altura=8.0,
        angulo_talud=30.0,
        cohesion=20.0,
        phi_grados=20.0,
        gamma=18.0,
        num_dovelas=8,
    )
    assert res_f.es_valido
    assert 0.5 < res_f.factor_seguridad < 10.0
