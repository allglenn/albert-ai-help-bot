"""add collection id to files

Revision ID: 1234567890ab
Revises: 
Create Date: 2024-03-14

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1234567890ab'
down_revision = None  # Set to None since it's the first migration
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('assistant_files', sa.Column('assistant_collection_id', sa.String(), nullable=True))

def downgrade():
    op.drop_column('assistant_files', 'assistant_collection_id') 