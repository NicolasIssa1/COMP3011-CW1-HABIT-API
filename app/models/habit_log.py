from sqlalchemy import Column, Date, ForeignKey, Integer, String, UniqueConstraint
from app.db.base import Base


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    notes = Column(String(500), nullable=True)

    __table_args__ = (
        UniqueConstraint("habit_id", "date", name="uq_habit_date"),
    )
