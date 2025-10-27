"""
Router de Autenticación
Endpoints: register, login, me, refresh
"""
from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional

from core.database import get_db
from models import orm_models
from models.schemas import (
    UsuarioCreate,
    Usuario,
    LoginRequest,
    TokenResponse,
    ResponseModel,
    RoleEnum
)
from utils.security import (
    verify_password,
    get_password_hash,
    create_token_response,
    decode_access_token
)

router = APIRouter()

# OAuth2 scheme para obtener el token del header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ==================== DEPENDENCIAS ====================

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


async def require_role(
    required_roles: list[str],
    current_user: orm_models.Usuario = Depends(get_current_user)
) -> orm_models.Usuario:
    """
    Verificar que el usuario tenga uno de los roles requeridos
    """
    if current_user.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requiere uno de estos roles: {', '.join(required_roles)}"
        )
    return current_user


async def require_admin(
    current_user: orm_models.Usuario = Depends(get_current_user)
) -> orm_models.Usuario:
    """
    Verificar que el usuario sea administrador del sistema
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere permisos de administrador del sistema"
        )
    return current_user


async def require_director_or_above(
    current_user: orm_models.Usuario = Depends(get_current_user)
) -> orm_models.Usuario:
    """
    Verificar que el usuario sea director de redacción o superior
    """
    if current_user.role not in ['admin', 'director']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere permisos de director de redacción o superior"
        )
    return current_user


# ==================== ENDPOINTS ====================

@router.post("/register", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo usuario
    
    - **email**: Email único del usuario
    - **username**: Nombre de usuario único
    - **password**: Contraseña (mínimo 6 caracteres)
    - **nombre_completo**: Nombre completo (opcional)
    - **role**: Rol del usuario (default: viewer)
    """
    # Verificar si el email ya existe
    existing_email = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.email == user_data.email.lower()
    ).first()
    
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el username ya existe
    existing_username = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.username == user_data.username.lower()
    ).first()
    
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user_data.password)
    
    new_user = orm_models.Usuario(
        email=user_data.email.lower(),
        username=user_data.username.lower(),
        hashed_password=hashed_password,
        nombre_completo=user_data.nombre_completo,
        role=user_data.role.value,
        is_active=True,
        is_superuser=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión y obtener token JWT
    
    Acepta OAuth2 form data para compatibilidad con Swagger UI.
    El campo 'username' debe contener el email del usuario.
    
    - **username**: Email del usuario (sí, aunque diga username, usa el email)
    - **password**: Contraseña
    
    Returns:
        Token JWT con información del usuario
    """
    # Buscar usuario por email (form_data.username contiene el email)
    user = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.email == form_data.username.lower()
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar contraseña
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Actualizar último login
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    # Crear y retornar token
    token_response = create_token_response(
        user_id=user.id,
        email=user.email,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        last_login=user.last_login,
        nombre_completo=user.nombre_completo
    )
    
    return token_response


@router.get("/me", response_model=Usuario)
async def get_me(
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Obtener información del usuario actual
    
    Requiere autenticación con token JWT
    """
    return current_user


@router.post("/login/json", response_model=TokenResponse)
async def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión con JSON (alternativa al OAuth2 form)
    
    - **email**: Email del usuario
    - **password**: Contraseña
    
    Returns:
        Token JWT con información del usuario
    """
    # Buscar usuario por email
    user = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.email == login_data.email.lower()
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar contraseña
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Actualizar último login
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    # Crear y retornar token
    token_response = create_token_response(
        user_id=user.id,
        email=user.email,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        last_login=user.last_login,
        nombre_completo=user.nombre_completo
    )
    
    return token_response


@router.post("/logout", response_model=ResponseModel)
async def logout(
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Cerrar sesión (invalidar token)
    
    Nota: En JWT stateless, el token expira automáticamente.
    Este endpoint es más para consistencia en el frontend.
    """
    return ResponseModel(
        success=True,
        message="Sesión cerrada correctamente"
    )


@router.get("/users", response_model=list[Usuario])
async def get_users(
    activos_solo: bool = True,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Obtener lista de usuarios
    
    Accesible para todos los usuarios autenticados (para dropdowns de autor)
    
    Args:
        activos_solo: Si True, solo retorna usuarios activos (default: True)
        
    Returns:
        Lista de usuarios ordenada por nombre_completo
    """
    query = db.query(orm_models.Usuario)
    
    if activos_solo:
        query = query.filter(orm_models.Usuario.is_active == True)
    
    users = query.order_by(orm_models.Usuario.nombre_completo).all()
    
    return users


@router.post("/create-admin", response_model=Usuario)
async def create_admin(
    admin_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Crear usuario administrador
    
    ⚠️ SOLO PARA DESARROLLO - En producción esto debe estar protegido
    """
    # Verificar si ya existe un admin
    admin_exists = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.role == 'admin'
    ).first()
    
    if admin_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario administrador. Usa /register para usuarios normales."
        )
    
    # Verificar email/username únicos
    existing = db.query(orm_models.Usuario).filter(
        (orm_models.Usuario.email == admin_data.email.lower()) |
        (orm_models.Usuario.username == admin_data.username.lower())
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email o username ya existe"
        )
    
    # Crear admin
    hashed_password = get_password_hash(admin_data.password)
    
    admin_user = orm_models.Usuario(
        email=admin_data.email.lower(),
        username=admin_data.username.lower(),
        hashed_password=hashed_password,
        nombre_completo=admin_data.nombre_completo,
        role='admin',
        is_active=True,
        is_superuser=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    return admin_user


# ==================== GESTIÓN AVANZADA DE USUARIOS ====================

@router.put("/users/{user_id}", response_model=Usuario)
async def update_user(
    user_id: int,
    user_data: dict,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_user)
):
    """
    Actualizar usuario por ID
    Solo administradores pueden actualizar otros usuarios
    """
    # Verificar permisos - solo admin puede editar otros usuarios
    if current_user.role != 'admin' and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar este usuario"
        )
    
    # Buscar usuario a actualizar
    user = db.query(orm_models.Usuario).filter(orm_models.Usuario.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar campos permitidos
    if 'email' in user_data and user_data['email']:
        # Verificar email único
        existing = db.query(orm_models.Usuario).filter(
            orm_models.Usuario.email == user_data['email'].lower(),
            orm_models.Usuario.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso"
            )
        user.email = user_data['email'].lower()
    
    if 'username' in user_data and user_data['username']:
        # Verificar username único
        existing = db.query(orm_models.Usuario).filter(
            orm_models.Usuario.username == user_data['username'].lower(),
            orm_models.Usuario.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está en uso"
            )
        user.username = user_data['username'].lower()
    
    if 'nombre_completo' in user_data:
        user.nombre_completo = user_data['nombre_completo']
    
    if 'password' in user_data and user_data['password']:
        user.hashed_password = get_password_hash(user_data['password'])
    
    # Solo admin puede cambiar roles y campos administrativos
    if current_user.role == 'admin':
        if 'role' in user_data:
            user.role = user_data['role']
        
        if 'supervisor_id' in user_data:
            if user_data['supervisor_id']:
                # Verificar que el supervisor existe
                supervisor = db.query(orm_models.Usuario).filter(
                    orm_models.Usuario.id == user_data['supervisor_id']
                ).first()
                if not supervisor:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Supervisor especificado no existe"
                    )
            user.supervisor_id = user_data['supervisor_id']
        
        if 'secciones_asignadas' in user_data:
            user.secciones_asignadas = user_data['secciones_asignadas']
        
        if 'limite_tokens_diario' in user_data:
            user.limite_tokens_diario = user_data['limite_tokens_diario']
        
        if 'fecha_expiracion_acceso' in user_data:
            if user_data['fecha_expiracion_acceso']:
                try:
                    # Parsear como fecha (no datetime) ya que el campo DB es Date
                    fecha_str = user_data['fecha_expiracion_acceso']
                    if 'T' in fecha_str:
                        # Si viene con tiempo, extraer solo la fecha
                        fecha_str = fecha_str.split('T')[0]
                    user.fecha_expiracion_acceso = date.fromisoformat(fecha_str)
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Formato de fecha inválido. Use YYYY-MM-DD"
                    )
            else:
                user.fecha_expiracion_acceso = None
        
        if 'is_active' in user_data:
            user.is_active = user_data['is_active']
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error actualizando usuario"
        )


@router.delete("/users/{user_id}", response_model=ResponseModel)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_user)
):
    """
    Eliminar usuario por ID
    Solo administradores pueden eliminar usuarios
    """
    # Solo admin puede eliminar usuarios
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar usuarios"
        )
    
    # No permitir auto-eliminación
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    # Buscar usuario
    user = db.query(orm_models.Usuario).filter(orm_models.Usuario.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    try:
        db.delete(user)
        db.commit()
        return ResponseModel(
            success=True,
            message=f"Usuario {user.username} eliminado correctamente"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error eliminando usuario"
        )
