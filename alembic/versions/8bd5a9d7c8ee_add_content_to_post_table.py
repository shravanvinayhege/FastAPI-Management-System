"""add content to post table

Revision ID: 8bd5a9d7c8ee
Revises: ad693f9b0163
Create Date: 2026-04-09 17:45:37.803340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bd5a9d7c8ee'
down_revision: Union[str, Sequence[str], None] = 'ad693f9b0163'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op: `content` is already created in the base revision.
    pass


def downgrade() -> None:
    # No-op to keep backward compatibility with existing revision history.
    pass
