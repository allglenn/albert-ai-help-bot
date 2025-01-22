"""add tone column to help_assistant

Revision ID: add_tone_column
Revises: previous_revision_id
Create Date: 2025-01-22
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = 'add_tone_column'
down_revision = None  # Update this with your previous migration ID
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