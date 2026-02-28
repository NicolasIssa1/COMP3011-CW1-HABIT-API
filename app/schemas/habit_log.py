from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class HabitLogCreate(BaseModel):
    date: date
    notes: str | None = Field(default=None, max_length=500)


class HabitLogOut(BaseModel):
    id: int
    habit_id: int
    date: date
    notes: str | None

    model_config = ConfigDict(from_attributes=True)