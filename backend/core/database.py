"""
Configuración de la base de datos con SQLAlchemy
Gestión de sesiones y conexiones
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from config import settings

# Motor de base de datos
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries en desarrollo
    pool_pre_ping=True,   # Verificar conexiones
    pool_size=10,
    max_overflow=20
)

# Sesión local
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para modelos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener sesión de BD
    Uso: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializar base de datos
    Crear todas las tablas si no existen
    """
    # Importar todos los modelos aquí para que SQLAlchemy los conozca
    from models import orm_models
    
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada correctamente")


def drop_all_tables():
    """
    CUIDADO: Elimina todas las tablas
    Solo para desarrollo/testing
    """
    if settings.DEBUG:
        Base.metadata.drop_all(bind=engine)
        print("⚠️ Todas las tablas eliminadas")
    else:
        raise Exception("No se puede eliminar tablas en producción")
