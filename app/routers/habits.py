from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitOut

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate, db: Session = Depends(get_db)):
    habit = Habit(
        name=payload.name.strip(),
        description=payload.description,
        frequency=payload.frequency,
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.get("", response_model=list[HabitOut])
def list_habits(db: Session = Depends(get_db)):
    habits = db.query(Habit).order_by(Habit.id.asc()).all()
    return habits
