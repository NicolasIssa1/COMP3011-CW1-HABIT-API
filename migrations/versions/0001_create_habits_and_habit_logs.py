"""Create habits and habit_logs tables

Revision ID: 0001
Revises: 
Create Date: 2026-02-21
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "habits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("frequency", sa.String(length=20), nullable=False, server_default="daily"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_habits_id", "habits", ["id"])

    op.create_table(
        "habit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("habit_id", sa.Integer(), sa.ForeignKey("habits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.UniqueConstraint("habit_id", "date", name="uq_habit_date"),
    )
    op.create_index("ix_habit_logs_id", "habit_logs", ["id"])
    op.create_index("ix_habit_logs_habit_id", "habit_logs", ["habit_id"])


def downgrade() -> None:
    op.drop_index("ix_habit_logs_habit_id", table_name="habit_logs")
    op.drop_index("ix_habit_logs_id", table_name="habit_logs")
    op.drop_table("habit_logs")

    op.drop_index("ix_habits_id", table_name="habits")
    op.drop_table("habits")
