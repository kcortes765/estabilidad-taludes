from core.circle_constraints import CalculadorLimites, aplicar_limites_inteligentes
from data.models import CirculoFalla


def test_validar_y_corregir_no_unboundlocalerror():
    perfil = [(0, 0), (10, 5), (20, 0)]
    limites = aplicar_limites_inteligentes(perfil, "talud_empinado")
    calc = CalculadorLimites()
    circulo = CirculoFalla(xc=limites.centro_x_min + 1,
                           yc=limites.centro_y_min + 1,
                           radio=limites.radio_min + 1)
    result = calc.validar_y_corregir_circulo(
        circulo, limites, corregir_automaticamente=False
    )
    assert result.es_valido
