# Script para poblar la tabla prompt_item con datos de ejemplo
# Ejecutar con: python backend/scripts/populate_prompt_items.py

from sqlalchemy.orm import sessionmaker
from core.database import engine
from models.orm_models import PromptItem

Session = sessionmaker(bind=engine)
session = Session()

# Datos de ejemplo para cada prompt_id existente
items = [
    {
        "prompt_id": 1,
        "nombre_archivo": "Prompt Seccion Cartagena.txt",
        "contenido": "Contenido ejemplo para Cartagena...",
        "orden": 1
    },
    {
        "prompt_id": 1,
        "nombre_archivo": "Prompt Seccion Farandula.txt",
        "contenido": "Contenido ejemplo para Farandula...",
        "orden": 2
    },
    {
        "prompt_id": 2,
        "nombre_archivo": "Prompt Seccion Politica.txt",
        "contenido": "Contenido ejemplo para Politica...",
        "orden": 1
    },
    {
        "prompt_id": 3,
        "nombre_archivo": "Prompt Seccion Salud.txt",
        "contenido": "Contenido ejemplo para Salud...",
        "orden": 1
    }
]

for item in items:
    db_item = PromptItem(**item)
    session.add(db_item)

session.commit()
session.close()

print("Datos de ejemplo insertados en prompt_item.")
