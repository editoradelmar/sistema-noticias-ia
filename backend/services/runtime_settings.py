"""
Runtime settings store (in-memory) para valores que pueden ajustarse en tiempo de ejecución
Este módulo no persiste los cambios en disco; sirve para overrides temporales desde el admin.
"""
from threading import Lock

# Valores por defecto (None indica usar el valor de config.settings)
_store = {
    "MAX_PROMPT_CHARS": None
}

_lock = Lock()

def get_max_prompt_chars():
    with _lock:
        return _store.get("MAX_PROMPT_CHARS")

def set_max_prompt_chars(value: int):
    with _lock:
        _store["MAX_PROMPT_CHARS"] = int(value) if value is not None else None

def reset_all():
    with _lock:
        for k in _store.keys():
            _store[k] = None
