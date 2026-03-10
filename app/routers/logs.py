from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogCreate, HabitLogOut
from app.core.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/habits/{habit_id}/logs", tags=["logs"])


def _ensure_habit_exists(habit_id: int, db: Session) -> None:
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit with ID {habit_id} not found")


@router.post(
    "",
    response_model=HabitLogOut,
    status_code=status.HTTP_201_CREATED,
    summary="Log a habit completion",
    responses={409: {"description": "Log already exists for this date"}},
)
def create_log(habit_id: int, payload: HabitLogCreate, db: Session = Depends(get_db)):
    """Log the completion of a habit on a specific date."""
    _ensure_habit_exists(habit_id, db)

    log = HabitLog(
        habit_id=habit_id,
        date=payload.date,
        notes=payload.notes,
    )
    db.add(log)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Log already exists for habit {habit_id} on {payload.date}",
        )

    db.refresh(log)
    return log


@router.get(
    "",
    response_model=list[HabitLogOut],
    summary="List habit logs",
    responses={404: {"description": "Habit not found"}},
)
def list_logs(
    habit_id: int,
    from_date: date | None = Query(None, description="Start date (inclusive)"),
    to_date: date | None = Query(None, description="End date (inclusive)"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Number of items to return"),
    db: Session = Depends(get_db),
):
    """List all logs for a specific habit with optional date filtering."""
    _ensure_habit_exists(habit_id, db)

    q = db.query(HabitLog).filter(HabitLog.habit_id == habit_id)

    if from_date is not None:
        q = q.filter(HabitLog.date >= from_date)
    if to_date is not None:
        q = q.filter(HabitLog.date <= to_date)

    return q.order_by(HabitLog.date.asc()).offset(skip).limit(limit).all()


@router.delete(
    "/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a log entry",
    responses={404: {"description": "Log not found"}},
)
def delete_log(habit_id: int, log_id: int, db: Session = Depends(get_db)):
    """Delete a specific log entry for a habit."""
    _ensure_habit_exists(habit_id, db)

    log = (
        db.query(HabitLog)
        .filter(HabitLog.id == log_id, HabitLog.habit_id == habit_id)
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail=f"Log with ID {log_id} not found")

    db.delete(log)
    db.commit()
    return None
