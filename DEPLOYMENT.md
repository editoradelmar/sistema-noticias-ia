# 🚀 Guía de Despliegue a Producción

Esta guía cubre el despliegue del Sistema de Noticias con IA en diferentes plataformas.

---

## 📋 Requisitos Previos

- **Cuenta en plataforma de hosting** (Railway, Render, Heroku, AWS, etc.)
- **Docker instalado** (para deployment con contenedores)
- **Variables de entorno configuradas**
- **Dominio** (opcional pero recomendado)

---

## ☁️ Opción 1: Railway.app (Recomendado)

Railway es ideal para proyectos fullstack Python + Node.js.

### Backend (FastAPI)

1. **Crear nuevo proyecto en Railway:**
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init
```

2. **Configurar variables de entorno en Railway:**
```env
PYTHON_VERSION=3.11
DEBUG=False
ANTHROPIC_API_KEY=tu_api_key
ALLOWED_ORIGINS=https://tu-frontend.railway.app
```

3. **Crear `railway.json` en la raíz del backend:**
```json
{
  "build": {
    "builder": "nixpacks",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

4. **Deploy:**
```bash
railway up
```

### Frontend (React)

1. **Configurar build en `package.json`:**
```json
{
  "scripts": {
    "build": "vite build",
    "preview": "vite preview --port $PORT"
  }
}
```

2. **Crear `.env.production`:**
```env
VITE_API_URL=https://tu-backend.railway.app/api
```

3. **Deploy:**
```bash
railway up
```

---

## 🌐 Opción 2: Render.com

Render ofrece plan gratuito y es muy fácil de usar.

### Backend

1. **Crear `render.yaml`:**
```yaml
services:
  - type: web
    name: noticias-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DEBUG
        value: False
```

2. **Conectar repositorio GitHub** y Render detectará automáticamente la configuración.

### Frontend

1. **Configuración de build:**
```yaml
services:
  - type: web
    name: noticias-frontend
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm run preview
    envVars:
      - key: VITE_API_URL
        value: https://noticias-backend.onrender.com/api
```

---

## 🐳 Opción 3: Docker + VPS (Más control)

Para deploy en VPS (DigitalOcean, Linode, AWS EC2, etc.)

### 1. Preparar docker-compose para producción

**Crear `docker-compose.prod.yml`:**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      target: production
    restart: always
    environment:
      - DEBUG=False
      - ALLOWED_ORIGINS=${FRONTEND_URL}
    ports:
      - "8000:8000"
    networks:
      - app-network

  frontend:
    build:
      context: ./frontend
      target: production
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    restart: always
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    ports:
      - "443:443"
    depends_on:
      - frontend
      - backend
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 2. Configurar Nginx como reverse proxy

**Crear `nginx/nginx.conf`:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name tudominio.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS
    server {
        listen 443 ssl http2;
        server_name tudominio.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend API
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # Health check
        location /health {
            proxy_pass http://backend/health;
        }
    }
}
```

### 3. Deploy en VPS

```bash
# En el servidor
git clone tu-repositorio
cd sistema-noticias-ia

# Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con valores de producción

# Build y deploy
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🔒 SSL/TLS con Let's Encrypt

Para HTTPS gratuito:

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Renovación automática (crontab)
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 📊 Monitoreo y Logging

### 1. Configurar logging en producción

**Backend `main.py`:**
```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logging
handler = RotatingFileHandler('logs/app.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logging.getLogger().addHandler(handler)
```

### 2. Monitoreo con Docker

```bash
# Ver recursos
docker stats

# Ver logs en tiempo real
docker-compose logs -f --tail=100
```

---

## 🔄 CI/CD con GitHub Actions

**Crear `.github/workflows/deploy.yml`:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to VPS
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.VPS_HOST }}
        username: ${{ secrets.VPS_USER }}
        key: ${{ secrets.VPS_SSH_KEY }}
        script: |
          cd /app/sistema-noticias-ia
          git pull origin main
          docker-compose -f docker-compose.prod.yml up -d --build
```

---

## ⚡ Optimizaciones de Producción

### Backend

1. **Usar Gunicorn con Uvicorn workers:**
```bash
pip install gunicorn

# Ejecutar
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. **Configurar límites:**
```python
# En main.py
app = FastAPI(
    title="API Producción",
    docs_url=None,  # Deshabilitar docs en producción
    redoc_url=None
)
```

### Frontend

1. **Optimizar build:**
```javascript
// vite.config.js
export default defineConfig({
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true
      }
    }
  }
})
```

---

## 🐛 Troubleshooting en Producción

### Backend no inicia

```bash
# Ver logs
docker logs nombre-contenedor

# Verificar variables de entorno
docker exec nombre-contenedor env

# Health check manual
curl http://localhost:8000/health
```

### Frontend no conecta con backend

1. Verificar CORS en `config.py`
2. Verificar `VITE_API_URL` en variables de entorno
3. Revisar logs de Nginx

### Alto uso de memoria

```bash
# Limitar recursos en docker-compose
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

---

## 📈 Escalado

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
      
  nginx:
    # Load balancing automático entre replicas
```

### Base de datos para producción

Migrar de almacenamiento en memoria a PostgreSQL:

```python
# Instalar
pip install sqlalchemy psycopg2-binary

# Configurar conexión
DATABASE_URL = "postgresql://user:password@host:5432/dbname"
```

---

## ✅ Checklist de Producción

- [ ] Variables de entorno configuradas
- [ ] Debug mode desactivado
- [ ] HTTPS habilitado
- [ ] CORS configurado correctamente
- [ ] API keys seguras
- [ ] Logging configurado
- [ ] Backups automatizados
- [ ] Monitoreo activado
- [ ] Health checks funcionando
- [ ] Rate limiting implementado
- [ ] Documentación actualizada

---

## 🆘 Soporte

Para problemas de deployment, crear un issue en el repositorio con:
- Plataforma de hosting
- Logs de error
- Configuración actual

---

**¡Tu aplicación está lista para producción! 🎉**