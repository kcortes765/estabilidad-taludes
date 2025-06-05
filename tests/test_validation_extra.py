from data.validation import validar_perfil_terreno


def test_validar_perfil_terreno_ok():
    perfil = [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0)]
    res = validar_perfil_terreno(perfil)
    assert res.es_valido


def test_validar_perfil_terreno_fail():
    perfil = [(0.0, 0.0)]
    res = validar_perfil_terreno(perfil)
    assert not res.es_valido
