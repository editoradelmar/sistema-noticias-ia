"""
Alembic migration: add llm_id to noticias
"""
revision = '004_add_llm_id_to_noticias'
down_revision = '003_remove_llm_prompt_estilo_from_noticia_salida'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('noticias', sa.Column('llm_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_noticias_llm_id', 'noticias', 'llm_maestro', ['llm_id'], ['id'], ondelete='SET NULL')

def downgrade():
    op.drop_constraint('fk_noticias_llm_id', 'noticias', type_='foreignkey')
    op.drop_column('noticias', 'llm_id')
