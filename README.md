# COMP3011 Coursework 1 — Habit & Productivity Analytics API

A data-driven RESTful web API for tracking habits and generating productivity analytics, with a minimal web front-end and API key authentication.

## What this project does

This API allows a client to:
- Create, view, update, and delete habits (CRUD)
- Log habit completions as **done-only logs** (a log exists only when a habit is completed)
- Retrieve analytics such as **current/longest streak** and **weekly completion summaries**
- Access a **minimal web dashboard** (`/ui/`) to interact with the API
- Authenticate using **API key headers** for security

## Tech stack

- **FastAPI (Python)** — API framework
- **SQL database** — SQLite for local development; database configured by `DATABASE_URL` in deployment (Render)
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Pytest** — tests
- **OpenAPI/Swagger** — API documentation
- **Vanilla HTML/CSS/JS** — Lightweight front-end (no frameworks)

## Key design choices

- **Habits vs Logs separation:** habits define what to do; logs record when it was done. This normalised design supports clean analytics.
- **Done-only logs:** completion is an event; missing dates imply "not completed", simplifying storage and streak computation.
- **Uniqueness constraint:** at most one completion log per habit per date to preserve data integrity (duplicate → `409 Conflict`).
- **API Key authentication:** Simple `X-API-Key` header for security without complex login flows.
- **Minimal front-end:** Vanilla HTML/CSS/JS dashboard for quick demos and UX validation (no React, no build step).

## Repository structure

```
.
├── app/                    # Application source code
│   ├── main.py            # FastAPI app entry point + static file serving
│   ├── routers/           # API routes (habits, logs, analytics)
│   ├── schemas/           # Pydantic request/response models
│   ├── models/            # SQLAlchemy ORM models
│   ├── services/          # Business logic (streak, analytics)
│   ├── db/                # Database session/engine setup
│   ├── core/              # Configuration + security
│   │   ├── config.py      # Settings & API key config
│   │   └── security.py    # API key authentication
│   └── static/            # Front-end assets (HTML, CSS, JS)
│       ├── index.html     # Dashboard single-page app
│       └── app.js         # Dashboard logic
│
├── tests/                 # Automated tests (pytest)
│   ├── test_habits.py
│   ├── test_logs_and_analytics.py
│   └── test_auth.py       # NEW: Authentication tests
│
├── docs/                  # **ALL DELIVERABLES**
│   ├── README.md                          # Documentation index
│   ├── api_documentation.pdf              # Swagger UI export
│   ├── TECHNICAL_REPORT.pdf               # Technical report (5 pages)
│   ├── TECHNICAL_REPORT.md                # Source markdown
│   ├── PRESENTATION.pptx                  # Presentation slides
│   ├── API_AUTHENTICATION.md              # NEW: Auth guide
│   ├── FRONTEND_GUIDE.md                  # NEW: Dashboard guide
│   ├── GENAI_DECLARATION.pdf              # AI usage disclosure
│   ├── GENAI_DECLARATION.md               # AI usage (markdown)
│   ├── GENAI_CONVERSATION_LOGS.md         # Evidence of AI usage
│   ├── openapi.json                       # OpenAPI specification
│   └── SUBMISSION_CHECKLIST.md            # Verification checklist
│
├── migrations/            # Alembic database migrations
├── .gitignore
├── .env.example           # Updated: includes API_KEY
├── requirements.txt       # Dependencies
├── README.md             # This file
└── alembic.ini
```

## Architecture Overview

This project has **three distinct interfaces** that all communicate with the same backend API:

```
Backend API (FastAPI)
    ↓
    ├─ Raw API Routes: /api/habits, /api/analytics/...
    │  └─ Accessed directly for programmatic consumption
    │
    ├─ Swagger/OpenAPI UI: /docs
    │  └─ Interactive documentation for testing endpoint
    │
    └─ Web Dashboard: /ui/
       └─ Single-page app (vanilla HTML/CSS/JS)
          └─ Consumes same /api/... routes under the hood
```

**Key Points:**
- **Backend routes** (prefixed `/api`) are the single source of truth
- **`/docs`** (Swagger UI) lets you test `/api/...` endpoints directly
- **`/ui/`** (dashboard) is a frontend layer that calls the same `/api/...` endpoints
- **Authentication** (API key in `X-API-Key` header) applies to all three

## Run locally

### 1. Setup

```bash
git clone https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API.git
cd COMP3011-CW1-HABIT-API

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment (optional)

Create `.env`:
```
DATABASE_URL=sqlite:///./dev.db
ENVIRONMENT=development
API_KEY=test-api-key-12345
```

### 3. Initialize & run

```bash
alembic upgrade head
python -m uvicorn app.main:app --reload
```

### 4. Access the three interfaces

**a) Web Dashboard (recommended for quick demo):**
```
http://localhost:8000/ui/
```
- Default API key: `test-api-key-12345` (pre-filled)
- Create, list, delete habits through the UI
- All actions call `/api/...` routes internally

**b) Interactive API Docs (for endpoint testing):**
```
http://localhost:8000/docs
```
- Swagger UI auto-generated from FastAPI
- Test each endpoint directly with custom payloads
- Same authentication required (X-API-Key header)

**c) Raw API (for programmatic access):**
```
http://localhost:8000/api/habits
```
Example with curl:
```bash
curl -H "X-API-Key: test-api-key-12345" \
  http://localhost:8000/api/habits
