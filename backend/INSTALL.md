# 📦 Instalación de Dependencias - Backend

## 🚀 Instalación Básica (Requerida)

### 1. Crear entorno virtual (si no existe)
```bash
cd backend
python -m venv venv
```

### 2. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias básicas
```bash
pip install -r requirements.txt --break-system-packages
```

Esta instalación incluye:
- ✅ FastAPI + Uvicorn (Framework web)
- ✅ SQLAlchemy + PostgreSQL (Base de datos)
- ✅ JWT + Bcrypt (Autenticación)
- ✅ Anthropic (Claude API) - **Proveedor principal**

---

## 🔧 Instalación Opcional (Proveedores IA adicionales)

### OpenAI (GPT-4, GPT-3.5)
```bash
pip install openai==1.58.1 --break-system-packages
```

### Google Gemini
```bash
pip install google-generativeai==0.8.3 --break-system-packages
```

### Todas las dependencias opcionales
```bash
pip install -r requirements-optional.txt --break-system-packages
```

---

## 📋 Verificar instalación

```bash
pip list
```

Deberías ver:
- `fastapi` (0.118.0)
- `uvicorn` (0.37.0)
- `sqlalchemy` (2.0.44)
- `anthropic` (0.69.0)
- `python-jose` (3.5.0)
- Y más...

---

## 🔍 Proveedores de IA Disponibles

| Proveedor | Requerido | Paquete | Estado |
|-----------|-----------|---------|--------|
| **Anthropic (Claude)** | ✅ Sí | `anthropic==0.69.0` | ✅ Instalado |
| **OpenAI (GPT)** | ❌ Opcional | `openai==1.58.1` | ⚠️ Instalar si necesitas |
| **Google (Gemini)** | ❌ Opcional | `google-generativeai==0.8.3` | ⚠️ Instalar si necesitas |

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` en el directorio `backend/`:

```bash
# Base de Datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/noticias_ia

# Seguridad
SECRET_KEY=tu-clave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# APIs de IA
ANTHROPIC_API_KEY=sk-ant-...        # REQUERIDO
OPENAI_API_KEY=sk-...               # Opcional
GOOGLE_API_KEY=...                  # Opcional

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Aplicación
VERSION=2.3.0
DEBUG=True
```

---

## 🎯 Iniciar Servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs

---

## 🔄 Actualizar Dependencias

Para actualizar todas las dependencias a las últimas versiones:

```bash
pip install --upgrade -r requirements.txt --break-system-packages
```

Para actualizar una dependencia específica:

```bash
pip install --upgrade fastapi --break-system-packages
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'X'"
**Solución**: Instala el paquete faltante
```bash
pip install nombre-del-paquete --break-system-packages
```

### Error: "ModuleNotFoundError: No module named 'openai'"
**Solución**: OpenAI es opcional. Si quieres usar GPT:
```bash
pip install openai --break-system-packages
```

### Error de permisos en Windows
**Solución**: Usa `--break-system-packages`
```bash
pip install -r requirements.txt --break-system-packages
```

### Error de PostgreSQL
**Solución**: Asegúrate de que PostgreSQL esté instalado y corriendo:
```bash
# Windows
net start postgresql-x64-12

# Linux
sudo systemctl start postgresql
```

---

## 📦 Generar nuevo requirements.txt

Si instalaste nuevos paquetes y quieres actualizar el archivo:

```bash
pip freeze > requirements.txt
```

---

## 🧹 Limpiar entorno

Para empezar desde cero:

```bash
# Desactivar entorno
deactivate

# Eliminar entorno
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Crear nuevo entorno
python -m venv venv
```

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Dependencias principales** | 15 |
| **Dependencias totales** | ~40 |
| **Dependencias opcionales** | 10+ |
| **Tamaño venv (aprox.)** | ~300 MB |

---

## 🔗 Enlaces Útiles

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Anthropic API](https://docs.anthropic.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [Google Gemini](https://ai.google.dev/)

---

**Última actualización**: 2025-10-17  
**Versión del proyecto**: 2.3.0-alpha
