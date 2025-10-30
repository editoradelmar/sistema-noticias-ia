<!-- Copia local: la fuente canónica está en ./docs/ -->
# ARCHITECTURE — Resumen técnico

Este archivo es una copia resumida con la información esencial; la versión completa está en `./docs/ARCHITECTURE.md`.

## Visión general

Sistema de Noticias con IA: backend en FastAPI (Python 3.11+), frontend en React 18 + Vite, base de datos PostgreSQL, y soporte Multi-LLM (Google Gemini, Anthropic Claude, OpenAI opcional).

## Componentes principales

- Backend: FastAPI, Uvicorn, SQLAlchemy (async), Alembic, Pydantic.
- Frontend: React, Vite, Tailwind CSS, Axios.
- IA: integración con Google Gemini y Anthropic Claude vía SDKs.
- DB: PostgreSQL con índices y foreign keys para integridad.

## Maestros (concepto)

- LLM Maestro: gestión centralizada de modelos y límites.
- Prompt Maestro: plantillas y variables dinámicas.
- Estilo Maestro: directrices de tono y formato.
- Secciones: organización de contenido.
- Salida Maestro: mapping para canales (Web, Impreso, Redes).

--
Última actualización: 2025-10-30
