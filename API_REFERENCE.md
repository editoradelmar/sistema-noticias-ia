<!-- Copia local: la fuente canónica está en ./docs/ -->
# API_REFERENCE — Resumen de endpoints

Esta es una copia rápida de referencia. Para la documentación completa en Swagger, ejecutar el backend y abrir `/docs`.

## Autenticación

POST /api/auth/register — Registrar usuario

POST /api/auth/login — Login (form)

POST /api/auth/login/json — Login (JSON)

GET /api/auth/me — Obtener perfil (Bearer token)

POST /api/auth/logout — Cerrar sesión

## Noticias

GET /api/noticias/ — Listar noticias (filtros disponibles)
GET /api/noticias/{id} — Obtener noticia por id
POST /api/noticias/ — Crear noticia (Admin/Editor)
PUT /api/noticias/{id} — Actualizar noticia (Admin/Owner)
DELETE /api/noticias/{id} — Eliminar noticia (Admin/Owner)

## IA

POST /api/ai/resumir/{id} — Generar resumen de noticia
POST /api/ai/chat — Chat con IA (mensaje + contexto)

--
Nota: Para detalles de request/response y modelos, abrir la UI Swagger en http://localhost:8000/docs
