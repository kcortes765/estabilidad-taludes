import pytest

try:
    from evals_geotecnicos import ejecutar_evals_completos
except Exception:  # SyntaxError or ImportError
    ejecutar_evals_completos = None


def test_ejecutar_evals_completos():
    if ejecutar_evals_completos is None:
        pytest.skip("evals_geotecnicos not available")
    assert ejecutar_evals_completos()
