"""create document chunks

Revision ID: 5c06a048340f
Revises:
Create Date: 2026-08-27 05:10:30.406338

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "5c06a048340f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "document_chunks",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "report_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "section",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "page",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "embedding",
            Vector(1536),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_document_chunks_report_id"),
        "document_chunks",
        ["report_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_document_chunks_user_id"),
        "document_chunks",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_document_chunks_user_id"),
        table_name="document_chunks",
    )

    op.drop_index(
        op.f("ix_document_chunks_report_id"),
        table_name="document_chunks",
    )

    op.drop_table("document_chunks")