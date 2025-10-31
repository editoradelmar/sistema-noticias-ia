# AGENT DIRECTIVES — Instrucciones persistentes para agentes AI

Propósito: Proveer directivas que los agentes (Copilot / asistentes automatizados) deben seguir por defecto al trabajar en este repositorio. Evita repetirlas en cada chat.

## 1) Objetivo
- Revisar, editar y probar el proyecto "sistema-noticias-ia" (FastAPI + React). Priorizar seguridad y evitar exponer secretos.

## 2) Reglas principales
- Nunca commitear claves ni secret tokens. Si hace falta usar una clave, cargarla desde `.env` o GitHub Secrets y documentarlo en el PR.
- Antes de cualquier cambio ejecutar tests relevantes y verificar que no se rompa la build (backend: `pytest -v`, frontend: `npm test`).
- Seguir convenciones de UI: reusar servicios en `frontend/src/services/*`, usar `useAuth()` y `useTheme()` en componentes nuevos, replicar estilos de `ProyectoForm.jsx`.
- Para IA: si falta API key, usar modo simulado y documentar claramente en el commit/PR que se usó modo simulado.

 - Antes de RESPONDER a preguntas que impliquen cambios técnicos, diseños de integración o recomendaciones de código, revisar a profundidad tanto el backend como el frontend: identificar puntos de entrada (por ejemplo `backend/main.py`, routers en `backend/routers/`, `frontend/src/main.jsx`, `frontend/src/App.jsx`), los servicios relevantes (`backend/services`, `frontend/src/services`) y las configuraciones que puedan verse afectadas. Documentar brevemente qué archivos se consultaron y por qué. Esta revisión es obligatoria y previa a cualquier propuesta de cambio.

### Nueva directiva obligatoria — Propuesta antes de generar código
- Antes de empezar a generar o modificar código, realiza un análisis detallado (impacto, archivos a tocar, tests afectados, riesgos de seguridad) y prepara una propuesta escrita (lista de cambios o diff/patch sugerido). Espera la aprobación explícita del mantenedor o del solicitante antes de crear o modificar archivos en el repositorio.

### Requerimiento de idioma
- Todas las respuestas técnicas, análisis, propuestas y mensajes que se dejen en issues/PRs/commits deben estar en ESPAÑOL por defecto.

### Regla estricta de no-generación sin propuesta y aprobación
- NO GENERAR NINGÚN PARCHÉ O CÓDIGO SIN ANTES PRESENTAR UN ANÁLISIS DETALLADO Y UNA PROPUESTA (en español) QUE INCLUYA:
	1) Qué archivos se van a modificar y por qué;
	2) Un resumen de los cambios propuestos (pequeño diff conceptual o lista de ediciones);
	3) Un plan de verificación rápido (tests/validaciones a correr);
	4) Esperar confirmación explícita del mantenedor o revisor responsable antes de aplicar cambios al repositorio.

Si un agente no respeta estas reglas, sus cambios deben revisarse manualmente y no fusionarse hasta recibir aprobación humana.

## 3) Prioridades
- 1) Seguridad (secretos/SECRET_KEY/API keys)
- 2) Bugs críticos (errores que impiden arranque o pruebas)
- 3) Calidad (tests mínimos + lint)

## 4) Qué hacer si falta información
- Tomar hasta 2 supuestos razonables, documentarlos en el commit/PR y dejar comentario para revisión.

## 5) Dónde colocar directivas adicionales
- Preferible: `.github/copilot-instructions.md` (archivo de referencia para agentes), `.github/AGENT_DIRECTIVES.md` (este archivo) o `docs/AGENT_DIRECTIVES.md` si se quiere versión visible públicamente en la documentación.

## 6) Contacto del owner
- Hector Romero — hromero@eluniversal.com.co

---

Si quieres que actualice este archivo con más reglas (por ejemplo, formato de commit, CI checks obligatorias o plantillas de PR), dime y lo añado.
