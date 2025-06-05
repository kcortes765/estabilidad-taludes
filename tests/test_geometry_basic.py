import math
from core.geometry import (
    calcular_y_circulo,
    interpolar_terreno,
    validar_geometria_circulo,
    crear_perfil_simple,
)
from data.models import CirculoFalla


def test_geometry_functions():
    perfil = crear_perfil_simple(0.0, 10.0, 30.0, 0.0, num_puntos=5)
    assert len(perfil) == 5
    # interpolar en mitad
    y_mid = interpolar_terreno(15.0, perfil)
    assert math.isclose(y_mid, 5.0, rel_tol=1e-6)

    y_top = calcular_y_circulo(5.0, 5.0, 5.0, 5.0, parte_superior=True)
    y_bottom = calcular_y_circulo(5.0, 5.0, 5.0, 5.0, parte_superior=False)
    assert math.isclose(y_top, 10.0, rel_tol=1e-6)
    assert math.isclose(y_bottom, 0.0, rel_tol=1e-6)

    circulo = CirculoFalla(xc=15.0, yc=8.0, radio=10.0)
    assert validar_geometria_circulo(circulo, perfil)
