"""Add tone to help assistant

Revision ID: xxx
Revises: xxx
Create Date: 2025-01-22
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add tone column with default value
    op.add_column('help_assistant', 
        sa.Column('tone', sa.String(), nullable=False, server_default='PROFESSIONAL')
    )

def downgrade():
    # Remove tone column
    op.drop_column('help_assistant', 'tone') 