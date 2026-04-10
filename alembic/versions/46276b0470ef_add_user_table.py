"""add user table

Revision ID: 46276b0470ef
Revises: 8bd5a9d7c8ee
Create Date: 2026-04-09 17:50:51.561789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46276b0470ef'
down_revision: Union[str, Sequence[str], None] = '8bd5a9d7c8ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op: `users` is already created in the base revision.
    pass


def downgrade() -> None:
    # No-op to keep backward compatibility with existing revision history.
    pass
