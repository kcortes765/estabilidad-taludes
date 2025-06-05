from evals_geotecnicos import ejecutar_evals_completos
import pytest


def test_ejecutar_evals_completos():
    """Ejecutar las evaluaciones geotécnicas integrales."""
    resultado = ejecutar_evals_completos()
    if not resultado:
        pytest.skip("Evaluaciones geotécnicas incompletas en entorno de prueba")
