from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.habit_log import HabitLog


def _dates_from_logs(logs: list[HabitLog]) -> set[date]:
    return {log.date for log in logs}


def current_streak(dates_done: set[date], today: date) -> int:
    streak = 0
    d = today
    while d in dates_done:
        streak += 1
        d = d - timedelta(days=1)
    return streak


def longest_streak(dates_done: set[date]) -> int:
    if not dates_done:
        return 0

    best = 0
    for d in dates_done:
        if (d - timedelta(days=1)) not in dates_done:
            length = 1
            nxt = d + timedelta(days=1)
            while nxt in dates_done:
                length += 1
                nxt = nxt + timedelta(days=1)
            best = max(best, length)
    return best


def streak_stats(db: Session, habit_id: int, today: date) -> dict:
    logs = db.query(HabitLog).filter(HabitLog.habit_id == habit_id).all()
    done = _dates_from_logs(logs)
    return {
        "habit_id": habit_id,
        "current_streak": current_streak(done, today),
        "longest_streak": longest_streak(done),
        "total_completions": len(done),
    }
