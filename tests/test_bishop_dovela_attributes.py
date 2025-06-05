from core.bishop import bishop_talud_homogeneo


def test_bishop_result_contains_dovela_heights():
    res = bishop_talud_homogeneo(
        altura=10.0,
        angulo_talud=30.0,
        cohesion=20.0,
        phi_grados=25.0,
        gamma=18.0,
        num_dovelas=5,
    )
    dovela = res.dovelas[0]
    assert hasattr(dovela, "y_base") and hasattr(dovela, "y_superficie")
