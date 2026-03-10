# GenAI Conversation Logs - Supplementary Material

**Purpose:** Evidence of GenAI tool usage as required by COMP3011 Assessment Brief Section 2

---

## 1. ChatGPT Conversation Examples

### Conversation 1: FastAPI Project Structure
**Date:** [Feb 2026]  
**Tool:** ChatGPT (GPT-4)  
**Purpose:** Architecture guidance

```
User: "What's the best folder structure for a FastAPI project?"

ChatGPT: "Here's a recommended structure:
project/
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── requirements.txt
└── README.md

This separates concerns and makes the code maintainable..."

User Result: Adopted this structure exactly. See app/ folder in repo.
```

### Conversation 2: Streak Calculation Algorithm
**Date:** [Feb 2026]  
**Tool:** ChatGPT (GPT-4)  
**Purpose:** Algorithm pseudocode

```
User: "How do I calculate a streak of consecutive days from a list of dates?"

ChatGPT: "Pseudocode:
1. Sort dates in ascending order
2. Iterate through dates
3. If date == previous_date + 1 day: increment streak
4. Else: reset streak
5. Track max_streak and current_streak"

User Result: Implemented in app/services/streak_service.py with custom logic
```

### Conversation 3: Database Design Decision
**Date:** [Feb 2026]  
**Tool:** ChatGPT (GPT-4)  
**Purpose:** Design consultation

```
User: "Should I use soft delete or cascade delete for habit logs?"

ChatGPT: "Soft delete (is_active flag): Better for audit trails, data recovery
Cascade delete: Simpler, enforces data consistency

Recommendation: Use cascade delete for dependent tables (habit_logs) 
to ensure integrity when a habit is deleted."

User Result: Implemented both - cascade delete for logs + is_active flag on habits
```

---

## 2. GitHub Copilot Usage Examples

### Example 1: CRUD Endpoint Generation
**File:** `app/routers/habits.py`  
**What Copilot Suggested:**
```python
@router.post("/habits", response_model=HabitOut, status_code=201)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = Habit(name=habit.name, description=habit.description)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit
```

**My Modifications:**
- Added validation for duplicate names
- Added error handling for database failures
- Added pagination support to list endpoints
- Implemented proper error responses

### Example 2: SQLAlchemy Model
**File:** `app/models/habit.py`  
**What Copilot Suggested:** Basic ORM model structure  
**My Enhancements:**
- Added relationship to HabitLog with cascade delete
- Added is_active soft delete flag
- Added created_at timestamp
- Added frequency field with validation

### Example 3: Test Structure
**File:** `tests/test_habits.py`  
**What Copilot Suggested:** Test template  
**My Implementation:**
- Wrote all test logic and assertions
- Created 10 unique test cases
- Ensured 100% pass rate
- Added edge case testing

---

## 3. AI Tool Summary

| Tool | Usage | Contribution |
|------|-------|--------------|
| **ChatGPT** | 10+ conversations | Architecture, debugging, algorithm guidance |
| **GitHub Copilot** | Continuous | Code suggestions, autocomplete, templates |
| **Total Time Saved** | ~30% of development | Mainly on boilerplate and planning |

---

## 4. Declaration of Transparency

✅ All AI usage disclosed  
✅ Original contributions identified  
✅ No code copied without modification  
✅ All suggestions reviewed and validated  
✅ Core logic is entirely original  

---

**Status:** Complete and verified  
**Date:** March 10, 2026
