
# � Control de versiones y autenticación

Todos los cambios en la lógica de autenticación deben ser versionados con Git y documentados en el historial. Se recomienda abrir Pull Requests para cualquier ajuste en roles, seguridad o endpoints sensibles. Consulta la [Guía de Contribución](./CONTRIBUTING.md) antes de modificar el sistema de autenticación.

## 📋 Tabla de Contenidos

- [Introducción](#introducción)
- [Arquitectura de Autenticación](#arquitectura-de-autenticación)
- [Flujos de Autenticación](#flujos-de-autenticación)
- [Sistema de Roles](#sistema-de-roles)
- [Implementación Frontend](#implementación-frontend)
- [Implementación Backend](#implementación-backend)
- [Seguridad](#seguridad)
- [Ejemplos de Código](#ejemplos-de-código)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

Este sistema implementa autenticación **JWT (JSON Web Tokens)** con:
- ✅ Tokens stateless firmados con HS256
- ✅ Hashing de contraseñas con bcrypt (costo 12)
- ✅ Sistema de roles (RBAC)
- ✅ OAuth2 compatible
- ✅ Persistencia de sesión

---

## 🏗️ Arquitectura de Autenticación

```
┌─────────────────────────────────────────────┐
│           Usuario Frontend                   │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│       AuthContext (React)                    │
│  - Maneja estado de autenticación           │
│  - Guarda token en localStorage             │
│  - Provee funciones login/logout            │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│       API Service (api.js)                   │
│  - Agrega token a headers                   │
│  - Maneja errores 401/403                   │
└──────────────┬──────────────────────────────┘
               │ HTTP + JWT
               ▼
┌─────────────────────────────────────────────┐
│       Backend FastAPI                        │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │  OAuth2PasswordBearer               │    │
│  │  - Extrae token de header          │    │
│  └──────────┬─────────────────────────┘    │
│             ▼                                │
│  ┌────────────────────────────────────┐    │
│  │  get_current_user()                 │    │
│  │  - Decodifica JWT                   │    │
│  │  - Busca usuario en BD              │    │
│  └──────────┬─────────────────────────┘    │
│             ▼                                │
│  ┌────────────────────────────────────┐    │
│  │  Verificación de permisos           │    │
│  │  - Valida rol                       │    │
│  │  - Verifica is_active               │    │
│  └────────────────────────────────────┘    │
│                                              │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│       PostgreSQL                             │
│  - Tabla usuarios                           │
│  - Contraseñas hasheadas                    │
└─────────────────────────────────────────────┘
```

---

## 🔄 Flujos de Autenticación

### 1. Registro de Usuario

```
Usuario → Formulario de Registro
    ↓
POST /api/auth/register {
    email,
    username,
    password,
    nombre_completo (opcional)
}
    ↓
Backend valida:
    - Email único ✓
    - Username único ✓
    - Password ≥ 6 caracteres ✓
    ↓
Hashea password con bcrypt (costo 12)
    ↓
INSERT INTO usuarios (
    email, username, hashed_password,
    role='viewer', is_active=true
)
    ↓
Response 201: Usuario creado
    ↓
Auto-login (llama a login())
```

### 2. Login

```
Usuario → email + password
    ↓
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded
username=email&password=password
    ↓
Backend:
    1. SELECT * FROM usuarios WHERE email = ?
    2. bcrypt.verify(password, hashed_password)
    3. Verifica is_active = true
    4. UPDATE last_login = NOW()
    ↓
Genera JWT token:
    {
        "sub": user_id,
        "exp": now + 30 min,
        "role": user.role,
        "email": user.email
    }
    ↓
Firma con SECRET_KEY (HS256)
    ↓
Response 200: {
    access_token: "eyJhbGci...",
    token_type: "bearer",
    expires_in: 1800,
    user: {...}
}
    ↓
Frontend guarda en localStorage:
    - token
    - user data
```

### 3. Request Autenticado

```
Usuario → Acción (ej: crear noticia)
    ↓
Frontend lee token de localStorage
    ↓
POST /api/noticias/
Authorization: Bearer eyJhbGci...
Content-Type: application/json
{noticia data}
    ↓
Backend Middleware:
    1. Extrae token del header
    2. Decodifica JWT
    3. Verifica firma
    4. Verifica expiración
    5. Busca usuario en BD
    6. Verifica is_active
    ↓
Si válido: request.user = usuario
Si inválido: 401 Unauthorized
    ↓
Endpoint valida permisos:
    - Verifica rol
    - Verifica ownership (si aplica)
    ↓
Si autorizado: ejecuta acción
Si no: 403 Forbidden
```

### 4. Logout

```
Usuario → Click Logout
    ↓
Frontend:
    - Elimina token de localStorage
    - Elimina user data
    - Limpia estado de AuthContext
    ↓
Redirige a Login
    ↓
(Opcional) Backend: /api/auth/logout
    - Registra logout en logs
    - Invalida refresh token (si existe)
```

---

## 👥 Sistema de Roles

### Roles Disponibles

| Rol | Valor | Descripción |
|-----|-------|-------------|
| **Admin** | `admin` | Acceso total al sistema |
| **Editor** | `editor` | Puede crear y editar contenido |
| **Viewer** | `viewer` | Solo lectura |

### Matriz de Permisos

| Acción | Admin | Editor | Viewer |
|--------|-------|--------|--------|
| **Autenticación** |
| Registrarse | ✅ | ✅ | ✅ |
| Login | ✅ | ✅ | ✅ |
| Ver perfil | ✅ | ✅ | ✅ |
| Logout | ✅ | ✅ | ✅ |
| **Noticias** |
| Listar noticias | ✅ | ✅ | ✅ |
| Ver noticia | ✅ | ✅ | ✅ |
| Crear noticia | ✅ | ✅ | ❌ |
| Editar cualquier noticia | ✅ | ❌ | ❌ |
| Editar propia noticia | ✅ | ✅ | ❌ |
| Eliminar cualquier noticia | ✅ | ❌ | ❌ |
| Eliminar propia noticia | ✅ | ✅ | ❌ |
| **IA** |
| Generar resumen | ✅ | ✅ | ✅ |
| Chat con IA | ✅ | ✅ | ✅ |
| Analizar noticia | ✅ | ✅ | ✅ |

### Lógica de Permisos

#### Crear Noticia
```python
# Requiere: admin O editor
if user.role not in ['admin', 'editor']:
    raise HTTPException(403, "Sin permisos")
```

#### Editar Noticia
```python
# Admin: puede todo
# Editor: solo sus propias noticias
if user.role == 'admin':
    return True
if user.role == 'editor' and noticia.usuario_id == user.id:
    return True
raise HTTPException(403, "Sin permisos")
```

#### Eliminar Noticia
```python
# Mismo que editar
if user.role == 'admin':
    return True
if user.role == 'editor' and noticia.usuario_id == user.id:
    return True
raise HTTPException(403, "Sin permisos")
```

---

## ⚛️ Implementación Frontend

### AuthContext

```jsx
// context/AuthContext.jsx
import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Cargar del localStorage al iniciar
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString(),
    });

    const data = await response.json();
    
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

### Protección de Rutas

```jsx
// App.jsx
import { useAuth } from './context/AuthContext';
import Login from './components/Login';

export default function App() {
  const { user, loading } = useAuth();
  
  if (loading) return <div>Cargando...</div>;
  
  if (!user) return <Login />;
  
  return <MainApp />;
}
```

### API Service con Tokens

```javascript
// services/api.js
const getHeaders = (token = null) => {
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

export const api = {
  crearNoticia: async (data, token) => {
    const res = await fetch('http://localhost:8000/api/noticias/', {
      method: 'POST',
      headers: getHeaders(token),
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail);
    }
    
    return res.json();
  }
};
```

---

## 🐍 Implementación Backend

### Configuración JWT

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "clave-super-secreta-cambiar-en-produccion"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Funciones de Seguridad

```python
# utils/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
```

### Dependencias de Autenticación

```python
# routers/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Token inválido")
    except JWTError:
        raise HTTPException(401, "Token inválido")
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise HTTPException(401, "Usuario no encontrado")
    
    return user

async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(400, "Usuario inactivo")
    return current_user
```

### Endpoint de Login

```python
# routers/auth.py
@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Buscar usuario por email
    user = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    # Actualizar last_login
    user.last_login = datetime.now()
    db.commit()
    
    # Crear token
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800,
        "user": user.to_dict()
    }
```

### Proteger Endpoints

```python
# routers/noticias.py
@router.post("/", response_model=Noticia)
async def crear_noticia(
    noticia: NoticiaCreate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verificar permisos
    if current_user.role not in ['admin', 'editor']:
        raise HTTPException(403, "Sin permisos para crear noticias")
    
    # Crear noticia vinculada al usuario
    nueva_noticia = Noticia(
        **noticia.dict(),
        usuario_id=current_user.id
    )
    db.add(nueva_noticia)
    db.commit()
    
    return nueva_noticia
```

---

## 🔒 Seguridad

### Mejores Prácticas Implementadas

✅ **Contraseñas:**
- Hasheadas con bcrypt (costo 12)
- Nunca se almacenan en texto plano
- Mínimo 6 caracteres

✅ **JWT Tokens:**
- Firmados con HS256
- Expiración de 30 minutos
- SECRET_KEY de 64 caracteres hex

✅ **Base de Datos:**
- Emails únicos
- Usernames únicos
- Prepared statements (SQLAlchemy ORM)

✅ **API:**
- CORS configurado
- Validación Pydantic
- Error handling robusto

### Recomendaciones para Producción

🔐 **HTTPS Obligatorio:**
```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

🔑 **Rotar SECRET_KEY:**
```bash
# Generar nueva clave
openssl rand -hex 32

# Actualizar .env
SECRET_KEY=nueva_clave_aqui
```

⏱️ **Rate Limiting:**
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(...):
    ...
```

📝 **Logging de Seguridad:**
```python
import logging

logger = logging.getLogger(__name__)

# En cada login
logger.info(f"Login exitoso: {user.email} desde {request.client.host}")

# En cada fallo
logger.warning(f"Login fallido: {form_data.username} desde {request.client.host}")
```

🔄 **Refresh Tokens (próximamente):**
```python
# Token de acceso: 30 minutos
# Refresh token: 7 días
# Renovar sin re-autenticar
```

---

## 💻 Ejemplos de Código

### Ejemplo 1: Login Completo

**Frontend:**
```jsx
const handleLogin = async (e) => {
  e.preventDefault();
  
  try {
    const result = await login(email, password);
    
    if (result.success) {
      console.log('Login exitoso!');
      // AuthContext maneja la redirección
    } else {
      setError(result.error);
    }
  } catch (err) {
    setError('Error de conexión');
  }
};
```

**Backend:**
```python
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Credenciales incorrectas")
    
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}
```

### Ejemplo 2: Crear Noticia Autenticada

**Frontend:**
```jsx
const crearNoticia = async (data) => {
  const { token } = useAuth();
  
  const response = await fetch('/api/noticias/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
};
```

**Backend:**
```python
@router.post("/")
async def crear_noticia(
    noticia: NoticiaCreate,
    user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if user.role not in ['admin', 'editor']:
        raise HTTPException(403)
    
    nueva = Noticia(**noticia.dict(), usuario_id=user.id)
    db.add(nueva)
    db.commit()
    return nueva
```

### Ejemplo 3: Verificar Permisos

```python
def verificar_permiso_noticia(noticia: Noticia, user: Usuario) -> bool:
    """
    Verifica si el usuario puede editar/eliminar la noticia
    """
    if user.role == 'admin':
        return True
    
    if user.role == 'editor' and noticia.usuario_id == user.id:
        return True
    
    return False

@router.delete("/{id}")
async def eliminar(
    id: int,
    user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    noticia = db.query(Noticia).filter(Noticia.id == id).first()
    
    if not verificar_permiso_noticia(noticia, user):
        raise HTTPException(403, "Sin permisos")
    
    db.delete(noticia)
    db.commit()
    return {"success": True}
```

---

## 🐛 Troubleshooting

### Error 401: Unauthorized

**Causa:** Token inválido o expirado

**Solución:**
```javascript
// Frontend: renovar sesión
if (error.status === 401) {
  logout();
  navigate('/login');
}
```

### Error 403: Forbidden

**Causa:** Usuario sin permisos

**Solución:**
```python
# Backend: verificar roles
if user.role not in ['admin', 'editor']:
    raise HTTPException(403, "Rol insuficiente")
```

### Token No Se Envía

**Causa:** Header mal formado

**Solución:**
```javascript
// Correcto:
headers: {
  'Authorization': 'Bearer eyJhbGci...'
}

// Incorrecto:
headers: {
  'Authorization': 'eyJhbGci...'  // Falta "Bearer "
}
```

### Password Hash Inválido

**Causa:** Versión incorrecta de bcrypt

**Solución:**
```bash
pip uninstall bcrypt passlib
pip install bcrypt==4.0.1 passlib==1.7.4
```

### CORS Error

**Causa:** Origin no permitido

**Solución:**
```python
# config.py
ALLOWED_ORIGINS = "http://localhost:5173,http://localhost:3000"
```

---

## 📚 Referencias

- [JWT.io](https://jwt.io/) - Debugger de JWT
- [OAuth2 RFC](https://tools.ietf.org/html/rfc6749) - Especificación
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) - Docs oficiales
- [Passlib](https://passlib.readthedocs.io/) - Hashing de passwords

---

**🔐 Documento actualizado:** 2025-10-14  
**📌 Versión:** 2.1.0
