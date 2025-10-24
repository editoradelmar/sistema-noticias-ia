"""
Revision ID: 005_add_prompt_item_table
Revises: 004_add_llm_id_to_noticias
Create Date: 2025-10-24

Alembic migration: crea la tabla prompt_item para asociar items a PromptMaestro
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005_add_prompt_item_table'
down_revision = 'add_estado_to_noticias'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'prompt_item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('prompt_id', sa.Integer, sa.ForeignKey('prompt_maestro.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('nombre_archivo', sa.String(200), nullable=False),
        sa.Column('orden', sa.Integer, nullable=False, default=1),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('idx_prompt_item_prompt_id', 'prompt_item', ['prompt_id'])
    op.create_index('idx_prompt_item_orden', 'prompt_item', ['orden'])

def downgrade():
    op.drop_index('idx_prompt_item_prompt_id', table_name='prompt_item')
    op.drop_index('idx_prompt_item_orden', table_name='prompt_item')
    op.drop_table('prompt_item')