```

**d) Health Check:**
```
http://localhost:8000/health
```
(no authentication required)

### 5. Run tests

```bash
python -m pytest -v
```

This validates all 14 tests (CRUD, auth, analytics) ✅

## How It Works: Frontend → Backend

When you use the **`/ui/` dashboard**, here's what happens behind the scenes:

### Example: Create a Habit

**UI Form:**
```
User fills form (name, description, frequency) → Clicks "Create Habit"
```

**Frontend Code (app.js):**
```javascript
// Calls backend API route
POST /api/habits
Body: { name, description, frequency }
Headers: { X-API-Key: test-api-key-12345 }
```

**Backend (routers/habits.py):**
```python
@router.post("/habits")  # Mounted at /api prefix
def create_habit(habit: HabitCreate, api_key: str = Depends(verify_api_key)):
    # Create and return habit
```

**Response:**
```json
{ "id": 1, "name": "Morning Exercise", ... }
```

**UI Update:**
```
Habit appears in the list, form clears, success message shown
```

### All Frontend Endpoints

| Feature | Frontend Call | Backend Endpoint | Mounted At |
|---------|---------------|------------------|------------|
| List habits | GET `/api/habits` | `routers/habits.py` | `/api` |
| Create habit | POST `/api/habits` | `routers/habits.py` | `/api` |
| Delete habit | DELETE `/api/habits/{id}` | `routers/habits.py` | `/api` |
| Log completion | POST `/api/habits/{id}/logs` | `routers/logs.py` | `/api` |
| Get streak | GET `/api/habits/{id}/streak` | `routers/analytics.py` | `/api` |
| Weekly summary | GET `/api/analytics/weekly-summary` | `routers/analytics.py` | `/api` |

**All require:** `X-API-Key: test-api-key-12345` header

## Quick Demo (5 minutes)

1. **Open dashboard:** http://localhost:8000/ui/
2. **Default API key is pre-filled:** `test-api-key-12345`
3. **Create a habit:** Fill form → Click "Create Habit"
4. **Mark it done:** Click "✓ Mark Done Today"
5. **View streak:** Click "📊 Stats" → See current streak
6. **Try another:** Create & complete multiple habits
7. **Or test directly:** Open http://localhost:8000/docs and try endpoints

Both `/ui/` and `/docs` call the same backend `/api/...` routes ✅

## API Endpoints

### Authentication

All `/api/...` endpoints require the `X-API-Key` header:

```bash
curl -H "X-API-Key: test-api-key-12345" http://localhost:8000/api/habits
```

**Public endpoints** (no auth required):
- `GET /` — API info
- `GET /health` — Health check

**Authenticated endpoints** (require `X-API-Key: test-api-key-12345`):
- All `/api/habits` routes
- All `/api/analytics` routes

### Habits

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/habits` | Create habit |
| GET | `/api/habits` | List habits (paginated, filterable) |
| GET | `/api/habits/{id}` | Get habit details |
| PATCH | `/api/habits/{id}` | Update habit |
| DELETE | `/api/habits/{id}` | Delete habit |

### Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/habits/{id}/logs` | Log completion |
| GET | `/api/habits/{id}/logs` | List logs (date filterable) |
| DELETE | `/api/habits/{id}/logs/{log_id}` | Delete log |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/habits/{id}/streak` | Get streak stats (current, longest, total) |
| GET | `/api/analytics/weekly-summary` | Weekly completion summary |

**Full details:** See `/docs/api_documentation.pdf`

## Testing

✅ **14/14 tests passing**

```bash
python -m pytest -v
```

Tests cover:
- ✅ CRUD operations (habits, logs)
- ✅ Streak calculation
- ✅ Weekly analytics
- ✅ API key authentication (missing, invalid, valid)
- ✅ Error handling (404, 409, 401, 403)
- ✅ Frontend consumption of `/api/...` routes

## Deployment

**Live:** https://comp3011-cw1-habit-api.onrender.com

**Access points:**
- **Dashboard:** https://comp3011-cw1-habit-api.onrender.com/ui/
- **API Docs:** https://comp3011-cw1-habit-api.onrender.com/docs
- **Health Check:** https://comp3011-cw1-habit-api.onrender.com/health

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

### Core API
✅ Full CRUD (Habits)  
✅ Done-only logs with uniqueness  
✅ Streak tracking (current & longest)  
✅ Weekly analytics & summaries  
✅ Pagination & filtering  
✅ Error handling & validation  
✅ Type safety (Pydantic + SQLAlchemy)  

### Security & Features (NEW)
✅ **API Key authentication** (`X-API-Key` header)  
✅ **Minimal web dashboard** (`/ui/`)  
✅ Responsive design (desktop, tablet, mobile)  
✅ Real-time search & filtering  
✅ Vanilla JS (no frameworks, no build step)  
✅ **13 tests** with 100% pass rate  

## Documentation

- **API Guide:** [API_AUTHENTICATION.md](docs/API_AUTHENTICATION.md)
- **Dashboard Guide:** [FRONTEND_GUIDE.md](docs/FRONTEND_GUIDE.md)
- **Technical Report:** [TECHNICAL_REPORT.pdf](docs/TECHNICAL_REPORT.pdf)
- **API Docs:** [Swagger UI](http://localhost:8000/docs) / [api_documentation.pdf](docs/api_documentation.pdf)
- **Slides:** [PRESENTATION.pptx](docs/PRESENTATION.pptx)
- **Index:** [docs/README.md](docs/README.md)

## Contact

**Author:** Nicolas Issa  
**Module:** COMP3011 — Web Services and Web Data  
**Institution:** University of Leeds, School of Computer Science  

---

**Status:** ✅ READY  
**Deadline:** 13 March 2026  
**Oral Exam:** 23-27 March 2026
