"""
Alembic migration script: Agrega columna 'estado' a la tabla 'noticias'.
"""

revision = 'add_estado_to_noticias'
down_revision = '004_add_llm_id_to_noticias'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('noticias', sa.Column('estado', sa.String(length=50), nullable=False, server_default='activo'))
    op.create_index('ix_noticias_estado', 'noticias', ['estado'])

def downgrade():
    op.drop_index('ix_noticias_estado', table_name='noticias')
    op.drop_column('noticias', 'estado')
