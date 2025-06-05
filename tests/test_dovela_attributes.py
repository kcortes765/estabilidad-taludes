import pytest
from core.geometry import crear_dovelas, crear_perfil_simple
from data.models import CirculoFalla, Estrato


def test_dovelas_expose_base_and_surface_attributes():
    perfil = crear_perfil_simple(0.0, 0.0, 10.0, 0.0, num_puntos=5)
    estrato = Estrato(cohesion=10.0, phi_grados=30.0, gamma=18.0)
    circulo = CirculoFalla(xc=5.0, yc=10.0, radio=12.0)
    dovelas = crear_dovelas(circulo, perfil, estrato, num_dovelas=3)
    d = dovelas[0]
    assert hasattr(d, "y_base"), "y_base attribute missing"
    assert hasattr(d, "y_superficie"), "y_superficie attribute missing"
    assert d.y_superficie > d.y_base
