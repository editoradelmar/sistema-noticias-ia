<!-- Copia local: la fuente canónica está en ./docs/ -->
# QUICKSTART — Guía rápida (5 minutos)

Este archivo es una copia localizada para conveniencia. Mantén la versión canónica en `./docs/`.

## Prerrequisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- Git

## 1) Clonar y configurar

```bash
git clone <repository-url>
cd sistema-noticias-ia

# Backend
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
python -m alembic upgrade head
python create_admin.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (nueva terminal)
cd ../frontend
npm install
npm run dev
```

## Verificar

- Backend: http://localhost:8000/docs
- Frontend: http://localhost:5173

--
Última actualización: 2025-10-30
