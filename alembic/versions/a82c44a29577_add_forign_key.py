"""add forign key

Revision ID: a82c44a29577
Revises: 46276b0470ef
Create Date: 2026-04-09 17:55:21.627257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a82c44a29577'
down_revision: Union[str, Sequence[str], None] = '46276b0470ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op: `owner_id` and FK are already created in the base revision.
    pass


def downgrade() -> None:
    # No-op to keep backward compatibility with existing revision history.
    pass
