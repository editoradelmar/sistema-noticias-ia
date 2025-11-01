import pytest
from services.generador_ia import GeneradorIA


def test_merge_replace():
    g = GeneradorIA(db=None)
    estilo = {'a': 1, 'max_caracteres': 200}
    salida = {'modo_fusion': 'replace', 'b': 2, 'max_caracteres': 100}
    res = g.merge_configs(estilo, salida)
    assert 'b' in res and res['b'] == 2
    assert 'modo_fusion' not in res
    assert res.get('max_caracteres') == 100


def test_merge_shallow():
    g = GeneradorIA(db=None)
    estilo = {'a': 1, 'b': 2, 'max_caracteres': 300}
    salida = {'b': 3}
    res = g.merge_configs(estilo, salida)
    # b overwritten, a preserved, max_caracteres should NOT be inherited from estilo
    assert res.get('a') == 1
    assert res.get('b') == 3
    assert 'max_caracteres' not in res


def test_combine_deep():
    g = GeneradorIA(db=None)
    estilo = {'meta': {'tags': ['a', 'b'], 'tone': 'formal'}, 'x': 1}
    salida = {'modo_fusion': 'combine', 'meta': {'tags': ['b', 'c'], 'extras': True}, 'x': 2, 'max_caracteres': 140}
    res = g.merge_configs(estilo, salida)
    assert isinstance(res, dict)
    assert '_merged' in res and '_metadata' in res
    merged = res['_merged']
    meta = res['_metadata']
    # merged checks
    assert merged.get('x') == 2
    assert merged.get('max_caracteres') == 140
    assert 'meta' in merged and 'tags' in merged['meta']
    tags = merged['meta']['tags']
    assert set(tags) == {'a', 'b', 'c'}
    # metadata should record override for x
    assert any('/' in k or 'x' in k for k in meta.get('source_map', {}).keys())