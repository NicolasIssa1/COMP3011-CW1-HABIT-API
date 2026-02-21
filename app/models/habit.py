from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from app.db.base import Base


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(String(500), nullable=True)
    frequency = Column(String(20), nullable=False, default="daily")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
