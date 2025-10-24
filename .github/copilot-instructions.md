<!-- .github/copilot-instructions.md - Guía corta para agentes AI que trabajen en este repo -->
# Instrucciones rápidas para agentes de codificación

Objetivo: ayudar a un agente AI a ser productivo de inmediato en este repositorio "sistema-noticias-ia" (FastAPI + React + Claude).

- Leer primero: `README.md`, `ARCHITECTURE.md`, `AUTH_GUIDE.md` — contienen el panorama y comandos de arranque.
- Punto de entrada (backend): `backend/main.py`. API routers en `backend/routers/` (ej: `noticias.py`, `ai.py`, `auth.py`).
- Punto de entrada (frontend): `frontend/src/main.jsx` y `frontend/src/App.jsx`. Componentes en `frontend/src/components/`.

Reglas de estilo y componentes a seguir
- UI: usa Tailwind CSS con clases `dark:`. Copiar patrones visuales existentes (ej: `ProyectoForm.jsx`) para nuevos formularios y botones.
- Contextos: `AuthContext` y `ThemeContext` son la fuente de verdad para permisos y tema (usar `useAuth()` y `useTheme()` en componentes nuevos).
- Servicios HTTP: todas las llamadas HTTP van a través de `frontend/src/services/api.js` y servicios específicos en `frontend/src/services/*.js` (ej: `maestros.js`). Usar esos servicios en lugar de fetch directo cuando sea posible.

API y contratos comunes
- Autenticación: OAuth2 form login en `/api/auth/login` (usar `username` en el body form). Frontend guarda `token` y `user` en localStorage. Ver `AuthContext.jsx`.
- Form callbacks: los formularios usan la convención `onSave(data, setLoading, setError)` o `onClose(updated)`. Revisar `ProyectoForm.jsx` y `LLMMaestroForm.jsx` para ejemplos.
- Servicios maestros: `llmService`, `promptService`, `estiloService`, `seccionService`, `salidaService` exportan métodos CRUD (getAll, getById, create, update, delete, toggleActivo). Reutilizarlos.

Prácticas específicas del repo
- Siempre respetar roles: usar `isAdmin()` o `canEdit()` desde `useAuth()` para mostrar/ocultar acciones sensibles.
- Evitar exponer API keys: las rutas que devuelven claves usan `/with-key` y suelen estar protegidas por admin. No tocar almacenamiento de claves sin revisión.
- Para cambios visuales, replicar las clases y estructura de `ProyectoForm.jsx` y `ProyectosList.jsx` para mantener coherencia.

Comandos útiles (desarrollo)
- Backend (dev):
  - Activar entorno Python y correr: `cd backend ; venv\Scripts\activate ; uvicorn main:app --reload` (Windows)
  - Tests backend: `cd backend ; pytest -v`
- Frontend (dev):
  - Instalar / ejecutar: `cd frontend ; npm install ; npm run dev`
  - Tests frontend: `cd frontend ; npm test`

Archivos clave y dónde mirar ejemplos
- Autenticación: `backend/routers/auth.py`, `frontend/src/context/AuthContext.jsx`.
- Maestros API: `backend/routers/llm_maestro.py` (si existe) y `frontend/src/services/maestros.js`.
- Formularios y estilos de referencia: `frontend/src/components/ProyectoForm.jsx`, `ProyectosList.jsx`.
- Theme & layout: `frontend/src/context/ThemeContext.jsx`, `index.css`, `tailwind.config.js`.

Errores comunes y cómo detectarlos
- Duplicate export/default: buscar múltiples `export default` en un archivo modificado.
- Mismatch de contrato entre form y list: confirmar firma de `onSave` y comportamiento (ej. si `onSave` debe cerrar modal o devolver booleano).
- Problemas CORS / Network: comprobar `backend/.env` / `config.py` ALLOWED_ORIGINS y que backend esté escuchando en `localhost:8000`.

Checklist rápido antes de crear PR
1. Ejecutar `npm run dev` (frontend) y `uvicorn main:app --reload` (backend) localmente.
2. Revisar `AuthContext`/`ThemeContext` para uso correcto.
3. Reutilizar servicios en `frontend/src/services/` para llamadas HTTP.
4. Mantener consistencia de UI con `ProyectoForm.jsx` (botones, inputs, errores, header gradient).
5. Añadir pruebas mínimas si el cambio altera lógica (backend: pytest, frontend: jest).

Si algo no está claro, preguntar al mantenedor: revisar `CONTRIBUTING.md` para contactos y el flujo de PR.

---
Por favor revisa este borrador. Indica si deseas que fusione contenido adicional del README o que añada ejemplos de código concretos dentro de cada sección.
