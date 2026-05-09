"""add workspace owner

Revision ID: 0003_add_workspace_owner
Revises: 0002_add_documents
Create Date: 2026-05-08
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_add_workspace_owner"
down_revision = "0002_add_documents"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "sessions",
        sa.Column("owner_id", sa.String(length=120), nullable=False, server_default="anonymous"),
    )
    op.create_index("ix_sessions_owner_id", "sessions", ["owner_id"])


def downgrade() -> None:
    op.drop_index("ix_sessions_owner_id", table_name="sessions")
    op.drop_column("sessions", "owner_id")
