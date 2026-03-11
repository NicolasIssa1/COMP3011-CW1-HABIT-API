import re
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.schemas.analytics import StreakOut, WeeklySummaryOut, WeeklySummaryItem
from app.services.streak_service import streak_stats
from app.core.security import verify_api_key

router = APIRouter(tags=["analytics"])

_WEEK_RE = re.compile(r"^(?P<year>\d{4})-W?(?P<week>\d{2})$")


@router.get(
    "/habits/{habit_id}/streak",
    response_model=StreakOut,
    summary="Get habit streak statistics",
    responses={404: {"description": "Habit not found"}, 401: {"description": "Missing API key"}, 403: {"description": "Invalid API key"}},
)
def get_streak(habit_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    """Get current streak, longest streak, and total completions for a habit."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit with ID {habit_id} not found")
    return streak_stats(db, habit_id, today=date.today())


def _parse_week(week: str) -> tuple[int, int]:
    """
    Accepts both:
      - YYYY-WW   (e.g. 2026-09)
      - YYYY-WWW  (e.g. 2026-W09)
    """
    m = _WEEK_RE.match(week)
    if not m:
        raise HTTPException(
            status_code=400,
            detail="week must be in format YYYY-WW or YYYY-Www (e.g. 2026-09 or 2026-W09)",
        )
    return int(m.group("year")), int(m.group("week"))


@router.get(
    "/analytics/weekly-summary",
    response_model=WeeklySummaryOut,
    summary="Get weekly summary of all habits",
    responses={400: {"description": "Invalid week format"}, 401: {"description": "Missing API key"}, 403: {"description": "Invalid API key"}},
)
def weekly_summary(
    week: str = Query(
        ...,
        description="Week in YYYY-WW or YYYY-WWW format (e.g. 2026-09)",
    ),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Get a summary of all habits' completions for a specific week (ISO week format)."""
    year, week_num = _parse_week(week)

    try:
        start = date.fromisocalendar(year, week_num, 1)
        end = date.fromisocalendar(year, week_num, 7)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid ISO week: {week}")

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