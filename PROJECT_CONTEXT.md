# 🧠 CONTEXTO DEL PROYECTO - Sistema de Noticias con IA

> **Documento maestro para Claude AI**  
> Este archivo contiene toda la información clave del proyecto para mantener contexto entre conversaciones.

---

## 📋 INFORMACIÓN GENERAL

| Campo | Valor |
|-------|-------|
| **Nombre** | Sistema de Noticias con IA |
| **Versión** | 2.3.0-alpha |
| **Estado** | ✅ Desarrollo activo - Fase 6 en planificación |
| **Desarrollador** | hromero |
| **Stack Principal** | FastAPI + React + PostgreSQL + Claude AI (Multi-LLM) |
| **Repositorio** | D:\hromero\Desktop\projects\sistema-noticias-ia |
| **Última actualización** | 2025-10-16 |

---

## 🎯 DESCRIPCIÓN DEL PROYECTO

Sistema profesional de gestión de noticias con **autenticación JWT**, **PostgreSQL**, **sistema de maestros** e integración de inteligencia artificial multi-proveedor. Permite crear, gestionar y analizar noticias con **múltiples salidas optimizadas** por canal de publicación (impreso, web, redes sociales).

### Características Principales:
- 🔐 Autenticación JWT con sistema de roles (Admin, Editor, Viewer)
- 📰 CRUD completo de noticias con PostgreSQL
- 🤖 Integración Multi-LLM (Claude, GPT-4, Gemini)
- 📋 Sistema de Maestros (LLM, Prompts, Estilos, Secciones, Salidas)
- 📤 Generación automática de contenido por canal
- 🎨 UI moderna con React + Tailwind CSS + Modo Oscuro
- 🔍 Búsqueda y filtrado en tiempo real
- 🌍 Interfaz completamente en español

---

## 📅 EVOLUCIÓN DEL PROYECTO

### Resumen de Fases

| Fase | Versión | Estado | Descripción |
|------|---------|--------|-------------|
| 1 | v1.0.0 | ✅ Completada | MVP Inicial - Base funcional |
| 2 | v2.0.0 | ✅ Completada | Migración a PostgreSQL |
| 3 | v2.1.0 | ✅ Completada | Sistema de Autenticación JWT |
| 4 | v2.2.0 | ✅ Completada | Rediseño UI/UX + Temas |
| 5 | v2.2.1 | 🔄 En desarrollo | Sistema de Proyectos |
| 6 | v2.3.0 | 📝 Planificación | **Maestros + Multi-Salidas** |

---

### Fase 6: Sistema de Maestros y Gestión Avanzada (v2.3.0) 🔄 EN PROGRESO
**Período**: 2025-10-16 → Estimado 2-2.5 meses  
**Objetivo**: Transformar el sistema en una plataforma profesional con gestión flexible mediante maestros independientes

#### 🎯 Objetivos Principales:

**1. Sistema de Maestros (5 maestros):**
- 📦 **LLM Maestro**: Claude, GPT-4, Gemini con configuración de APIs
- 📝 **Prompt Maestro**: Plantillas reutilizables con variables dinámicas
- 🎨 **Estilo Maestro**: Directivas de tono, longitud y formato
- 📋 **Secciones**: Reemplazo de Category con configuración IA
- 📤 **Salida Maestro**: Canales (impreso, web, twitter, instagram)

**2. Generación Multi-Salida:**
- Genera automáticamente contenido optimizado por canal
- Pestañas en noticia para ver cada salida
- Metadatos de generación (LLM, prompt, estilo usado)

**3. Cambios Conceptuales:**
- ❌ Eliminar `categoria` → ✅ `secciones` (tabla relacional)
- ✅ Relación Noticia ↔ Salidas (M2M)
- ✅ UI completamente en español

#### 📊 Progreso de Implementación:

**Fase 6.1: Base de Datos** ✅ COMPLETADA (2025-10-17)
- ✅ 6 tablas creadas (llm_maestro, prompt_maestro, estilo_maestro, seccion, salida_maestro, noticia_salida)
- ✅ 18 índices para optimización
- ✅ Datos de ejemplo insertados (3 LLMs, 3 prompts, 3 estilos, 6+ secciones, 5 salidas)
- ✅ Migración de categorías → secciones
- ✅ Columna seccion_id agregada a tabla noticias
- ✅ Triggers de updated_at configurados
- 📝 Script: `backend/migrations/fase_6_maestros_v3.sql`

