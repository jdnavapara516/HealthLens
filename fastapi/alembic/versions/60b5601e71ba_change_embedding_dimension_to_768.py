"""change embedding dimension to 768

Revision ID: 60b5601e71ba
Revises: 5c06a048340f
Create Date: 2026-08-27

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import VECTOR


# revision identifiers, used by Alembic.
revision: str = "60b5601e71ba"

down_revision: Union[str, Sequence[str], None] = "5c06a048340f"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "document_chunks",
        "embedding",
        existing_type=VECTOR(dim=1536),
        type_=VECTOR(dim=768),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "document_chunks",
        "embedding",
        existing_type=VECTOR(dim=768),
        type_=VECTOR(dim=1536),
        existing_nullable=True,
    )