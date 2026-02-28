from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class HabitFrequency(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class HabitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    frequency: HabitFrequency = Field(default=HabitFrequency.daily)


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    frequency: HabitFrequency | None = None
    is_active: bool | None = None


class HabitOut(BaseModel):
    id: int
    name: str
    description: str | None
    frequency: HabitFrequency
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)