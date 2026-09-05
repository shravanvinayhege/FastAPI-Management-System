"""add post shares

Revision ID: a7b8c9d0e1f2
Revises: f6a7b8c9d0e1
Create Date: 2026-09-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7b8c9d0e1f2"
down_revision: Union[str, Sequence[str], None] = "f6a7b8c9d0e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "post_shares",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("post_id", "user_id", name="uq_post_shares_post_user"),
    )
    op.create_index("ix_post_shares_post_id", "post_shares", ["post_id"])
    op.create_index("ix_post_shares_user_id", "post_shares", ["user_id"])
    op.create_index("ix_post_shares_created_at", "post_shares", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_post_shares_created_at", table_name="post_shares")
    op.drop_index("ix_post_shares_user_id", table_name="post_shares")
    op.drop_index("ix_post_shares_post_id", table_name="post_shares")
    op.drop_table("post_shares")
