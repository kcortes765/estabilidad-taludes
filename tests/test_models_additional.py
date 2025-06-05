import math
import pytest
from data.models import Estrato, Dovela, CirculoFalla


@pytest.mark.parametrize("cohesion", [-1.0, -0.01])
def test_estrato_invalid_cohesion(cohesion):
    with pytest.raises(ValueError):
        Estrato(cohesion=cohesion, phi_grados=10.0, gamma=18.0)


@pytest.mark.parametrize("phi", [-5.0, 50.0])
def test_estrato_invalid_phi(phi):
    with pytest.raises(ValueError):
        Estrato(cohesion=10.0, phi_grados=phi, gamma=18.0)


@pytest.mark.parametrize("gamma", [0.0, -2.0])
def test_estrato_invalid_gamma(gamma):
    with pytest.raises(ValueError):
        Estrato(cohesion=10.0, phi_grados=20.0, gamma=gamma)


def test_estrato_properties():
    e = Estrato(cohesion=5.0, phi_grados=30.0, gamma=18.0)
    assert math.isclose(e.phi_radianes, math.pi / 6, rel_tol=1e-6)
    assert math.isclose(e.tan_phi, math.tan(math.pi / 6), rel_tol=1e-6)


@pytest.mark.parametrize("ancho", [0.0, -1.0])
def test_dovela_invalid_ancho(ancho):
    with pytest.raises(ValueError):
        Dovela(x_centro=0.0, ancho=ancho, altura=1.0, angulo_alpha=0.0,
               cohesion=5.0, phi_grados=20.0, gamma=18.0,
               peso=1.0, presion_poros=0.0, longitud_arco=1.0)


@pytest.mark.parametrize("altura", [0.0, -1.0])
def test_dovela_invalid_altura(altura):
    with pytest.raises(ValueError):
        Dovela(x_centro=0.0, ancho=1.0, altura=altura, angulo_alpha=0.0,
               cohesion=5.0, phi_grados=20.0, gamma=18.0,
               peso=1.0, presion_poros=0.0, longitud_arco=1.0)


@pytest.mark.parametrize("angulo", [math.radians(90), math.radians(-90)])
def test_dovela_invalid_alpha(angulo):
    with pytest.raises(ValueError):
        Dovela(x_centro=0.0, ancho=1.0, altura=1.0, angulo_alpha=angulo,
               cohesion=5.0, phi_grados=20.0, gamma=18.0,
               peso=1.0, presion_poros=0.0, longitud_arco=1.0)


def test_dovela_forces_and_resistance():
    d = Dovela(x_centro=0.0, ancho=1.0, altura=2.0,
               angulo_alpha=math.radians(30), cohesion=10.0,
               phi_grados=20.0, gamma=18.0, peso=36.0,
               presion_poros=0.0, longitud_arco=1.0)
    n = d.calcular_fuerza_normal_efectiva()
    assert n > 0
    resistencia = d.calcular_resistencia_fellenius()
    actuante = d.calcular_fuerza_actuante_fellenius()
    assert resistencia > 0
    assert actuante > 0


def test_circulo_init_validation():
    with pytest.raises(ValueError):
        CirculoFalla(xc=0.0, yc=0.0, radio=-1.0)
