from core.circle_constraints import aplicar_limites_inteligentes


def test_limites_amplios():
    perfil = [(0, 0), (10, 5), (20, 0)]
    limites = aplicar_limites_inteligentes(perfil, "talud_empinado")
    altura = limites.altura_talud
    assert limites.radio_max >= 2 * altura
    assert limites.centro_y_max > limites.centro_y_min
