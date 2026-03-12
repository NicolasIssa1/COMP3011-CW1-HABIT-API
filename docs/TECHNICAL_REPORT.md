# Technical Report: Habit & Productivity Analytics API

**Module:** COMP3011 — Web Services & Web Data (Coursework 1)
**Author:** Nicolas Issa
**Date:** March 2026
**Repository:** [github.com/NicolasIssa1/COMP3011-CW1-HABIT-API](https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API)
**Deployed URL:** [comp3011-cw1-habit-api.onrender.com](https://comp3011-cw1-habit-api.onrender.com)

---

## 1. Overview

The Habit & Productivity Analytics API is a RESTful web service for tracking habits, logging completions, and computing productivity analytics (streaks and weekly summaries). It is built with FastAPI (Python 3.12), uses SQLAlchemy as the ORM with SQLite for local development, and is deployed on Render.

The project also includes a lightweight vanilla-JS web dashboard served at `/ui/`, API key authentication on all data endpoints, and automated tests via pytest.

---

## 2. Technology Stack & Justification

| Component | Choice | Why |
|-----------|--------|-----|
| Framework | FastAPI | Auto-generates OpenAPI/Swagger docs at `/docs`; built-in Pydantic request validation; minimal boilerplate |
| ORM | SQLAlchemy | Database-agnostic models; parameterised queries prevent SQL injection; pairs with Alembic for migrations |
| Migrations | Alembic | Version-controlled schema changes; one migration file creates both tables |
| Database | SQLite | Zero-config for development; `DATABASE_URL` env var allows switching to PostgreSQL in production |
| Auth | X-API-Key header | Simple to implement and test; suitable for a single-service API without user accounts |
| Frontend | Vanilla HTML/CSS/JS | No build step; served as static files via FastAPI's `StaticFiles` mount at `/ui/` |
| Testing | pytest + FastAPI TestClient | In-process testing; no external server required |

---

## 3. Architecture

```
Client (browser / curl / Swagger UI)
  │
  ├─ /api/habits, /api/habits/{id}/logs, /api/analytics/...
  │     ↓
  │   FastAPI routers (habits.py, logs.py, analytics.py)
  │     ↓  Depends(verify_api_key)  ← X-API-Key header check
  │   Service layer (streak_service.py)
  │     ↓
  │   SQLAlchemy ORM  →  SQLite (dev.db)
  │
  ├─ /docs           → Swagger UI (auto-generated)
  ├─ /ui/            → Static dashboard (index.html, app.js, styles.css)
  └─ /health         → Public health-check endpoint
```

Three routers are registered under the `/api` prefix. A `verify_api_key` dependency (in `app/core/security.py`) protects every data endpoint: missing key → 401; wrong key → 403. The `/health` and `/` root endpoints are public. CORS middleware is enabled to allow cross-origin requests from the `/ui/` dashboard. A global exception handler catches unhandled errors and returns a JSON 500 response without exposing stack traces.

---

## 4. Data Model

**Habit** — `habits` table: `id` (PK), `name` (VARCHAR 120), `description` (VARCHAR 500, nullable), `frequency` (VARCHAR 20, default "daily"), `is_active` (BOOLEAN, default true), `created_at` (DATETIME).

**HabitLog** — `habit_logs` table: `id` (PK), `habit_id` (FK → habits, CASCADE delete), `date` (DATE), `notes` (VARCHAR 500, nullable). A **unique constraint** on `(habit_id, date)` enforces at most one log per habit per day; violations return **409 Conflict**.

Design rationale:

- **Done-only logging:** A log exists only when a habit is completed. Missing dates implicitly mean "not done", which keeps storage lean and simplifies streak computation.
- **DB-level uniqueness:** Duplicate prevention is enforced by the database constraint, not application code, ensuring integrity regardless of client.
- **Cascade delete:** Removing a habit automatically removes its logs via `ondelete="CASCADE"` on the foreign key.

---

## 5. API Endpoints & Status Codes

All `/api/` endpoints require the `X-API-Key` header.

| Method | Endpoint | Success | Error codes |
|--------|----------|---------|-------------|
| POST | `/api/habits` | 201 | 401, 403 |
| GET | `/api/habits` | 200 | 401, 403 |
| GET | `/api/habits/{id}` | 200 | 404, 401, 403 |
| PATCH | `/api/habits/{id}` | 200 | 404, 401, 403 |
| DELETE | `/api/habits/{id}` | 204 | 404, 401, 403 |
| POST | `/api/habits/{id}/logs` | 201 | 409, 404, 401, 403 |
| GET | `/api/habits/{id}/logs` | 200 | 404, 401, 403 |
| DELETE | `/api/habits/{id}/logs/{log_id}` | 204 | 404, 401, 403 |
| GET | `/api/habits/{id}/streak` | 200 | 404, 401, 403 |
| GET | `/api/analytics/weekly-summary?week=` | 200 | 400, 422, 401, 403 |
| GET | `/health` | 200 | — |
| GET | `/` | 200 | — |

Notable behaviours:

- **List endpoints** support `skip` and `limit` query parameters for pagination (default 20, max 100). `GET /api/habits` also accepts `is_active` and `frequency` filters.
- **Weekly summary** accepts `week` in `YYYY-WW` or `YYYY-Www` format (e.g. `2026-09` or `2026-W09`), validated by regex. Invalid format → 400; invalid ISO week number → 400; missing param → 422.
- **Streak endpoint** returns `current_streak`, `longest_streak`, and `total_completions`. The algorithm iterates backwards from today counting consecutive dates present in the log set.

---

## 6. Testing

The test suite uses pytest with FastAPI's `TestClient`. A custom `AuthenticatedTestClient` in `conftest.py` automatically injects the `X-API-Key` header into every request.

**14 tests across 3 files — all passing:**

| File | Tests | What is covered |
|------|-------|-----------------|
| `test_auth.py` | 4 | 401 (no key), 403 (bad key), 200 (valid key), health endpoint |
| `test_habits.py` | 3 | Create + list, PATCH missing → 404, delete lifecycle → 404 |
| `test_logs_and_analytics.py` | 7 | Duplicate log → 409, streak + weekly summary, invalid week format → 400, invalid week number → 400, delete missing log → 404, log for missing habit → 404, missing week param → 422 |

Tests are run with `python -m pytest -v` and verify every documented HTTP status code the API can return.

---

## 7. Deployment

The API is deployed on **Render** (free tier) with auto-deploy from the `main` branch. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

**Deployment incident:** After initial deploy, `GET /api/habits` returned 500 with `"no such table: habits"`. The SQLite database file was empty because Alembic migrations do not run automatically on Render.

**Fix:** Added `Base.metadata.create_all(bind=engine)` inside the FastAPI `lifespan` context manager in `app/main.py`. This is idempotent — it only creates tables that do not already exist. Commits `871826a` through `02406d5` document the debugging and resolution.

Environment variables used: `DATABASE_URL` (connection string), `ENVIRONMENT` (development/production), `API_KEY` (authentication key).

---

## 8. Limitations & Future Work

- **Single API key:** All clients share one key. A future version could add per-user JWT authentication.
- **SQLite in production:** Render's ephemeral filesystem means data does not persist across deploys. Switching to a managed PostgreSQL instance would solve this.
- **No coverage report:** Tests pass but formal coverage metrics have not been generated.
- **Frontend is supplementary:** The `/ui/` dashboard demonstrates the API but is not a full-featured application.
- **Future enhancements:** User accounts, habit categories/tags, data visualisation charts, rate limiting.

---

## 9. GenAI Usage

Generative AI tools were used during development in accordance with COMP3011's GREEN GenAI policy:

- **GitHub Copilot:** Code suggestions for CRUD endpoint boilerplate and SQLAlchemy model definitions (~60% acceptance rate; the rest were modified or rejected).
- **ChatGPT (GPT-4):** Architecture guidance, streak algorithm pseudocode, and debugging consultation.

Estimated AI contribution: ~30% of development time, primarily on boilerplate and planning. All AI-generated code was reviewed, tested, and modified.

**Evidence files:**

- Declaration: `docs/GENAI_DECLARATION.md` and `docs/GENAI_DECLARATION.pdf`
- Conversation logs: `docs/GENAI_CONVERSATION_LOGS.md` (3 ChatGPT + 3 Copilot examples)

---

## 10. Deliverables Summary

| Deliverable | Location |
|-------------|----------|
| Source code | `app/`, `tests/`, `migrations/` |
| API documentation (Swagger export) | `docs/api_documentation.pdf` |
| Technical report | `docs/TECHNICAL_REPORT.pdf` |
| Presentation slides | `docs/PRESENTATION.pptx` |
| GenAI declaration | `docs/GENAI_DECLARATION.pdf` |
| GenAI conversation logs | `docs/GENAI_CONVERSATION_LOGS.md` |
| OpenAPI specification | `docs/openapi.json` |
| Live deployment | [comp3011-cw1-habit-api.onrender.com](https://comp3011-cw1-habit-api.onrender.com) |

