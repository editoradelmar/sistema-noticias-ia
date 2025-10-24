"""
Migración: Quitar columna categoria y agregar seccion_id a Noticia
"""
revision = '002_remove_categoria_add_seccion'
down_revision = '001_initial'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Quitar columna categoria
    with op.batch_alter_table('noticias') as batch_op:
        batch_op.drop_index('ix_noticias_categoria')
        batch_op.drop_column('categoria')
        batch_op.add_column(sa.Column('seccion_id', sa.Integer(), sa.ForeignKey('seccion.id', ondelete='SET NULL'), nullable=True, index=True))


def downgrade():
    # Revertir cambios
    with op.batch_alter_table('noticias') as batch_op:
        batch_op.drop_column('seccion_id')
        batch_op.add_column(sa.Column('categoria', sa.String(length=50), nullable=False))
        batch_op.create_index('ix_noticias_categoria', ['categoria'], unique=False)
