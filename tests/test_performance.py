import timeit
from core.geometry import calcular_y_circulo


def test_calcular_y_circulo_speed():
    duration = timeit.timeit(
        lambda: calcular_y_circulo(5.0, 0.0, 0.0, 10.0), number=1000
    )
    assert duration < 0.5
