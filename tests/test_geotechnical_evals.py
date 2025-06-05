import pytest
from evals_geotecnicos import ejecutar_evals_completos


@pytest.mark.skip("Geotechnical evaluations not fully implemented")
def test_ejecutar_evals_completos():
    assert ejecutar_evals_completos()
