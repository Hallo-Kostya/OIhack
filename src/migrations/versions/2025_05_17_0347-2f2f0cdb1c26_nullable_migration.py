"""nullable migration

Revision ID: 2f2f0cdb1c26
Revises: a7143b354e8e
Create Date: 2025-05-17 03:47:01.673176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f2f0cdb1c26'
down_revision: Union[str, None] = 'a7143b354e8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('users', 'profile_photo',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'about',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('users', 'hobbies',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('users', 'skills',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('users', 'preferences',
               existing_type=sa.TEXT(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'preferences',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('users', 'skills',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('users', 'hobbies',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('users', 'about',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('users', 'profile_photo',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
