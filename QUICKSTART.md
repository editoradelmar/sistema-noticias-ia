
# 🐙 Integración rápida con Git/GitHub

```bash
git init
git remote add origin https://github.com/<usuario>/<repositorio>.git
git add .
git commit -m "init: estructura base"
git branch -M main
git push -u origin main
```

Para cada nueva funcionalidad, crea una rama y abre un Pull Request siguiendo la [Guía de Contribución](./CONTRIBUTING.md).


Guía ultra-rápida para poner el proyecto en marcha en **5 minutos**.

---

## 🎯 Lo que vas a construir

Sistema completo de noticias con:
- ✅ CRUD de noticias
- 🤖 Resúmenes automáticos con Claude IA
- 💬 Chat inteligente
- 📊 Categorización y búsqueda
- 🎨 UI moderna y responsive

**Stack:** FastAPI + React + Claude + Vite + Tailwind CSS

---

## 🚀 Instalación Express (Linux/Mac)

```bash
# 1. Clonar/crear estructura
mkdir sistema-noticias-ia && cd sistema-noticias-ia

# 2. Backend
mkdir backend && cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic anthropic httpx python-dotenv pydantic-settings

# 3. Frontend  
cd .. && npx create-vite@latest frontend --template react
cd frontend
npm install
npm install lucide-react

# 4. Listo! Ahora copia los archivos proporcionados
```

## 🪟 Instalación Express (Windows)

```powershell
# 1. Crear estructura
mkdir sistema-noticias-ia
cd sistema-noticias-ia

# 2. Backend
mkdir backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn pydantic anthropic httpx python-dotenv pydantic-settings

# 3. Frontend
cd ..
npx create-vite@latest frontend --template react
cd frontend
npm install
npm install lucide-react
```

---

## 📁 Archivos Esenciales

### Backend (copiar en orden)

1. `backend/main.py` - ⭐ Aplicación principal
2. `backend/config.py` - Configuración
3. `backend/requirements.txt` - Dependencias
4. `backend/models/schemas.py` - Modelos de datos
5. `backend/routers/__init__.py` - Init routers
6. `backend/routers/noticias.py` - Endpoints CRUD
7. `backend/routers/ai.py` - Endpoints IA

### Frontend (reemplazar)

1. `frontend/src/App.jsx` - ⭐ Componente principal
2. `frontend/vite.config.js` - Config de Vite
3. `frontend/package.json` - Actualizar dependencias

---

## ▶️ Ejecutar (Método 1 - Manual)

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
uvicorn main:app --reload
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

**Abrir:** http://localhost:5173

---

## ▶️ Ejecutar (Método 2 - Con Makefile)

```bash
# Instalar todo
make install

# Ejecutar backend
make dev-backend

# Ejecutar frontend (en otra terminal)
make dev-frontend

# Ver todos los comandos
make help
```

---

## ▶️ Ejecutar (Método 3 - Docker)

```bash
# Build y run
docker-compose up --build

# En background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 🎮 Primeros Pasos en la App

1. **Abrir** http://localhost:5173
2. **Cargar datos:** Click en "Cargar Ejemplos"
3. **Crear noticia:** Click en "Crear" → llenar formulario
4. **Generar resumen:** Click en "Generar resumen con IA"
5. **Chat:** Click en "Chat IA" → hacer preguntas

---

## 📊 Estructura del Proyecto

```
sistema-noticias-ia/
├── backend/              ← API FastAPI
│   ├── main.py          ← ⭐ IMPORTANTE
│   ├── config.py
│   ├── models/
│   │   └── schemas.py   ← ⭐ IMPORTANTE
│   └── routers/
│       ├── noticias.py  ← ⭐ IMPORTANTE
│       └── ai.py        ← ⭐ IMPORTANTE
│
└── frontend/            ← UI React
    ├── src/
    │   └── App.jsx      ← ⭐ IMPORTANTE
    └── vite.config.js
```

---

## 🔧 Comandos Útiles

### Backend
```bash
# Docs interactivas
http://localhost:8000/docs

