"""add some few columns to posts table

Revision ID: ef50ab4032cb
Revises: a82c44a29577
Create Date: 2026-04-09 18:27:56.487961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef50ab4032cb'
down_revision: Union[str, Sequence[str], None] = 'a82c44a29577'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op: these columns are already created in the base revision.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # No-op to keep backward compatibility with existing revision history.
    pass
