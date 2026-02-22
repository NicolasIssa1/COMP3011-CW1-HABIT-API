# Technical Report Notes (to convert to PDF later)

## Project Overview
- What the API does (habits CRUD, logs, analytics)
- Target users and example use case

## Stack Choice & Justification
- FastAPI + why (OpenAPI docs, speed, clean typing)
- SQLAlchemy + Alembic + why (ORM + migrations)
- SQLite locally + Render deployment choice + tradeoffs

## Architecture
- routers / schemas / models / services structure
- DB session dependency injection (get_db)
- Why separation of concerns matters

## Key Design Decisions
- done-only logs model and why
- unique constraint (habit_id, date) and why 409 is correct
- analytics computed from logs (no redundant storage)

## Testing
- pytest coverage: habits, logs duplicate, analytics

## Deployment
- Render deployment URL
- How to run locally

## Challenges & Lessons Learned
- Alembic autogenerate produced empty file; resolved with manual migration and explained why

## Limitations & Future Work
- auth not implemented (optional)
- working-day streak + bank holidays dataset (optional enhancement)
- stronger validation and more analytics

## GenAI Declaration (summary)
- Tools used
- Purposes (planning, debugging, alternatives exploration)
- What was verified manually
