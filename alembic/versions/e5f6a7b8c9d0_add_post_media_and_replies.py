"""add post media and nested replies

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-09-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, Sequence[str], None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("image_url", sa.String(length=2048), nullable=True))
    op.add_column("posts", sa.Column("video_url", sa.String(length=2048), nullable=True))

    op.create_table(
        "post_replies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=2000), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.CheckConstraint("parent_id IS NULL OR parent_id <> id", name="ck_post_replies_no_self_parent"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_id"], ["post_replies.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_post_replies_post_id", "post_replies", ["post_id"])
    op.create_index("ix_post_replies_parent_id", "post_replies", ["parent_id"])
    op.create_index("ix_post_replies_owner_id", "post_replies", ["owner_id"])
    op.create_index("ix_post_replies_created_at", "post_replies", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_post_replies_created_at", table_name="post_replies")
    op.drop_index("ix_post_replies_owner_id", table_name="post_replies")
    op.drop_index("ix_post_replies_parent_id", table_name="post_replies")
    op.drop_index("ix_post_replies_post_id", table_name="post_replies")
    op.drop_table("post_replies")
    op.drop_column("posts", "video_url")
    op.drop_column("posts", "image_url")
