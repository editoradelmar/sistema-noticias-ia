"""
Router de Administración de Usuarios
Endpoints para gestión avanzada de usuarios con jerarquía editorial
Solo accesible para usuarios con permisos administrativos
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, date

from core.database import get_db
from models import orm_models
from models.schemas import (
    UsuarioCreate, 
    UsuarioUpdate, 
    Usuario, 
    UsuarioExtendido,
    ResponseModel
)
from routers.auth import get_current_user

router = APIRouter()

# ==================== DEPENDENCIAS ====================

async def require_admin_or_director(
    current_user: orm_models.Usuario = Depends(get_current_user)
) -> orm_models.Usuario:
    """
    Verificar que el usuario sea admin o director de redacción
    """
    if current_user.role not in ['admin', 'director']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere permisos de administrador o director de redacción"
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

def can_manage_user(manager: orm_models.Usuario, target_user: orm_models.Usuario) -> bool:
    """
    Verificar si un usuario puede gestionar a otro según jerarquía
    """
    # Admin puede gestionar a todos
    if manager.role == 'admin':
        return True
    
    # Director puede gestionar a todos excepto admin
    if manager.role == 'director' and target_user.role != 'admin':
        return True
    
    # Jefe de sección puede gestionar a sus subordinados directos
    if manager.role == 'jefe_seccion':
        return target_user.supervisor_id == manager.id
    
    # Otros roles no pueden gestionar usuarios
    return False

# ==================== ENDPOINTS ====================

@router.get("/admin/usuarios", response_model=List[UsuarioExtendido])
async def get_usuarios_admin(
    activos_solo: bool = Query(True, description="Solo usuarios activos"),
    role_filter: Optional[str] = Query(None, description="Filtrar por role"),
    seccion_id: Optional[int] = Query(None, description="Filtrar por sección asignada"),
    supervisor_id: Optional[int] = Query(None, description="Filtrar por supervisor"),
    search: Optional[str] = Query(None, description="Buscar en nombre o email"),
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(require_admin_or_director)
):
    """
    Obtener lista de usuarios con información extendida para administración
    
    Incluye:
    - Información básica del usuario
    - Datos de jerarquía (supervisor, subordinados)
    - Métricas básicas (cantidad de noticias)
    - Nombres de secciones asignadas
    
    Filtros disponibles por parámetros de query
    """
    # Construir query base con joins optimizados
    query = db.query(orm_models.Usuario).options(
        joinedload(orm_models.Usuario.supervisor),
        joinedload(orm_models.Usuario.subordinados)
    )
    
    # Filtros según permisos del usuario actual
    if current_user.role == 'director':
        # Director no ve admins del sistema
        query = query.filter(orm_models.Usuario.role != 'admin')
    elif current_user.role == 'jefe_seccion':
        # Jefe de sección solo ve su equipo
        query = query.filter(
            or_(
                orm_models.Usuario.supervisor_id == current_user.id,
                orm_models.Usuario.id == current_user.id
            )
        )
    
    # Aplicar filtros de query params
    if activos_solo:
        query = query.filter(orm_models.Usuario.is_active == True)
    
    if role_filter:
        query = query.filter(orm_models.Usuario.role == role_filter)
    
    if supervisor_id:
        query = query.filter(orm_models.Usuario.supervisor_id == supervisor_id)
    
    if seccion_id:
        query = query.filter(
            orm_models.Usuario.secciones_asignadas.contains([seccion_id])
        )
    
    if search:
        search_filter = f"%{search.lower()}%"
        query = query.filter(
            or_(
                func.lower(orm_models.Usuario.nombre_completo).contains(search_filter),
                func.lower(orm_models.Usuario.email).contains(search_filter),
                func.lower(orm_models.Usuario.username).contains(search_filter)
            )
        )
    
    # Ordenar por jerarquía y nombre
    usuarios = query.order_by(
        orm_models.Usuario.role,
        orm_models.Usuario.nombre_completo
    ).all()
    
    # Construir respuesta extendida
    result = []
    for usuario in usuarios:
        # Obtener conteo de noticias
        noticias_count = db.query(func.count(orm_models.Noticia.id)).filter(
            orm_models.Noticia.usuario_id == usuario.id
        ).scalar() or 0
        
        # Obtener nombres de secciones
        secciones_nombres = []
        if usuario.secciones_asignadas:
            secciones = db.query(orm_models.Seccion).filter(
                orm_models.Seccion.id.in_(usuario.secciones_asignadas)
            ).all()
            secciones_nombres = [s.nombre for s in secciones]
        
        # Construir objeto extendido
        usuario_ext = UsuarioExtendido(
            id=usuario.id,
            email=usuario.email,
            username=usuario.username,
            nombre_completo=usuario.nombre_completo,
            role=usuario.role,
            is_active=usuario.is_active,
            is_superuser=usuario.is_superuser,
            supervisor_id=usuario.supervisor_id,
            secciones_asignadas=usuario.secciones_asignadas or [],
            limite_tokens_diario=usuario.limite_tokens_diario,
            fecha_expiracion_acceso=usuario.fecha_expiracion_acceso.isoformat() if usuario.fecha_expiracion_acceso else None,
            created_at=usuario.created_at,
            last_login=usuario.last_login,
            supervisor_nombre=usuario.supervisor.nombre_completo if usuario.supervisor else None,
            subordinados_count=len(usuario.subordinados),
            noticias_count=noticias_count,
            secciones_nombres=secciones_nombres,
            puede_supervisar=usuario.puede_supervisar,
            nivel_jerarquico=usuario.nivel_jerarquico
        )
        
        result.append(usuario_ext)
    
    return result


@router.get("/admin/usuarios/{user_id}", response_model=UsuarioExtendido)
async def get_usuario_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(require_admin_or_director)
):
    """
    Obtener información detallada de un usuario específico
    """
    usuario = db.query(orm_models.Usuario).options(
        joinedload(orm_models.Usuario.supervisor),
        joinedload(orm_models.Usuario.subordinados)
    ).filter(orm_models.Usuario.id == user_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar permisos para ver este usuario
    if not can_manage_user(current_user, usuario):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver este usuario"
        )
    
    # Construir respuesta (similar al endpoint de lista)
    noticias_count = db.query(func.count(orm_models.Noticia.id)).filter(
        orm_models.Noticia.usuario_id == usuario.id
    ).scalar() or 0
    
    secciones_nombres = []
    if usuario.secciones_asignadas:
        secciones = db.query(orm_models.Seccion).filter(
            orm_models.Seccion.id.in_(usuario.secciones_asignadas)
        ).all()
        secciones_nombres = [s.nombre for s in secciones]
    
    return UsuarioExtendido(
        id=usuario.id,
        email=usuario.email,
        username=usuario.username,
        nombre_completo=usuario.nombre_completo,
        role=usuario.role,
        is_active=usuario.is_active,
        is_superuser=usuario.is_superuser,
        supervisor_id=usuario.supervisor_id,
        secciones_asignadas=usuario.secciones_asignadas or [],
        limite_tokens_diario=usuario.limite_tokens_diario,
        fecha_expiracion_acceso=usuario.fecha_expiracion_acceso.isoformat() if usuario.fecha_expiracion_acceso else None,
        created_at=usuario.created_at,
        last_login=usuario.last_login,
        supervisor_nombre=usuario.supervisor.nombre_completo if usuario.supervisor else None,
        subordinados_count=len(usuario.subordinados),
        noticias_count=noticias_count,
        secciones_nombres=secciones_nombres,
        puede_supervisar=usuario.puede_supervisar,
        nivel_jerarquico=usuario.nivel_jerarquico
    )


@router.post("/admin/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def crear_usuario_admin(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(require_admin_or_director)
):
    """
    Crear nuevo usuario con configuración completa de jerarquía
    
    Solo admin puede crear otros admins o directores
    Director puede crear jefes de sección, redactores y viewers
    """
    from utils.security import get_password_hash
    
    # Validar permisos para crear usuario con el rol especificado
    if usuario_data.role == 'admin' and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden crear otros administradores"
        )
    
    if usuario_data.role == 'director' and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden crear directores de redacción"
        )
    
    # Verificar si email/username ya existen
    existing = db.query(orm_models.Usuario).filter(
        or_(
            orm_models.Usuario.email == usuario_data.email.lower(),
            orm_models.Usuario.username == usuario_data.username.lower()
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email o username ya existe"
        )
    
    # Validar supervisor si se especifica
    supervisor = None
    if usuario_data.supervisor_id:
        supervisor = db.query(orm_models.Usuario).filter(
            orm_models.Usuario.id == usuario_data.supervisor_id
        ).first()
        
        if not supervisor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Supervisor especificado no existe"
            )
        
        if not supervisor.puede_supervisar:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario especificado no puede ser supervisor"
            )
    
    # Validar secciones asignadas
    if usuario_data.secciones_asignadas:
        secciones_validas = db.query(orm_models.Seccion).filter(
            orm_models.Seccion.id.in_(usuario_data.secciones_asignadas)
        ).count()
        
        if secciones_validas != len(usuario_data.secciones_asignadas):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Una o más secciones especificadas no existen"
            )
    
    # Procesar fecha de expiración
    fecha_expiracion = None
    if usuario_data.fecha_expiracion_acceso:
        try:
            fecha_expiracion = datetime.strptime(
                usuario_data.fecha_expiracion_acceso, "%Y-%m-%d"
            ).date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de fecha inválido. Use YYYY-MM-DD"
            )
    
    # Crear usuario
    hashed_password = get_password_hash(usuario_data.password)
    
    nuevo_usuario = orm_models.Usuario(
        email=usuario_data.email.lower(),
        username=usuario_data.username.lower(),
        hashed_password=hashed_password,
        nombre_completo=usuario_data.nombre_completo,
        role=usuario_data.role.value,
        supervisor_id=usuario_data.supervisor_id,
        secciones_asignadas=usuario_data.secciones_asignadas or [],
        limite_tokens_diario=usuario_data.limite_tokens_diario,
        fecha_expiracion_acceso=fecha_expiracion,
        is_active=True,
        is_superuser=(usuario_data.role == 'admin')
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario


@router.put("/admin/usuarios/{user_id}", response_model=Usuario)
async def actualizar_usuario_admin(
    user_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(require_admin_or_director)
):
    """
    Actualizar usuario existente con validación de jerarquía
    """
    from utils.security import get_password_hash
    
    # Buscar usuario a actualizar
    usuario = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.id == user_id
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar permisos para modificar este usuario
    if not can_manage_user(current_user, usuario):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para modificar este usuario"
        )
    
    # Validaciones específicas de campos
    if usuario_data.role:
        # Solo admin puede cambiar roles a admin o director
        if usuario_data.role in ['admin', 'director'] and current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden asignar roles de admin o director"
            )
        
        # No se puede degradar al último admin
        if usuario.role == 'admin' and usuario_data.role != 'admin':
            admin_count = db.query(func.count(orm_models.Usuario.id)).filter(
                orm_models.Usuario.role == 'admin',
                orm_models.Usuario.is_active == True,
                orm_models.Usuario.id != user_id
            ).scalar()
            
            if admin_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede cambiar el rol del último administrador activo"
                )
    
    # Validar email/username únicos si se cambian
    if usuario_data.email and usuario_data.email != usuario.email:
        email_exists = db.query(orm_models.Usuario).filter(
            orm_models.Usuario.email == usuario_data.email.lower(),
            orm_models.Usuario.id != user_id
        ).first()
        
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso"
            )
    
    if usuario_data.username and usuario_data.username != usuario.username:
        username_exists = db.query(orm_models.Usuario).filter(
            orm_models.Usuario.username == usuario_data.username.lower(),
            orm_models.Usuario.id != user_id
        ).first()
        
        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está en uso"
            )
    
    # Validar supervisor
    if usuario_data.supervisor_id is not None:
        if usuario_data.supervisor_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un usuario no puede ser supervisor de sí mismo"
            )
        
        if usuario_data.supervisor_id > 0:
            supervisor = db.query(orm_models.Usuario).filter(
                orm_models.Usuario.id == usuario_data.supervisor_id
            ).first()
            
            if not supervisor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Supervisor especificado no existe"
                )
    
    # Validar secciones
    if usuario_data.secciones_asignadas is not None:
        if usuario_data.secciones_asignadas:
            secciones_validas = db.query(orm_models.Seccion).filter(
                orm_models.Seccion.id.in_(usuario_data.secciones_asignadas)
            ).count()
            
            if secciones_validas != len(usuario_data.secciones_asignadas):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Una o más secciones especificadas no existen"
                )
    
    # Aplicar cambios
    update_data = usuario_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == 'password' and value:
            # Hash de nueva contraseña
            setattr(usuario, 'hashed_password', get_password_hash(value))
        elif field == 'fecha_expiracion_acceso' and value:
            # Procesar fecha
            try:
                fecha_exp = datetime.strptime(value, "%Y-%m-%d").date()
                setattr(usuario, field, fecha_exp)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Formato de fecha inválido. Use YYYY-MM-DD"
                )
        elif field == 'role' and value:
            # Actualizar role y is_superuser
            setattr(usuario, 'role', value.value)
            setattr(usuario, 'is_superuser', (value.value == 'admin'))
        elif field != 'password':  # Evitar setear password directamente
            setattr(usuario, field, value)
    
    db.commit()
    db.refresh(usuario)
    
    return usuario


@router.delete("/admin/usuarios/{user_id}", response_model=ResponseModel)
async def eliminar_usuario_admin(
    user_id: int,
    forzar: bool = Query(False, description="Forzar eliminación aunque tenga noticias"),
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(require_admin)
):
    """
    Eliminar usuario (solo admin)
    
    Por defecto solo desactiva el usuario. 
    Con forzar=true elimina físicamente (cuidado con integridad referencial)
    """
    usuario = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.id == user_id
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir eliminación del último admin
    if usuario.role == 'admin':
        admin_count = db.query(func.count(orm_models.Usuario.id)).filter(
            orm_models.Usuario.role == 'admin',
            orm_models.Usuario.is_active == True,
            orm_models.Usuario.id != user_id
        ).scalar()
        
        if admin_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar al último administrador activo"
            )
    
    # Verificar si tiene noticias asociadas
    noticias_count = db.query(func.count(orm_models.Noticia.id)).filter(
        orm_models.Noticia.usuario_id == user_id
    ).scalar()
    
    if noticias_count > 0 and not forzar:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario tiene {noticias_count} noticias asociadas. Use forzar=true para eliminarlo de todas formas."
        )
    
    # Quitar como supervisor de otros usuarios
    db.query(orm_models.Usuario).filter(
        orm_models.Usuario.supervisor_id == user_id
    ).update({'supervisor_id': None})
    
    if forzar:
        # Eliminación física
        db.delete(usuario)
        mensaje = f"Usuario {usuario.username} eliminado permanentemente"
    else:
        # Solo desactivar
        usuario.is_active = False
        mensaje = f"Usuario {usuario.username} desactivado"
    
    db.commit()
    
    return ResponseModel(
        success=True,
        message=mensaje
    )


@router.get("/admin/jerarquia", response_model=List[dict])
async def get_jerarquia_organizacional(
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(require_admin_or_director)
):
    """
    Obtener estructura jerárquica organizacional en formato de árbol
    
    Retorna una estructura anidada con todos los usuarios y sus subordinados
    """
    # Obtener todos los usuarios según permisos
    if current_user.role == 'admin':
        usuarios = db.query(orm_models.Usuario).filter(
            orm_models.Usuario.is_active == True
        ).all()
    else:  # director
        usuarios = db.query(orm_models.Usuario).filter(
            orm_models.Usuario.is_active == True,
            orm_models.Usuario.role != 'admin'
        ).all()
    
    # Construir diccionario para lookup eficiente
    usuarios_dict = {u.id: u for u in usuarios}
    
    def build_user_node(usuario):
        """Construir nodo de usuario con información básica"""
        return {
            'id': usuario.id,
            'username': usuario.username,
            'nombre_completo': usuario.nombre_completo,
            'role': usuario.role,
            'email': usuario.email,
            'subordinados_count': len([u for u in usuarios if u.supervisor_id == usuario.id]),
            'subordinados': []
        }
    
    def build_tree(supervisor_id=None):
        """Construir árbol recursivamente"""
        subordinados = [u for u in usuarios if u.supervisor_id == supervisor_id]
        tree = []
        
        for usuario in subordinados:
            node = build_user_node(usuario)
            node['subordinados'] = build_tree(usuario.id)
            tree.append(node)
        
        # Ordenar por role y nombre
        tree.sort(key=lambda x: (x['role'], x['nombre_completo']))
        return tree
    
    # Construir árbol completo
    jerarquia = build_tree(None)
    
    return jerarquia


@router.post("/admin/usuarios/{user_id}/reset-password", response_model=ResponseModel)
async def reset_password_usuario(
    user_id: int,
    nueva_password: str = Query(..., min_length=6, description="Nueva contraseña"),
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(require_admin_or_director)
):
    """
    Resetear contraseña de un usuario
    """
    from utils.security import get_password_hash
    
    usuario = db.query(orm_models.Usuario).filter(
        orm_models.Usuario.id == user_id
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    if not can_manage_user(current_user, usuario):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para resetear la contraseña de este usuario"
        )
    
    # Actualizar contraseña
    usuario.hashed_password = get_password_hash(nueva_password)
    db.commit()
    
    return ResponseModel(
        success=True,
        message=f"Contraseña reseteada para {usuario.username}"
    )