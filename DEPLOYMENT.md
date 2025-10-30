<!-- Copia local: la fuente canónica está en ./docs/ -->
# DEPLOYMENT — Preparación para producción

Pasos resumidos para desplegar:

1. Configurar variables de entorno:

```bash
DEBUG=False
SECRET_KEY=<clave-segura>
DATABASE_URL=<postgresql-produccion>
ALLOWED_ORIGINS=https://tu-dominio.com
```

2. Build frontend:

```bash
cd frontend
npm run build
# Archivos en dist/
```

3. Usar Nginx o Caddy como reverse proxy y configurar HTTPS (Let's Encrypt).
4. Base de datos administrada (RDS, Railway, etc.) y backups.

Opciones: Railway, Render, Heroku, AWS (EC2/ECS + RDS)
