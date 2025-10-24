"""
Revision ID: 006_add_contenido_to_prompt_item
Revises: 005_add_prompt_item_table
Create Date: 2025-10-24

Alembic migration: agrega el campo 'contenido' tipo TEXT a la tabla prompt_item
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006_add_contenido_to_prompt_item'
down_revision = '005_add_prompt_item_table'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('prompt_item', sa.Column('contenido', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('prompt_item', 'contenido')
