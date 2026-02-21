from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitOut, HabitUpdate

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
    return db.query(Habit).order_by(Habit.id.asc()).all()


@router.get("/{habit_id}", response_model=HabitOut)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.patch("/{habit_id}", response_model=HabitOut)
def update_habit(habit_id: int, payload: HabitUpdate, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    data = payload.model_dump(exclude_unset=True)

    # Optional: strip name if provided
    if "name" in data and data["name"] is not None:
        data["name"] = data["name"].strip()

    for key, value in data.items():
        setattr(habit, key, value)

    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(habit)
    db.commit()
    return None
