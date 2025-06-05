from evals_geotecnicos import ejecutar_evals_completos


def test_ejecutar_evals_completos():
    assert isinstance(ejecutar_evals_completos(), bool)