# Health check
curl http://localhost:8000/health

# Ver todas las noticias
curl http://localhost:8000/api/noticias/

# Crear datos de ejemplo
curl -X POST http://localhost:8000/api/noticias/seed
```

### Tests
```bash
# Backend
cd backend && pytest -v

# Ver coverage
pytest --cov=. --cov-report=html
```

---

## 🐛 Solución de Problemas Comunes

### ❌ "Connection refused" en frontend

**Problema:** Frontend no puede conectar con backend

**Solución:**
```bash
# Verificar que backend esté corriendo
curl http://localhost:8000/health

# Verificar CORS en backend/config.py
ALLOWED_ORIGINS = ["http://localhost:5173"]
```

### ❌ "Module not found" en backend

**Solución:**
```bash
# Activar venv
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### ❌ Error de importación en routers

**Solución:**
```bash
# Verificar que existe __init__.py
touch routers/__init__.py
touch models/__init__.py
```

### ❌ Frontend muestra página en blanco

**Solución:**
```bash
# Limpiar cache y reinstalar
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📖 Endpoints Principales

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/noticias/` | Lista todas las noticias |
| POST | `/api/noticias/` | Crea noticia |
| DELETE | `/api/noticias/{id}` | Elimina noticia |
| POST | `/api/ai/resumir/{id}` | Genera resumen |
| POST | `/api/ai/chat` | Chat con IA |
| GET | `/health` | Estado del servidor |
| GET | `/docs` | Documentación Swagger |

---

## 🎨 Personalización Rápida

### Cambiar colores (Frontend)

Editar `App.jsx`:
```javascript
// Buscar y reemplazar
bg-purple-600  →  bg-blue-600
bg-purple-50   →  bg-blue-50
```

### Agregar nueva categoría (Backend)

En `models/schemas.py`:
```python
class CategoriaNoticia(str, Enum):
    TECNOLOGIA = "tecnologia"
    # ... existentes
    TU_NUEVA = "tu_nueva"  # ← Agregar aquí
```

### Cambiar puerto del backend

```bash
uvicorn main:app --reload --port 9000
```

### Cambiar puerto del frontend

En `vite.config.js`:
```javascript
server: {
  port: 3000  // Cambiar de 5173 a 3000
}
```

---

## 📚 Recursos Adicionales

- **README.md** - Documentación completa
- **DEPLOYMENT.md** - Guía de producción
- **Makefile** - Comandos automatizados
- **Backend Docs** - http://localhost:8000/docs

---

## 🔥 Comandos de Un Solo Línea

```bash
# Instalación completa
git clone repo && cd repo && make install

# Iniciar todo
make dev

# Docker todo-en-uno
docker-compose up --build

# Tests completos
make test

# Limpiar todo
make clean

# Backup
make backup
```

---

## ⚡ Next Steps

1. ✅ Terminar instalación
2. ✅ Ejecutar proyecto
3. 📝 Revisar código en archivos marcados con ⭐
4. 🎨 Personalizar UI
5. 🚀 Agregar features
6. 🌐 Deploy a producción

---

## 🆘 Ayuda Rápida

**¿Algo no funciona?**

1. Verificar que Python 3.8+ y Node 18+ estén instalados
2. Revisar logs en ambas terminales
3. Verificar que todos los archivos estén en su lugar
4. Consultar README.md completo
5. Abrir issue en GitHub

---

## ✨ Features para Implementar

Ideas para extender el proyecto:

- [ ] Autenticación JWT
- [ ] Base de datos PostgreSQL
- [ ] Upload de imágenes
- [ ] Exportar a PDF
- [ ] Notificaciones push
- [ ] Sistema de comentarios
- [ ] Analytics dashboard
- [ ] Tests E2E con Playwright
- [ ] CI/CD con GitHub Actions
- [ ] Modo oscuro

---

**¡Listo! Ahora tienes un sistema completo de noticias con IA funcionando. 🎉**

Para más detalles, consulta **README.md** y **DEPLOYMENT.md**.