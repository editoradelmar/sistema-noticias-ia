"""
Utilidades de seguridad
Manejo de contraseñas y JWT tokens
"""
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = settings.SECRET_KEY if hasattr(settings, 'SECRET_KEY') else "tu-clave-secreta-super-segura-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar si la contraseña coincide con el hash
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada
        
    Returns:
        bool: True si coinciden, False si no
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashear una contraseña
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Contraseña hasheada
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crear un token JWT
    
    Args:
        data: Datos a incluir en el token (típicamente user_id, email, role)
        expires_delta: Tiempo de expiración personalizado
        
    Returns:
        str: Token JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodificar y verificar un token JWT
    
    Args:
        token: Token JWT a verificar
        
    Returns:
        dict: Datos del token si es válido, None si no
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def create_token_response(user_id: int, email: str, username: str, role: str, is_active: bool, is_superuser: bool, created_at: Any, last_login: Any = None, nombre_completo: str = None) -> dict:
    """
    Crear respuesta con token y datos del usuario
    
    Args:
        user_id: ID del usuario
        email: Email del usuario
        username: Username del usuario
        role: Rol del usuario
        is_active: Si el usuario está activo
        is_superuser: Si es superusuario
        created_at: Fecha de creación
        last_login: Último login
        nombre_completo: Nombre completo
        
    Returns:
        dict: Respuesta formateada con token y user data
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={
            "sub": str(user_id),
            "email": email,
            "username": username,
            "role": role
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # segundos
        "user": {
            "id": user_id,
            "email": email,
            "username": username,
            "nombre_completo": nombre_completo,
            "role": role,
            "is_active": is_active,
            "is_superuser": is_superuser,
            "created_at": created_at,
            "last_login": last_login
        }
    }
