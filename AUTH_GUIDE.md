<!-- Copia local: la fuente canónica está en ./docs/ -->
# AUTH_GUIDE — Guía de Autenticación

## Flujo

1. Usuario envía credenciales (email + password).
2. Backend valida y genera JWT (vigencia por defecto 30 min).
3. Frontend guarda token en `localStorage` y lo envía en `Authorization: Bearer <token>`.

## Endpoints

- POST /api/auth/login (form-urlencoded)
- POST /api/auth/login/json (JSON)
- GET /api/auth/me

## Roles

- admin: acceso completo
- editor: crear/editar sus noticias
- viewer: solo lectura
