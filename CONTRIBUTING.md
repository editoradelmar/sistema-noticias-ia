# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al **Sistema de Noticias con IA**! Esta guía te ayudará a empezar.

---

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Commits y Mensajes](#commits-y-mensajes)
- [Pull Requests](#pull-requests)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Features](#sugerir-features)

---

## 📜 Código de Conducta

### Nuestro Compromiso

Nos comprometemos a hacer de este proyecto un espacio inclusivo y acogedor para todos, independientemente de:
- Nivel de experiencia
- Identidad de género
- Orientación sexual
- Discapacidad
- Apariencia personal
- Raza o etnia
- Religión
- Nacionalidad

### Comportamiento Esperado

✅ **SÍ hacer:**
- Ser respetuoso y profesional
- Aceptar críticas constructivas
- Enfocarse en lo mejor para la comunidad
- Mostrar empatía hacia otros miembros

❌ **NO hacer:**
- Usar lenguaje o imágenes sexualizadas
- Hacer comentarios despectivos o ataques personales
- Acosar públicamente o privadamente
- Publicar información privada sin permiso

### Consecuencias

Comportamientos inaceptables pueden resultar en:
1. Advertencia
2. Suspensión temporal
3. Expulsión permanente

---


## � Buenas prácticas con Git/GitHub

- Usa ramas descriptivas para cada feature/fix (ej: feature/chat-ia, fix/bug-login)
- Haz commits claros y atómicos
- Sincroniza frecuentemente con el remoto
- Abre Pull Requests y sigue el formato sugerido
- Consulta el README y la guía rápida antes de contribuir

---

### 1. Reportar Bugs

¿Encontraste un error? ¡Ayúdanos a solucionarlo!

**Antes de reportar:**
- Busca en [issues existentes](https://github.com/usuario/proyecto/issues)
- Verifica que uses la última versión
- Intenta reproducir el error

**Al reportar incluye:**
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si es relevante
- Versión del sistema
- Logs de error

**Template:**
```markdown
## Descripción del Bug
[Descripción clara y concisa]

## Pasos para Reproducir
1. Ir a '...'
2. Click en '...'
3. Scroll hasta '...'
4. Ver error

## Comportamiento Esperado
[Qué debería pasar]

## Comportamiento Actual
[Qué pasa realmente]

## Screenshots
[Si aplica]

## Entorno
- OS: [ej. Windows 11]
- Browser: [ej. Chrome 120]
- Versión: [ej. 2.1.0]
```

### 2. Sugerir Features

¿Tienes una idea genial? ¡Compártela!

**Template:**
```markdown
## Feature Request

### Problema que Resuelve
[Describe el problema o necesidad]

### Solución Propuesta
[Describe tu solución ideal]

### Alternativas Consideradas
[Otras soluciones que consideraste]

### Contexto Adicional
[Screenshots, mockups, etc.]
```

### 3. Contribuir Código

¡La mejor forma de contribuir!

**Áreas donde necesitamos ayuda:**
- 🐛 Fix de bugs
- ✨ Nuevas features
- 📝 Documentación
- 🧪 Tests
- 🌐 Traducción i18n
- 🎨 Mejoras de UI/UX
- ⚡ Optimizaciones de performance

---

## 🔧 Proceso de Desarrollo

### Setup Inicial

```bash
# 1. Fork el proyecto
# Click en "Fork" en GitHub

# 2. Clonar tu fork
git clone https://github.com/TU_USERNAME/sistema-noticias-ia.git
cd sistema-noticias-ia

# 3. Agregar upstream
git remote add upstream https://github.com/usuario/sistema-noticias-ia.git

# 4. Verificar remotes
git remote -v
```

### Configurar Entorno

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus configuraciones
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Workflow de Desarrollo

```bash
# 1. Actualizar tu fork
git checkout main
git pull upstream main

# 2. Crear rama para tu feature
git checkout -b feature/nombre-descriptivo
# Ejemplos:
# - feature/add-password-recovery
# - fix/login-error-401
# - docs/update-readme

# 3. Hacer cambios
# ... editar código ...

# 4. Probar cambios
pytest  # Backend
npm test  # Frontend

# 5. Commit (ver sección de commits abajo)
git add .
git commit -m "feat: agregar recuperación de contraseña"

# 6. Push a tu fork
git push origin feature/nombre-descriptivo

# 7. Crear Pull Request en GitHub
```

---

## 📝 Estándares de Código

### Python (Backend)

**Style Guide:** PEP 8

```python
# ✅ CORRECTO
def crear_usuario(email: str, password: str) -> Usuario:
    """
    Crea un nuevo usuario en el sistema.
    
    Args:
        email: Email del usuario
        password: Contraseña en texto plano
        
    Returns:
        Usuario: Instancia del usuario creado
        
    Raises:
        ValueError: Si el email ya existe
    """
    if usuario_existe(email):
        raise ValueError("Email ya registrado")
    
    hashed_password = hash_password(password)
    return Usuario(email=email, password=hashed_password)


# ❌ INCORRECTO
def CreateUser(e,p):
    if check(e):
        raise Exception("Error")
    pwd=Hash(p)
    return User(e,pwd)
```

**Convenciones:**
- Type hints obligatorios
- Docstrings en funciones públicas
- snake_case para variables/funciones
- PascalCase para clases
- UPPER_CASE para constantes
- Imports ordenados (stdlib, third-party, local)

**Linting:**
```bash
# Formatear código
black .

# Linting
flake8 .
pylint *.py

# Type checking
mypy .
```

### JavaScript/React (Frontend)

**Style Guide:** Airbnb + Prettier

```javascript
// ✅ CORRECTO
const LoginForm = ({ onSubmit }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await onSubmit(email, password);
    } catch (error) {
      console.error('Error en login:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* ... */}
    </form>
  );
};

// ❌ INCORRECTO
function form(props){
  const [e,setE]=useState('')
  var p=''
  const submit=()=>{
    props.onSubmit(e,p)
  }
  return <form onSubmit={submit}></form>
}
```

**Convenciones:**
- PascalCase para componentes
- camelCase para funciones/variables
- UPPER_CASE para constantes
- Props destructuring
- Hooks en orden correcto

**Linting:**
```bash
# Formatear
npm run format

# Linting
npm run lint

# Type checking (si usas TypeScript)
npm run type-check
```

### SQL

```sql
-- ✅ CORRECTO
SELECT 
    u.id,
    u.email,
    u.nombre_completo,
    COUNT(n.id) as total_noticias
FROM usuarios u
LEFT JOIN noticias n ON u.id = n.usuario_id
WHERE u.is_active = true
GROUP BY u.id, u.email, u.nombre_completo
ORDER BY total_noticias DESC
LIMIT 10;

-- ❌ INCORRECTO
select * from usuarios u left join noticias n on u.id=n.usuario_id where u.is_active=true;
```

---

## 💬 Commits y Mensajes

Usamos [Conventional Commits](https://www.conventionalcommits.org/).

### Formato

```
<tipo>[scope opcional]: <descripción>

[cuerpo opcional]

[footer opcional]
```

### Tipos

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `feat` | Nueva feature | `feat: agregar recuperación de contraseña` |
| `fix` | Bug fix | `fix: corregir error 401 en login` |
| `docs` | Documentación | `docs: actualizar README con nuevas features` |
| `style` | Formato (no afecta código) | `style: formatear código con black` |
| `refactor` | Refactorización | `refactor: extraer lógica de auth a módulo` |
| `perf` | Mejora de performance | `perf: optimizar query de noticias` |
| `test` | Tests | `test: agregar tests para auth` |
| `chore` | Mantenimiento | `chore: actualizar dependencias` |

### Ejemplos

```bash
# Feature
git commit -m "feat(auth): agregar login con Google OAuth"

# Bug fix
git commit -m "fix(api): corregir error 500 en endpoint /noticias"

# Documentación
git commit -m "docs: agregar guía de deployment"

# Breaking change
git commit -m "feat(api)!: cambiar estructura de response de login

BREAKING CHANGE: el campo 'token' ahora se llama 'access_token'"
```

### Reglas

✅ **DO:**
- Usar presente ("add" no "added")
- Primera letra minúscula
- Sin punto al final
- Máximo 72 caracteres en primera línea
- Explicar QUÉ y POR QUÉ (no cómo)

❌ **DON'T:**
- "Fixed stuff"
- "Update files"
- "WIP"
- "asdfasdf"

---

## 🔄 Pull Requests

### Antes de Crear PR

**Checklist:**
- [ ] Código cumple estándares
- [ ] Tests pasan
- [ ] Documentación actualizada
- [ ] Sin console.log / print de debug
- [ ] Branch actualizado con main
- [ ] Commits limpios y descriptivos

### Template de PR

```markdown
## Descripción
[Describe tus cambios en detalle]

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva feature
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo se ha Probado?
[Describe las pruebas que realizaste]

## Checklist
- [ ] Mi código sigue el style guide del proyecto
- [ ] He hecho self-review de mi código
- [ ] He comentado mi código en áreas difíciles
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan warnings
- [ ] He agregado tests
- [ ] Tests nuevos y existentes pasan localmente
- [ ] Cambios dependientes han sido mergeados

## Screenshots (si aplica)
[Agregar screenshots]

## Issue Relacionado
Closes #123
```

### Proceso de Review

1. **Crear PR** con descripción clara
2. **CI/CD** corre automáticamente
3. **Reviewer** revisa código
4. **Cambios solicitados** (si hay)
5. **Aprobar** PR
6. **Merge** a main

### Tiempo de Review

- Features pequeñas: 1-2 días
- Features grandes: 3-5 días
- Bug fixes críticos: mismo día

---

## 🧪 Testing

### Backend Tests

```python
# test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_exitoso():
    response = client.post(
        "/api/auth/login",
        data={
            "username": "admin@sistema.com",
            "password": "admin123456"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_credenciales_incorrectas():
    response = client.post(
        "/api/auth/login",
        data={
            "username": "admin@sistema.com",
            "password": "wrong"
        }
    )
    assert response.status_code == 401
```

**Ejecutar:**
```bash
pytest
pytest -v
pytest --cov=. --cov-report=html
```

### Frontend Tests

```javascript
// Login.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Login from './Login';

test('muestra formulario de login', () => {
  render(<Login />);
  expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
});

test('valida email requerido', () => {
  render(<Login />);
  const submitButton = screen.getByText(/iniciar sesión/i);
  fireEvent.click(submitButton);
  expect(screen.getByText(/email es requerido/i)).toBeInTheDocument();
});
```

**Ejecutar:**
```bash
npm test
npm test -- --coverage
```

---

## 🎨 Style Guide Visual

### Componentes React

```jsx
// ✅ CORRECTO: Componente bien estructurado
import React, { useState } from 'react';
import PropTypes from 'prop-types';

const Button = ({ 
  label, 
  onClick, 
  variant = 'primary',
  disabled = false,
  loading = false 
}) => {
  const baseClasses = 'px-4 py-2 rounded-lg font-bold';
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300'
  };
  
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`${baseClasses} ${variantClasses[variant]}`}
    >
      {loading ? 'Cargando...' : label}
    </button>
  );
};

Button.propTypes = {
  label: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary']),
  disabled: PropTypes.bool,
  loading: PropTypes.bool
};

export default Button;
```

---

## 📚 Recursos

### Documentación
- [README.md](./README.md)
- [API_REFERENCE.md](./API_REFERENCE.md)
- [AUTH_GUIDE.md](./AUTH_GUIDE.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)

### Tutoriales
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [React Docs](https://react.dev)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com)

### Comunidad
- Discord: [Servidor](https://discord.gg/ejemplo)
- Discussions: [GitHub Discussions](https://github.com/usuario/proyecto/discussions)

---

## ❓ FAQ

**P: ¿Puedo trabajar en cualquier issue?**  
R: Sí, pero verifica que no esté asignado a alguien más. Comenta en el issue que quieres trabajar en él.

**P: ¿Cuánto tiempo toma aprobar un PR?**  
R: Usualmente 1-3 días hábiles. Bug fixes críticos se revisan el mismo día.

**P: ¿Necesito experiencia previa?**  
R: No! Todos fueron principiantes alguna vez. Hay issues marcados como `good first issue`.

**P: ¿Puedo proponer cambios grandes?**  
R: Sí, pero primero abre un issue para discutirlo con el equipo.

**P: ¿Qué pasa si mi PR es rechazado?**  
R: No te desanimes. Recibir feedback es parte del proceso. Aprenderás mucho.

---

## 🏆 Reconocimientos

Contribuidores destacados:
- [@usuario1](https://github.com/usuario1) - 50+ commits
- [@usuario2](https://github.com/usuario2) - Documentación
- [@usuario3](https://github.com/usuario3) - UI/UX

¡Tu nombre podría estar aquí! 🌟

---

## 📝 Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la misma [licencia MIT](./LICENSE) del proyecto.

---

## 💖 Agradecimientos

¡Gracias por hacer de este proyecto algo mejor! Cada contribución, sin importar cuán pequeña, es valiosa.

**¡Happy coding!** 🚀

---

**📅 Última actualización:** 2025-10-14  
**✍️ Mantenido por:** @hromero
