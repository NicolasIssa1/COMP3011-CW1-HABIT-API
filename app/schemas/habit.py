from datetime import datetime
from pydantic import BaseModel, Field


class HabitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    frequency: str = Field(default="daily", max_length=20)


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    frequency: str | None = Field(default=None, max_length=20)
    is_active: bool | None = None


class HabitOut(BaseModel):
    id: int
    name: str
    description: str | None
    frequency: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
