# 🗄️ Configuración PostgreSQL

## ✅ Scripts Creados

1. **setup_database.sql** - Script SQL puro
2. **setup_windows.bat** - Script automatizado Windows

---

## 📋 Opción 1: Script Automatizado (Recomendado)

```bash
# Ejecutar como Administrador
cd D:\hromero\Desktop\projects\sistema-noticias-ia\backend\scripts
setup_windows.bat
```

El script:
- Verifica PostgreSQL instalado
- Crea base de datos `noticias_ia`
- Configura extensiones necesarias

---

## 📋 Opción 2: Manual

### 1️⃣ Verificar PostgreSQL instalado

```bash
psql --version
```

**Si no está instalado:**
- Descargar: https://www.postgresql.org/download/windows/
- Durante instalación, recordar password de usuario `postgres`

### 2️⃣ Crear base de datos

```bash
# Abrir Command Prompt
psql -U postgres

# Dentro de psql:
CREATE DATABASE noticias_ia;
\c noticias_ia
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
\q
```

### 3️⃣ Configurar .env

Editar `backend/.env`:
```
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/noticias_ia
```

---

## 🚀 Próximos Pasos

```bash
# 1. Instalar dependencias Python
cd backend
pip install -r requirements.txt

# 2. Ejecutar migraciones
alembic upgrade head

# 3. Cargar datos de ejemplo
python scripts/migrate_data.py

# 4. Iniciar servidor
uvicorn main:app --reload
```

---

## ⚠️ Troubleshooting

### Error: "psql no reconocido"
Agregar al PATH: `C:\Program Files\PostgreSQL\16\bin`

### Error: "password authentication failed"
Verificar password en pgAdmin o durante instalación

### Error: "database already exists"
OK, continuar con migraciones

---

## 🔍 Verificar Instalación

```bash
# Verificar conexión
psql -U postgres -d noticias_ia -c "SELECT version();"

# Ver tablas (después de migraciones)
psql -U postgres -d noticias_ia -c "\dt"
```
