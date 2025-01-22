"""add tone to help assistant

Revision ID: 2025_01_22_add_tone
Revises: previous_revision_id  # Replace with your last migration's revision ID
Create Date: 2025-01-22 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '2025_01_22_add_tone'
down_revision = None  # Replace with your last migration's revision ID
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