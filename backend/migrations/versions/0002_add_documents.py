"""add documents

Revision ID: 0002_add_documents
Revises: 0001_initial_schema
Create Date: 2026-05-08
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_add_documents"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("content_text", sa.Text(), nullable=False),
        sa.Column("source_type", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_session_id", "documents", ["session_id"])


def downgrade() -> None:
    op.drop_index("ix_documents_session_id", table_name="documents")
    op.drop_table("documents")
