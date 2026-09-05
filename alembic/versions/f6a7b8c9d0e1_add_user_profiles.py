"""add user profile fields

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-09-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f6a7b8c9d0e1"
down_revision: Union[str, Sequence[str], None] = "e5f6a7b8c9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(length=50), nullable=True))
    op.add_column("users", sa.Column("display_name", sa.String(length=100), nullable=True))
    op.add_column("users", sa.Column("bio", sa.String(length=1000), nullable=True))
    op.add_column("users", sa.Column("avatar_url", sa.String(length=2048), nullable=True))
    op.add_column("users", sa.Column("avatar_type", sa.String(length=20), server_default="default", nullable=True))
    op.add_column("users", sa.Column("profile_visibility", sa.String(length=20), server_default="public", nullable=True))
    op.add_column("users", sa.Column("show_posts", sa.Boolean(), server_default="true", nullable=True))
    op.add_column("users", sa.Column("show_communities", sa.Boolean(), server_default="true", nullable=True))
    op.add_column("users", sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=True))

    op.execute(sa.text("""
        WITH normalized AS (
            SELECT
                id,
                email,
                CASE
                    WHEN regexp_replace(lower(split_part(email, '@', 1)), '[^a-z0-9_]+', '_', 'g') = ''
                    THEN 'user'
                    ELSE regexp_replace(lower(split_part(email, '@', 1)), '[^a-z0-9_]+', '_', 'g')
                END AS base_name
            FROM users
        ), ranked AS (
            SELECT id,
                   CASE WHEN length(base_name) > 39
                        THEN left(base_name, 39) || '_' || substr(md5(email), 1, 10)
                        ELSE base_name
                   END AS base_name,
                   row_number() OVER (PARTITION BY base_name ORDER BY id) AS position
            FROM normalized
        )
        UPDATE users
        SET username = left(ranked.base_name || CASE WHEN ranked.position = 1 THEN '' ELSE '_' || ranked.position::text END, 50),
            display_name = left(ranked.base_name || CASE WHEN ranked.position = 1 THEN '' ELSE '_' || ranked.position::text END, 100),
            avatar_type = 'default',
            profile_visibility = 'public',
            show_posts = true,
            show_communities = true,
            updated_at = NOW()
        FROM ranked
        WHERE users.id = ranked.id
    """))

    op.alter_column("users", "username", nullable=False)
    op.alter_column("users", "display_name", nullable=False)
    op.alter_column("users", "avatar_type", nullable=False)
    op.alter_column("users", "profile_visibility", nullable=False)
    op.alter_column("users", "show_posts", nullable=False)
    op.alter_column("users", "show_communities", nullable=False)
    op.alter_column("users", "updated_at", nullable=False)
    op.create_unique_constraint("uq_users_username", "users", ["username"])
    op.create_index("ix_users_username", "users", ["username"])
    op.create_check_constraint("ck_users_profile_visibility", "users", "profile_visibility IN ('public', 'private')")
    op.create_check_constraint("ck_users_avatar_type", "users", "avatar_type IN ('default', 'uploaded', 'generated')")


def downgrade() -> None:
    op.drop_constraint("ck_users_avatar_type", "users", type_="check")
    op.drop_constraint("ck_users_profile_visibility", "users", type_="check")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_constraint("uq_users_username", "users", type_="unique")
    for column in ("updated_at", "show_communities", "show_posts", "profile_visibility", "avatar_type", "avatar_url", "bio", "display_name", "username"):
        op.drop_column("users", column)