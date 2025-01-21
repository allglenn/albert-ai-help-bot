"""add albert_ai_id to files

Revision ID: add_albert_ai_id_to_files
Revises: 1234567890ab
Create Date: 2024-01-21

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_albert_ai_id_to_files'
down_revision = '1234567890ab'  # This should be your previous migration ID
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('assistant_files', sa.Column('albert_ai_id', sa.String(), nullable=True))

def downgrade():
    op.drop_column('assistant_files', 'albert_ai_id') 