**Fase 6.2: Modelos ORM y Schemas** ✅ COMPLETADA (2025-10-17)
- ✅ 6 modelos SQLAlchemy agregados a `orm_models.py`
- ✅ 30+ schemas Pydantic en `schemas_fase6.py`
- ✅ Validaciones y relaciones configuradas
- ✅ Enums para proveedores, tipos de salida, categorías
- ✅ Schemas con/sin API key para seguridad
- 📝 Archivos: `backend/models/orm_models.py`, `backend/models/schemas_fase6.py`

**Fase 6.3: Backend - Routers CRUD** ✅ COMPLETADA (2025-10-17)
- ✅ Router LLM Maestro (`llm_maestro.py`) - 11 endpoints
- ✅ Router Prompts (`prompts.py`) - 8 endpoints + validación
- ✅ Router Estilos (`estilos.py`) - 7 endpoints
- ✅ Router Secciones (`secciones.py`) - 9 endpoints + asignaciones
- ✅ Router Salidas (`salidas.py`) - 8 endpoints
- ✅ Total: 43 nuevos endpoints REST
- ✅ Autenticación JWT integrada (admin/user)
- ✅ `main.py` actualizado con nuevos routers
- 📝 Archivos: `backend/routers/*.py`, `backend/main.py`

**Fase 6.4: Backend - Servicio de Generación IA** ✅ COMPLETADA (2025-10-17)
- ✅ Clase `GeneradorIA` multi-LLM (Anthropic, OpenAI, Google)
- ✅ Procesamiento de prompts con variables dinámicas
- ✅ Aplicación de estilos a prompts
- ✅ Generación optimizada por tipo de salida
- ✅ Soporte para generación múltiple
- ✅ Router `/api/generar` con 5 endpoints
- ✅ Frontend: Modal generación + Componente salidas
- 📝 Archivos: `backend/services/generador_ia.py`, `backend/routers/generacion.py`

**Fase 6.5: Frontend - Componentes Maestros** ⚠️ PARCIAL (18% completado)
- ✅ Servicio API `maestros.js` (5 servicios + constantes)
- ✅ Componente `Maestros.jsx` con tabs de navegación
- ✅ 5 componentes de LISTA: LLMMaestroList, PromptsList, EstilosList, SeccionesList, SalidasList
- ⚠️ Listas funcionan pero botones NO hacen nada
- ❌ **FALTA: Formularios de crear/editar** (0/5 implementados)
- ❌ **FALTA: Botones eliminar funcionales**
- ❌ **FALTA: Modales de confirmación**
- 📝 Archivos: `frontend/src/services/maestros.js`, `frontend/src/components/Maestros*.jsx`

**Fase 6.7: Frontend - Formularios CRUD** ❌ PENDIENTE (0% completado)
- [ ] LLMForm.jsx - Crear/editar modelos IA
- [ ] PromptForm.jsx - Crear/editar prompts
- [ ] EstiloForm.jsx - Crear/editar estilos
- [ ] SeccionForm.jsx - Crear/editar secciones
- [ ] SalidaForm.jsx - Crear/editar salidas
- [ ] DeleteConfirmModal.jsx - Modal de confirmación
- [ ] Integrar formularios con componentes de lista
- [ ] Implementar funcionalidad de botones

**Fase 6.6: Testing y Documentación** ✅ COMPLETADA (2025-10-17)
- ✅ Tests unitarios para GeneradorIA (15+ tests)
- ✅ Tests de integración para routers
- ✅ Guía de usuario completa (200+ líneas)
- ✅ CHANGELOG detallado
- ✅ Documentación de API actualizada
- ✅ README principal actualizado
- 📝 Archivos: `backend/tests/*.py`, `GUIA_USUARIO.md`, `CHANGELOG.md`

**Documentación:**
- ✅ `PLAN_FASE_6.md` creado (300+ líneas, plan completo)
- ✅ `backend/migrations/fase_6_maestros_v3.sql` (migración exitosa)

**Estado**: ⚠️ EN PROGRESO - Falta Fase 6.7 (Formularios Frontend)  
**Prioridad**: CRITICA - Sistema no funcional sin formularios  
**Inicio**: 2025-10-16  
**Última actualización**: 2025-10-17

**Progreso general:** 85% completado (6/7 fases, Fase 6.5 parcial)

---

## 🚨 CARPETAS EXCLUIDAS

**⚠️ IMPORTANTE - NO explorar estas carpetas:**
- ❌ `D:\hromero\Desktop\projects\sistema-noticias-ia\frontend\node_modules`
- ❌ `D:\hromero\Desktop\projects\sistema-noticias-ia\backend\venv`
- ❌ `__pycache__`
- ❌ `.git`

**Razón**: Contienen miles de archivos y causan errores de tamaño/timeout.

---

## 💻 STACK TECNOLÓGICO ACTUAL

