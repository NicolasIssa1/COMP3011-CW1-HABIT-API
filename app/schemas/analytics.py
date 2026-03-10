from pydantic import BaseModel, Field, ConfigDict


class StreakOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    habit_id: int = Field(..., description="ID of the habit")
    current_streak: int = Field(..., description="Current consecutive days completed")
    longest_streak: int = Field(..., description="Longest streak achieved")
    total_completions: int = Field(..., description="Total number of completions")


class WeeklySummaryItem(BaseModel):
    habit_id: int = Field(..., description="ID of the habit")
    habit_name: str = Field(..., description="Name of the habit")
    completions: int = Field(..., description="Number of completions this week")


class WeeklySummaryOut(BaseModel):
    week: str = Field(..., description="Week in YYYY-WW format")
    items: list[WeeklySummaryItem] = Field(..., description="List of habits and their completions")
    total_completions: int = Field(..., description="Total completions across all habits this week")
