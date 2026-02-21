from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogCreate, HabitLogOut

router = APIRouter(prefix="/habits/{habit_id}/logs", tags=["logs"])


def _ensure_habit_exists(habit_id: int, db: Session) -> None:
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")


@router.post("", response_model=HabitLogOut, status_code=status.HTTP_201_CREATED)
def create_log(habit_id: int, payload: HabitLogCreate, db: Session = Depends(get_db)):
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
        # Unique constraint (habit_id, date) -> duplicate completion
        raise HTTPException(status_code=409, detail="Log already exists for this habit and date")

    db.refresh(log)
    return log


@router.get("", response_model=list[HabitLogOut])
def list_logs(
    habit_id: int,
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db),
):
    _ensure_habit_exists(habit_id, db)

    q = db.query(HabitLog).filter(HabitLog.habit_id == habit_id)

    if from_date is not None:
        q = q.filter(HabitLog.date >= from_date)
    if to_date is not None:
        q = q.filter(HabitLog.date <= to_date)

    return q.order_by(HabitLog.date.asc()).all()


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(habit_id: int, log_id: int, db: Session = Depends(get_db)):
    _ensure_habit_exists(habit_id, db)

    log = (
        db.query(HabitLog)
        .filter(HabitLog.id == log_id, HabitLog.habit_id == habit_id)
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(log)
    db.commit()
    return None
