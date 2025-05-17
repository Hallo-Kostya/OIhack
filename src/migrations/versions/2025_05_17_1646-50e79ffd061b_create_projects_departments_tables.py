"""Create Projects departments tables

Revision ID: 50e79ffd061b
Revises: 84cc23a2b5d2
Create Date: 2025-05-17 16:46:16.662824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50e79ffd061b'
down_revision: Union[str, None] = '84cc23a2b5d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('workers_projects',
    sa.Column('worker_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('joined_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['worker_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('worker_id', 'project_id')
    )
    op.drop_column('events', 'location')
    op.add_column('users', sa.Column('role', sa.Enum('HR', 'MANAGER', 'WORKER', name='workrole'), nullable=False))
    op.drop_column('users', 'department')
    op.drop_column('users', 'position')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('position', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('department', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_column('users', 'role')
    op.add_column('events', sa.Column('location', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_table('workers_projects')
    op.drop_table('projects')
    op.drop_table('departments')
