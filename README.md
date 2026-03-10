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
- **OpenAPI/Swagger** — API documentation

## Key design choices

- **Habits vs Logs separation:** habits define what to do; logs record when it was done. This normalised design supports clean analytics.
- **Done-only logs:** completion is an event; missing dates imply "not completed", simplifying storage and streak computation.
- **Uniqueness constraint:** at most one completion log per habit per date to preserve data integrity (duplicate → `409 Conflict`).

## Repository structure

```
.
├── app/                    # Application source code
│   ├── main.py            # FastAPI app entry point
│   ├── routers/           # API routes (habits, logs, analytics)
│   ├── schemas/           # Pydantic request/response models
│   ├── models/            # SQLAlchemy ORM models
│   ├── services/          # Business logic (streak, analytics)
│   ├── db/                # Database session/engine setup
│   └── core/              # Configuration
│
├── tests/                 # Automated tests (pytest)
│
├── docs/                  # **ALL DELIVERABLES**
│   ├── README.md                          # Documentation index
│   ├── api_documentation.pdf              # Swagger UI export
│   ├── TECHNICAL_REPORT.pdf               # Technical report (5 pages)
│   ├── TECHNICAL_REPORT.md                # Source markdown
│   ├── PRESENTATION.pptx                  # Presentation slides
│   ├── GENAI_DECLARATION.pdf              # AI usage disclosure
│   ├── GENAI_DECLARATION.md               # AI usage (markdown)
│   ├── GENAI_CONVERSATION_LOGS.md         # Evidence of AI usage
│   ├── openapi.json                       # OpenAPI specification
│   └── SUBMISSION_CHECKLIST.md            # Verification checklist
│
├── migrations/            # Alembic database migrations
├── .gitignore
├── .env.example
├── requirements.txt       # Dependencies
├── README.md             # This file
└── alembic.ini
```

## Run locally

### 1. Setup

```bash
git clone https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API.git
cd COMP3011-CW1-HABIT-API

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure database (optional)

Create `.env`:
```
DATABASE_URL=sqlite:///./dev.db
```

### 3. Initialize & run

```bash
alembic upgrade head
python -m uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

### 4. Run tests

```bash
python -m pytest -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/habits` | Create habit |
| GET | `/habits` | List habits (paginated) |
| GET | `/habits/{id}` | Get habit details |
| PATCH | `/habits/{id}` | Update habit |
| DELETE | `/habits/{id}` | Delete habit |
| POST | `/habits/{id}/logs` | Log completion |
| GET | `/habits/{id}/logs` | List logs |
| DELETE | `/habits/{id}/logs/{log_id}` | Delete log |
| GET | `/habits/{id}/streak` | Get streak stats |
| GET | `/analytics/weekly-summary` | Weekly summary |

**Full details:** See `/docs/api_documentation.pdf`

## Testing

✅ **10/10 tests passing**

```bash
python -m pytest -v
```

## Deployment

**Live:** https://comp3011-cw1-habit-api.onrender.com  
**Docs:** https://comp3011-cw1-habit-api.onrender.com/docs  
**Health:** https://comp3011-cw1-habit-api.onrender.com/health

## Assessment Deliverables

All materials in `/docs/` ✅

### Required (Pass/Fail)
- ✅ Code Repository (GitHub with history)
- ✅ API Documentation (`api_documentation.pdf`)
- ✅ Technical Report (`TECHNICAL_REPORT.pdf`, 5 pages)
- ✅ GenAI Declaration (`GENAI_DECLARATION.pdf`)

### Presentation
- ✅ Slides (`PRESENTATION.pptx`, 13 slides)
- 5 min presentation + 5 min Q&A

## GenAI Usage (GREEN Assessment)

**Declared Tools:**
- ✅ ChatGPT (GPT-4) — Architecture, debugging, algorithm guidance
- ✅ GitHub Copilot — Code templates, suggestions

**Evidence:** `/docs/GENAI_DECLARATION.pdf` + `/docs/GENAI_CONVERSATION_LOGS.md`

**Integrity:** Original logic, testing, and architecture decisions maintained. All AI suggestions reviewed and modified.

## Features

✅ Full CRUD (Habits)  
✅ Done-only logs  
✅ Streak tracking  
✅ Weekly analytics  
✅ Pagination & filtering  
✅ Error handling  
✅ Type safety  
✅ 100% test pass rate  

## Documentation

- **Technical Report:** `/docs/TECHNICAL_REPORT.pdf`
- **API Docs:** `/docs/api_documentation.pdf`
- **Slides:** `/docs/PRESENTATION.pptx`
- **Index:** `/docs/README.md`

## Contact

**Author:** Nicolas Issa  
**Module:** COMP3011 — Web Services and Web Data  
**Institution:** University of Leeds, School of Computer Science  

---

**Status:** ✅ READY  
**Deadline:** 13 March 2026  
**Oral Exam:** 23-27 March 2026
