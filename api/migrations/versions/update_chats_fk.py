"""Update chats foreign key constraint"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Drop existing constraint
    op.drop_constraint('chats_user_id_fkey', 'chats', type_='foreignkey')
    
    # Add new constraint
    op.create_foreign_key(
        'chats_user_id_fkey',
        'chats',
        'users',  # Changed from 'user' to 'users'
        ['user_id'],
        ['id']
    )

def downgrade():
    # Drop new constraint
    op.drop_constraint('chats_user_id_fkey', 'chats', type_='foreignkey')
    
    # Restore original constraint
    op.create_foreign_key(
        'chats_user_id_fkey',
        'chats',
        'user',
        ['user_id'],
        ['id']
    ) 