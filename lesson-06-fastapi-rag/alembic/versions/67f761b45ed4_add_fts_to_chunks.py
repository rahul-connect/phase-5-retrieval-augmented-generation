"""add fts to chunks

Revision ID: 67f761b45ed4
Revises: 2da87e6c0517
Create Date: 2026-10-28 17:32:15.370024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '67f761b45ed4'
down_revision: Union[str, Sequence[str], None] = '2da87e6c0517'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "rag_chunks",
        sa.Column(
            "content_tsv",
            postgresql.TSVECTOR(),
            sa.Computed("to_tsvector('english', content)", persisted=True),
            nullable=False,
        ),
    )

    op.execute(
        "CREATE INDEX ix_rag_chunks_content_tsv "
        "ON rag_chunks USING GIN (content_tsv)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX ix_rag_chunks_content_tsv")
    op.drop_column("rag_chunks", "content_tsv")