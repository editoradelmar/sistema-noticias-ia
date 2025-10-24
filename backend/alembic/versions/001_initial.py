"""
Migración inicial - Crear todas las tablas base
Revision ID: 001_initial
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crear tablas"""
    
    # Tabla proyectos
    op.create_table(
        'proyectos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=200), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('estado', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_proyectos_id'), 'proyectos', ['id'], unique=False)
    op.create_index(op.f('ix_proyectos_nombre'), 'proyectos', ['nombre'], unique=False)
    
    # Tabla noticias
    op.create_table(
        'noticias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(length=200), nullable=False),
        sa.Column('contenido', sa.Text(), nullable=False),
        sa.Column('categoria', sa.String(length=50), nullable=False),
        sa.Column('autor', sa.String(length=100), nullable=True),
        sa.Column('resumen_ia', sa.Text(), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('keywords', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('fecha', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('proyecto_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['proyecto_id'], ['proyectos.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_noticias_categoria'), 'noticias', ['categoria'], unique=False)
    op.create_index(op.f('ix_noticias_id'), 'noticias', ['id'], unique=False)
    op.create_index(op.f('ix_noticias_titulo'), 'noticias', ['titulo'], unique=False)
    
    # Tabla documentos_contexto
    op.create_table(
        'documentos_contexto',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('ruta_archivo', sa.String(length=500), nullable=True),
        sa.Column('url', sa.String(length=1000), nullable=True),
        sa.Column('contenido_extraido', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('proyecto_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['proyecto_id'], ['proyectos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documentos_contexto_id'), 'documentos_contexto', ['id'], unique=False)
    
    # Tabla conversaciones_ia
    op.create_table(
        'conversaciones_ia',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversacion_id', sa.String(length=100), nullable=False),
        sa.Column('mensajes', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('conversacion_id')
    )
    op.create_index(op.f('ix_conversaciones_ia_conversacion_id'), 'conversaciones_ia', ['conversacion_id'], unique=True)
    op.create_index(op.f('ix_conversaciones_ia_id'), 'conversaciones_ia', ['id'], unique=False)
    


def downgrade() -> None:
    """Eliminar tablas"""
    op.drop_index(op.f('ix_conversaciones_ia_id'), table_name='conversaciones_ia')
    op.drop_index(op.f('ix_conversaciones_ia_conversacion_id'), table_name='conversaciones_ia')
    op.drop_table('conversaciones_ia')
    op.drop_index(op.f('ix_documentos_contexto_id'), table_name='documentos_contexto')
    op.drop_table('documentos_contexto')
    op.drop_index(op.f('ix_noticias_titulo'), table_name='noticias')
    op.drop_index(op.f('ix_noticias_id'), table_name='noticias')
    op.drop_index(op.f('ix_noticias_categoria'), table_name='noticias')
    op.drop_table('noticias')
    op.drop_index(op.f('ix_proyectos_nombre'), table_name='proyectos')
    op.drop_index(op.f('ix_proyectos_id'), table_name='proyectos')
    op.drop_table('proyectos')
