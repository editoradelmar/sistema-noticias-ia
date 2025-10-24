revision = '003_remove_llm_prompt_estilo_from_noticia_salida'
down_revision = '002_remove_categoria_add_seccion'
branch_labels = None
depends_on = None
"""
Remove llm_usado_id, prompt_usado_id, estilo_usado_id from noticia_salida
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('noticia_salida') as batch_op:
        batch_op.drop_column('llm_usado_id')
        batch_op.drop_column('prompt_usado_id')
        batch_op.drop_column('estilo_usado_id')

def downgrade():
    with op.batch_alter_table('noticia_salida') as batch_op:
        batch_op.add_column(sa.Column('llm_usado_id', sa.Integer(), sa.ForeignKey('llm_maestro.id', ondelete='SET NULL'), nullable=True))
        batch_op.add_column(sa.Column('prompt_usado_id', sa.Integer(), sa.ForeignKey('prompt_maestro.id', ondelete='SET NULL'), nullable=True))
        batch_op.add_column(sa.Column('estilo_usado_id', sa.Integer(), sa.ForeignKey('estilo_maestro.id', ondelete='SET NULL'), nullable=True))