### Backend
```
Python 3.11+
├── FastAPI 0.118.0
├── SQLAlchemy 2.0.44
├── PostgreSQL 12.10
├── Anthropic 0.69.0 (Claude)
├── OpenAI (próximamente)
├── Google Generative AI (próximamente)
├── python-jose 3.3.0 (JWT)
└── bcrypt 4.0.1
```

### Frontend
```
Node.js 18+
├── React 18.2.0
├── Vite 5.0.8
├── Tailwind CSS 3.4.0
└── Lucide React 0.263.1
```

---

## 📂 ESTRUCTURA DE ARCHIVOS (ACTUALIZADA)

```
sistema-noticias-ia/
├── backend/
│   ├── routers/
│   │   ├── llm.py              🆕 FASE 6 - Maestro LLM
│   │   ├── prompts.py          🆕 FASE 6 - Maestro Prompts
│   │   ├── estilos.py          🆕 FASE 6 - Maestro Estilos
│   │   ├── secciones.py        🆕 FASE 6 - Secciones (ex-categorías)
│   │   ├── salidas.py          🆕 FASE 6 - Maestro Salidas
│   │   └── ...
│   │
│   ├── services/
│   │   └── generacion_ia.py    🆕 FASE 6 - Generador Multi-LLM
│   │
│   └── migrations/
│       └── fase_6_maestros.sql 🆕 FASE 6 - SQL completo
│
├── frontend/src/
│   └── components/
│       └── maestros/            🆕 FASE 6 - 10 componentes nuevos
│           ├── LLMList.jsx
│           ├── LLMForm.jsx
│           ├── PromptList.jsx
│           ├── PromptForm.jsx
│           ├── EstiloList.jsx
│           ├── EstiloForm.jsx
│           ├── SeccionList.jsx
│           ├── SeccionForm.jsx
│           ├── SalidaList.jsx
│           └── SalidaForm.jsx
│
└── docs/
    ├── PLAN_FASE_6.md          ✅ CREADO - Plan detallado 300+ líneas
    ├── PROJECT_CONTEXT.md       ✅ ACTUALIZADO - Este archivo
    └── ...
```

---

## ⚡ COMANDOS ESENCIALES

### Desarrollo Diario
```bash
# Backend (Terminal 1)
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Frontend (Terminal 2)
cd frontend && npm run dev
```

### Ver Documentación Completa Fase 6
```bash
# Leer plan detallado
cat PLAN_FASE_6.md

# O abrir en editor
code PLAN_FASE_6.md
```

---

## 🔮 ROADMAP ACTUALIZADO

### Fase 6 (v2.3.0) - PRÓXIMA ⏰
- [ ] Sistema de 5 maestros (LLM, Prompt, Estilo, Sección, Salida)
- [ ] Generación multi-LLM (Claude, GPT-4, Gemini)
- [ ] Generación multi-salida (impreso, web, redes)
- [ ] Traducción completa a español
- [ ] Migración Category → Secciones

### Fase 7 (v2.4.0) - Futuro
- [ ] Dashboard con estadísticas
- [ ] Sistema de comentarios
- [ ] Notificaciones en tiempo real

### Fase 8 (v3.0.0) - Largo plazo
- [ ] Mobile App (React Native)
- [ ] Búsqueda avanzada (Elasticsearch)
- [ ] Internacionalización (i18n)

---

## 📊 MÉTRICAS ACTUALES

| Métrica | Valor |
|---------|-------|
| **Líneas de código** | ~4,500 |
| **Archivos** | 58 |
| **Endpoints API** | 20+ (→ 35+ en Fase 6) |
| **Tablas BD** | 6 (→ 12 en Fase 6) |
| **Componentes React** | 10 (→ 20 en Fase 6) |
| **Tests coverage** | 70% |

---

## 🎯 RESUMEN EJECUTIVO

Sistema profesional de gestión de noticias con IA en **6 fases**:

1. ✅ MVP Inicial (v1.0.0)
2. ✅ PostgreSQL (v2.0.0)
3. ✅ Autenticación JWT (v2.1.0)
4. ✅ Sistema de Temas (v2.2.0)
5. 🔄 Proyectos (v2.2.1 - en desarrollo)
6. 📝 **Maestros + Multi-Salidas (v2.3.0 - planificación)** ⭐ NUEVA

**Próximo gran hito**: Fase 6 - Sistema de maestros con generación multi-LLM y multi-salida

---

**📝 Última actualización**: 2025-10-16  
**📌 Versión**: 2.3.0-alpha  
**✍️ Mantenido por**: hromero  
**🤖 Asistente**: Claude (Anthropic)
