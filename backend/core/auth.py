"""
Módulo de autenticación y autorización
Exporta funciones de dependencias para proteger endpoints
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.database import get_db
from models import orm_models
from utils.security import decode_access_token

# OAuth2 scheme para obtener el token del header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> orm_models.Usuario:
    """
    Obtener usuario actual desde el token JWT
    
    Args:
        token: Token JWT del header Authorization
        db: Sesión de base de datos
        
    Returns:
        Usuario: Usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodificar token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Buscar usuario en BD
    user = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.id == int(user_id)
    ).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user


async def get_current_active_user(
    current_user: orm_models.Usuario = Depends(get_current_user)
) -> orm_models.Usuario:
    """
    Verificar que el usuario esté activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


async def get_current_admin(
    current_user: orm_models.Usuario = Depends(get_current_user)
) -> orm_models.Usuario:
    """
    Verificar que el usuario sea administrador
    
    Args:
        current_user: Usuario autenticado
        
    Returns:
        Usuario: Usuario admin
        
    Raises:
        HTTPException: Si el usuario no es admin
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user


async def get_current_editor(
    current_user: orm_models.Usuario = Depends(get_current_user)
) -> orm_models.Usuario:
    """
    Verificar que el usuario sea admin o editor
    
    Args:
        current_user: Usuario autenticado
        
    Returns:
        Usuario: Usuario con permisos de edición
        
    Raises:
        HTTPException: Si el usuario no tiene permisos
    """
    if current_user.role not in ['admin', 'editor']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de editor o administrador"
        )
    return current_user


async def require_role(
    required_roles: list[str],
    current_user: orm_models.Usuario = Depends(get_current_user)
) -> orm_models.Usuario:
    """
    Verificar que el usuario tenga uno de los roles requeridos
    
    Args:
        required_roles: Lista de roles permitidos
        current_user: Usuario autenticado
        
    Returns:
        Usuario: Usuario con rol permitido
        
    Raises:
        HTTPException: Si el usuario no tiene ninguno de los roles
    """
    if current_user.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requiere uno de estos roles: {', '.join(required_roles)}"
        )
    return current_user
