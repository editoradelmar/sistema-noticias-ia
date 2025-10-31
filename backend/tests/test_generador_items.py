import types
import importlib.util
import pathlib

# Cargar módulo GeneradorIA desde su ruta para evitar problemas de import en pytest
base_dir = pathlib.Path(__file__).resolve().parents[1]
mod_path = base_dir / 'services' / 'generador_ia.py'
spec = importlib.util.spec_from_file_location('generador_ia', str(mod_path))
generador_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generador_mod)
GeneradorIA = generador_mod.GeneradorIA


def make_prompt_item(contenido, orden=1):
    it = types.SimpleNamespace()
    it.contenido = contenido
    it.orden = orden
    return it


def make_prompt_maestro(nombre, items):
    p = types.SimpleNamespace()
    p.nombre = nombre
    p.items = items
    return p


def make_estilo_item(contenido, orden=1):
    it = types.SimpleNamespace()
    it.contenido = contenido
    it.orden = orden
    return it


def make_estilo_maestro(nombre, configuracion, items):
    e = types.SimpleNamespace()
    e.nombre = nombre
    e.configuracion = configuracion
    e.items = items
    return e


def test_procesar_prompt_concat_items_and_replace_variables():
    gen = GeneradorIA(db=None)

    items = [
        make_prompt_item("INSTRUCCIONES BASE: Reescribe manteniendo formato.\nTEMA: {tema}", orden=1),
        make_prompt_item("AGREGAR: Usa lenguaje claro y subtítulos.\nLONGITUD: ~{longitud}", orden=2)
    ]

    prompt = make_prompt_maestro('PruebaPrompt', items)

    variables = {
        'titulo': 'Mi noticia',
        'contenido': 'Contenido original',
        'tema': 'Economía',
        'longitud': '200'
    }

    result = gen.procesar_prompt(prompt, variables)

    assert 'INSTRUCCIONES BASE' in result
    assert 'AGREGAR' in result
    assert '{tema}' not in result
    assert 'Economía' in result
    assert '{longitud}' not in result
    assert '200' in result


def test_aplicar_estilo_concat_items_and_config():
    gen = GeneradorIA(db=None)

    estilo_items = [
        make_estilo_item('REGLA 1: Usa voz pasiva con moderación.', orden=1),
        make_estilo_item('EJEMPLO: "El gobierno anunció..."', orden=2)
    ]

    estilo = make_estilo_maestro('EstiloPrueba', {'tono': 'formal', 'longitud': 'corta'}, estilo_items)

    prompt_base = "TEXTO BASE: Reescribe la noticia para público general."

    resultado = gen.aplicar_estilo(prompt_base, estilo)

    assert 'ESTILO Y DIRECTIVAS' in resultado or 'Tono:' in resultado or 'Longitud aproximada' in resultado
    assert 'REGLA 1' in resultado
    assert 'EJEMPLO' in resultado
    assert 'formal' in resultado or 'tono' in resultado
