"""Add tables task and events_users


Revision ID: 76437ccfebff
Revises: 50e79ffd061b
Create Date: 2025-05-17 17:50:17.606732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76437ccfebff'
down_revision: Union[str, None] = '50e79ffd061b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('events_users',
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('joined_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('member_id', 'event_id')
    )
    op.create_table('tasks_users',
    sa.Column('worker_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('joined_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['worker_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('worker_id', 'task_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tasks_users')
    op.drop_table('events_users')
    op.drop_table('tasks')
