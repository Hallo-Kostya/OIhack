"""create tables

Revision ID: a7143b354e8e
Revises: 32f2daefa518
Create Date: 2025-05-17 03:44:43.255004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7143b354e8e'
down_revision: Union[str, None] = '32f2daefa518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('organizer_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('birth_date', sa.DateTime(), nullable=False),
    sa.Column('position', sa.String(length=100), nullable=False),
    sa.Column('department', sa.String(length=100), nullable=False),
    sa.Column('work_status', sa.Enum('IN_OFFICE', 'REMOTE', 'ON_LEAVE', name='workstatus'), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('profile_photo', sa.String(length=255), nullable=False),
    sa.Column('about', sa.Text(), nullable=False),
    sa.Column('hobbies', sa.Text(), nullable=False),
    sa.Column('skills', sa.Text(), nullable=False),
    sa.Column('preferences', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    op.drop_table('events')
