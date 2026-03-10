from datetime import date as date_type

from pydantic import BaseModel, Field, ConfigDict


class HabitLogCreate(BaseModel):
    date: date_type = Field(..., description="Date of habit completion")
    notes: str | None = Field(default=None, max_length=500, description="Optional notes about the completion")


class HabitLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    date: date_type
    notes: str | None