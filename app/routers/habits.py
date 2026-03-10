from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitOut, HabitUpdate
from app.core.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post(
    "",
    response_model=HabitOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new habit",
    responses={400: {"description": "Invalid input"}}
)
def create_habit(payload: HabitCreate, db: Session = Depends(get_db)):
    """Create a new habit to track."""
    habit = Habit(
        name=payload.name.strip(),
        description=payload.description,
        frequency=payload.frequency,
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.get(
    "",
    response_model=list[HabitOut],
    summary="List all habits",
    responses={200: {"description": "List of habits"}}
)
def list_habits(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Number of items to return"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    frequency: str | None = Query(None, description="Filter by frequency (daily, weekly, monthly)"),
    db: Session = Depends(get_db)
):
    """List all habits with optional filtering and pagination."""
    query = db.query(Habit)
    
    if is_active is not None:
        query = query.filter(Habit.is_active == is_active)
    
    if frequency is not None:
        query = query.filter(Habit.frequency == frequency)
    
    return query.order_by(Habit.id.asc()).offset(skip).limit(limit).all()


@router.get(
    "/{habit_id}",
    response_model=HabitOut,
    summary="Get a specific habit",
    responses={404: {"description": "Habit not found"}}
)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific habit by ID."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit with ID {habit_id} not found")
    return habit


@router.patch(
    "/{habit_id}",
    response_model=HabitOut,
    summary="Update a habit",
    responses={404: {"description": "Habit not found"}}
)
def update_habit(
    habit_id: int,
    payload: HabitUpdate,
    db: Session = Depends(get_db)
):
    """Update a habit's details."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit with ID {habit_id} not found")

    data = payload.model_dump(exclude_unset=True)

    if "name" in data and data["name"] is not None:
        data["name"] = data["name"].strip()

    for key, value in data.items():
        setattr(habit, key, value)

    db.commit()
    db.refresh(habit)
    return habit


@router.delete(
    "/{habit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a habit",
    responses={404: {"description": "Habit not found"}}
)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    """Delete a habit and all its associated logs."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit with ID {habit_id} not found")

    db.delete(habit)
    db.commit()
    return None
