# COMP3011 Coursework 1 — Habit & Productivity Analytics API

A data-driven RESTful web API for tracking habits and generating productivity analytics.

## What this project does
This API allows a client to:
- Create, view, update, and delete habits (CRUD)
- Log habit completions as **done-only logs** (a log exists only when a habit is completed)
- Retrieve analytics such as **current/longest streak** and **weekly completion summaries**

## Tech stack
- **FastAPI (Python)** — API framework
- **SQL database** — SQLite for local development; database configured by `DATABASE_URL` in deployment (Render)
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Pytest** — tests
- **OpenAPI/Swagger** — API documentation (exported to PDF in `/docs`)

## Key design choices (verbal justification)
- **Habits vs Logs separation:** habits define what to do; logs record when it was done. This normalised design supports clean analytics.
- **Done-only logs:** completion is an event; missing dates imply “not completed”, simplifying storage and streak computation.
- **Uniqueness constraint:** at most one completion log per habit per date to preserve data integrity (duplicate → `409 Conflict`).

## Repository structure
- `app/` — application source code
  - `routers/` — API routes (habits, logs, analytics)
  - `schemas/` — request/response models (Pydantic)
  - `models/` — database models (SQLAlchemy)
  - `db/` — database session/engine setup
  - `services/` — business logic (streaks, summaries)
- `migrations/` — Alembic migration files
- `tests/` — automated tests
- `docs/` — API documentation (PDF)
- `report/` — technical report (PDF, max 5 pages)
- `slides/` — presentation slides used in oral exam
- `ai-logs/` — GenAI declaration and exported conversation logs

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (optional) create .env with:
# DATABASE_URL=sqlite:///./dev.db

alembic upgrade head
uvicorn app.main:app --reload

Deliverables (for assessment)

API documentation: docs/api_documentation.pdf

Technical report: report/technical_report.pdf

Presentation slides: slides/presentation.pptx (to be generated near submission)

GenAI declaration + logs: ai-logs/

GenAI (GREEN assessment)

This is a GREEN assessment. All GenAI tools used will be declared with purpose and examples.
GenAI declaration and exported logs are stored in: ai-logs/

Links

Deployed API URL: https://comp3011-cw1-habit-api.onrender.com

Health check: https://comp3011-cw1-habit-api.onrender.com/health

Swagger UI: https://comp3011-cw1-habit-api.onrender.com/docs

OpenAPI JSON: https://comp3011-cw1-habit-api.onrender.com/openapi.json