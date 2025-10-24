"""
Routers de la API
"""
from . import noticias, ai, auth, proyectos
from . import llm_maestro, prompts, estilos, secciones, salidas
from . import generacion

__all__ = [
    "noticias", 
    "ai", 
    "auth", 
    "proyectos",
    "llm_maestro",
    "prompts",
    "estilos",
    "secciones",
    "salidas",
    "generacion"
]
