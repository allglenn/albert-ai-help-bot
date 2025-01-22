"""add tone column

Revision ID: 202501221234
Revises: 202501221233
Create Date: 2025-01-22 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '202501221234'
down_revision = '202501221233'  # Point to the chats migration
branch_labels = None
depends_on = None


def upgrade():
    # Add tone column with default value
    op.add_column('help_assistant', 
        sa.Column('tone', sa.String(), nullable=False, server_default='PROFESSIONAL')
    )


def downgrade():
    # Remove tone column
    op.drop_column('help_assistant', 'tone') 