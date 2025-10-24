"""
Entorno de Alembic para migraciones
Conecta con la configuración de SQLAlchemy
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importar configuración y modelos
from config import settings
from core.database import Base
from models import orm_models  # Importar para que SQLAlchemy conozca los modelos

# Configuración de Alembic
config = context.config

# Configurar logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de los modelos para autogenerar migraciones
target_metadata = Base.metadata

# Sobrescribir DATABASE_URL desde settings
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """
    Ejecutar migraciones en modo 'offline'.
    Genera SQL sin conectarse a la BD.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Ejecutar migraciones en modo 'online'.
    Se conecta a la BD y ejecuta las migraciones.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
