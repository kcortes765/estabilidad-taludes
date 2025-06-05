import math
from data.models import CirculoFalla, Dovela


def crear_dovela_simple():
    return Dovela(
        x_centro=0.0,
        ancho=1.0,
        altura=1.0,
        angulo_alpha=0.0,
        cohesion=5.0,
        phi_grados=20.0,
        gamma=18.0,
        peso=18.0,
        presion_poros=0.0,
        longitud_arco=1.0,
    )


def test_agregar_dovela():
    c = CirculoFalla(xc=0.0, yc=5.0, radio=10.0)
    d = crear_dovela_simple()
    c.agregar_dovela(d)
    assert c.num_dovelas == 1


def test_validar_geometria_false_without_dovelas():
    c = CirculoFalla(xc=0.0, yc=5.0, radio=10.0)
    assert not c.validar_geometria()


def test_calcular_fuerzas_normales():
    c = CirculoFalla(xc=0.0, yc=5.0, radio=10.0)
    d = crear_dovela_simple()
    c.agregar_dovela(d)
    c.calcular_fuerzas_normales_efectivas()
    assert d.fuerza_normal_efectiva != 0


def test_traccion_detection():
    c = CirculoFalla(xc=0.0, yc=5.0, radio=10.0)
    d = crear_dovela_simple()
    d.fuerza_normal_efectiva = -1.0
    d.tiene_traccion = True
    c.agregar_dovela(d)
    assert c.tiene_dovelas_en_traccion()
    assert c.obtener_dovelas_en_traccion() == [0]


def test_resumen_includes_data():
    c = CirculoFalla(xc=0.0, yc=5.0, radio=10.0)
    d = crear_dovela_simple()
    c.agregar_dovela(d)
    summary = c.resumen()
    assert "Círculo de Falla" in summary
    assert "Radio" in summary
