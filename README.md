# COMP3011 Coursework 1 — Habit & Productivity Analytics API

A data-driven RESTful web API for tracking habits and generating productivity analytics.

## What this project does
This API allows a client to:
- Create, view, update, and delete habits (CRUD)
- Log habit completions as **done-only logs** (a log exists only when a habit is completed)
- Retrieve analytics such as **current/longest streak** and **weekly completion summaries**

## Tech stack (planned / in progress)
- **FastAPI (Python)** — API framework
- **SQL database** — SQLite for local development; PostgreSQL for deployment
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Pytest** — tests
- **OpenAPI/Swagger** — API documentation (exported to PDF in `/docs`)

## Key design choices (verbal justification)
- **Habits vs Logs separation:** habits define what to do; logs record when it was done. This normalised design supports clean analytics.
- **Done-only logs:** completion is an event; missing dates imply “not completed”, simplifying storage and streak computation.
- **Uniqueness constraint:** at most one completion log per habit per date to preserve data integrity.

## Repository structure
- `app/` — application source code
  - `routers/` — API routes (habits, logs, analytics)
  - `schemas/` — request/response models (Pydantic)
  - `models/` — database models (SQLAlchemy)
  - `db/` — database session/engine setup
  - `services/` — business logic (streaks, summaries)
- `migrations/` — Alembic migration files
- `tests/` — automated tests
- `docs/` — API documentation (PDF will be placed here)
- `report/` — technical report (PDF will be placed here, max 5 pages)
- `slides/` — presentation slides used in oral exam
- `ai-logs/` — GenAI declaration and exported conversation logs
- `data/` — dataset files (raw/processed) if used

## How to run (will be updated once the API skeleton is implemented)
> Setup/run instructions will be added after the initial FastAPI + database skeleton is committed.

## Deliverables (for assessment)
- **Code repository:** this GitHub repository with visible commit history
- **API documentation:** `/docs/api_documentation.pdf` (added later)
- **Technical report:** `/report/technical_report.pdf` (added later)
- **Presentation slides:** `/slides/presentation.pptx` (added later)

## GenAI (GREEN assessment)
This is a GREEN assessment. All GenAI tools used will be declared with purpose and examples.
- GenAI declaration and exported logs are stored in: **`/ai-logs`**

## Links (to be filled near submission)
- Deployed API URL: _TBD_
- API docs PDF: _TBD_
- Technical report PDF: _TBD_
- Slides link: _TBD_
