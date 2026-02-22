from pydantic import BaseModel


class StreakOut(BaseModel):
    habit_id: int
    current_streak: int
    longest_streak: int
    total_completions: int


class WeeklySummaryItem(BaseModel):
    habit_id: int
    habit_name: str
    completions: int


class WeeklySummaryOut(BaseModel):
    week: str
    items: list[WeeklySummaryItem]
    total_completions: int
