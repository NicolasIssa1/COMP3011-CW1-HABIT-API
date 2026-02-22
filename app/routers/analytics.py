from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.schemas.analytics import StreakOut, WeeklySummaryOut, WeeklySummaryItem
from app.services.streak_service import streak_stats

router = APIRouter(tags=["analytics"])


@router.get("/habits/{habit_id}/streak", response_model=StreakOut)
def get_streak(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return streak_stats(db, habit_id, today=date.today())


def _parse_week(week: str) -> tuple[int, int]:
    try:
        year_str, week_str = week.split("-")
        return int(year_str), int(week_str)
    except Exception:
        raise HTTPException(status_code=400, detail="week must be in format YYYY-WW")


@router.get("/analytics/weekly-summary", response_model=WeeklySummaryOut)
def weekly_summary(week: str, db: Session = Depends(get_db)):
    year, week_num = _parse_week(week)

    start = date.fromisocalendar(year, week_num, 1)
    end = date.fromisocalendar(year, week_num, 7)

    habits = db.query(Habit).order_by(Habit.id.asc()).all()

    items: list[WeeklySummaryItem] = []
    total = 0

    for h in habits:
        count = (
            db.query(HabitLog)
            .filter(HabitLog.habit_id == h.id, HabitLog.date >= start, HabitLog.date <= end)
            .count()
        )
        items.append(WeeklySummaryItem(habit_id=h.id, habit_name=h.name, completions=count))
        total += count

    return WeeklySummaryOut(week=week, items=items, total_completions=total)
