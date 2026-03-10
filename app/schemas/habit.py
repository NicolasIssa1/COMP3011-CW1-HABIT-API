from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class HabitFrequency(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class HabitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Name of the habit")
    description: str | None = Field(default=None, max_length=500, description="Description of the habit")
    frequency: HabitFrequency = Field(default=HabitFrequency.daily, description="Frequency of the habit")


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120, description="Updated habit name")
    description: str | None = Field(default=None, max_length=500, description="Updated description")
    frequency: HabitFrequency | None = Field(default=None, description="Updated frequency")
    is_active: bool | None = Field(default=None, description="Whether the habit is active")


class HabitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    frequency: HabitFrequency
    is_active: bool
    created_at: datetime