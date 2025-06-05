from evals_geotecnicos import ejecutar_evals_completos


def test_ejecutar_evals_completos():
    # El resultado puede ser True o False según la configuración del sistema,
    # pero la función no debe lanzar excepciones.
    result = ejecutar_evals_completos()
    assert isinstance(result, bool)
