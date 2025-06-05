import math
from core.circle_constraints import CalculadorLimites, aplicar_limites_inteligentes
from data.models import CirculoFalla
from casos_literatura_adaptados import crear_casos_literatura_adaptados
from core.bishop import analizar_bishop


def test_limites_flexibles_no_rechazan_circulos_razonables():
    perfil = [(0, 0), (10, 5), (20, 0)]
    limites = aplicar_limites_inteligentes(perfil, "talud_empinado")
    calc = CalculadorLimites()

    delta_x = (limites.centro_x_max - limites.centro_x_min) * 0.05
    delta_y = (limites.centro_y_max - limites.centro_y_min) * 0.05
    delta_r = (limites.radio_max - limites.radio_min) * 0.05

    circulo = CirculoFalla(
        xc=limites.centro_x_max + delta_x,
        yc=limites.centro_y_max + delta_y,
        radio=limites.radio_max + delta_r,
    )

    result = calc.validar_y_corregir_circulo(circulo, limites, corregir_automaticamente=True)

    assert not result.es_valido
    assert result.circulo_corregido is not None

    corregido = result.circulo_corregido
    assert limites.centro_x_min <= corregido.xc <= limites.centro_x_max
    assert limites.centro_y_min <= corregido.yc <= limites.centro_y_max
    assert limites.radio_min <= corregido.radio <= limites.radio_max


def test_optimizador_encuentra_fs_caso_literatura():
    casos = crear_casos_literatura_adaptados()
    caso = casos["caso_critico_realista"]

    # Usar el círculo crítico conocido del caso
    circulo = caso["circulo"]
    resultado = analizar_bishop(circulo, caso["perfil"], caso["estrato"], num_dovelas=8)

    assert resultado.es_valido
    assert math.isfinite(resultado.factor_seguridad)
    assert 0.5 < resultado.factor_seguridad < 10.0
