# Documentation - Habit & Productivity Analytics API

**Project:** COMP3011 Coursework 1 - Individual Web Services API Development  
**Author:** Nicolas Issa  
**Submission Date:** March 13, 2026  
**Deadline:** 13 March 2026

---

## 📑 Contents

This folder contains all required deliverables for the COMP3011 coursework submission:

### **1. API Documentation**
- **File:** `api_documentation.pdf`
- **Description:** Generated from FastAPI Swagger UI
- **Contents:** All 12 endpoints, examples, status codes, error handling

### **2. Technical Report**
- **File:** `TECHNICAL_REPORT.pdf` (5 pages)
- **Contents:** Architecture, design choices, testing, limitations, GenAI declaration

### **3. Presentation Slides**
- **File:** `PRESENTATION.pptx` (10 slides)
- **Sections:** Overview, stack, architecture, features, security, testing, roadmap

### **4. GenAI Declaration**
- **Files:** `GENAI_DECLARATION.pdf` & `GENAI_DECLARATION.md`
- **Purpose:** Transparent disclosure of ChatGPT & GitHub Copilot usage

### **5. GenAI Conversation Logs**
- **File:** `GENAI_CONVERSATION_LOGS.md`
- **Purpose:** Supplementary evidence of AI tool usage

### **6. OpenAPI Specification**
- **File:** `openapi.json`
- **Use:** Import into Postman, Swagger Editor, or similar tools

### **7. Supplementary Guides**
- `API_AUTHENTICATION.md` — How X-API-Key authentication works
- `FRONTEND_GUIDE.md` — How the `/ui/` dashboard works
- `IMPLEMENTATION_GUIDE.md` — Implementation notes
- `SUBMISSION_CHECKLIST.md` — Pre-submission verification checklist

---

## 🔗 Quick Links

### Local Development (after running `python -m uvicorn app.main:app --reload`)
- **Web Dashboard:** http://localhost:8000/ui/ (frontend UI)
- **Swagger Docs:** http://localhost:8000/docs (API testing)
- **Raw API:** http://localhost:8000/api/habits (programmatic access)
- **Health Check:** http://localhost:8000/health (no auth needed)

### Live Deployment on Render
- **GitHub Repository:** https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API
- **Live API:** https://comp3011-cw1-habit-api.onrender.com
- **Web Dashboard:** https://comp3011-cw1-habit-api.onrender.com/ui/
- **Swagger Docs:** https://comp3011-cw1-habit-api.onrender.com/docs
- **Health Check:** https://comp3011-cw1-habit-api.onrender.com/health

---

## 🚀 Quick Start

### **Option 1: Web Dashboard (Recommended for Quick Demo) ⭐**

Open the dashboard at `/ui/` — no installation needed:

- **Local:** http://localhost:8000/ui/
- **Live:** https://comp3011-cw1-habit-api.onrender.com/ui/

Default API key `test-api-key-12345` is pre-filled. You can create, list, and delete habits, log completions, and view streak analytics through the UI.

### **Option 2: Swagger Docs (For Endpoint Testing)**

Open `/docs` to test each endpoint interactively:

- **Local:** http://localhost:8000/docs
- **Live:** https://comp3011-cw1-habit-api.onrender.com/docs

Click any endpoint → "Try it out" → fill parameters → "Execute" → see response.

### **Option 3: Run Locally**

```bash
git clone https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API.git
cd COMP3011-CW1-HABIT-API

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload
```

Then access:
- **Dashboard:** http://localhost:8000/ui/
- **Swagger Docs:** http://localhost:8000/docs
- **Raw API:** http://localhost:8000/api/habits

```bash
# Run tests (14/14 passing)
python -m pytest -v
```

---

## ✅ Deliverables Checklist

- [x] Code Repository (GitHub with commit history)
- [x] API Documentation (`api_documentation.pdf`)
- [x] Technical Report (`TECHNICAL_REPORT.pdf`, 5 pages)
- [x] Presentation Slides (`PRESENTATION.pptx`, 10 slides)
- [x] GenAI Declaration (`GENAI_DECLARATION.pdf` + evidence logs)
- [x] Tests (14/14 passing)
- [x] Live Deployment (Render)

---

## 📊 Project Summary

| Item | Status |
|------|--------|
| **API Endpoints** | 12 (CRUD + Analytics) |
| **Authentication** | X-API-Key header on all `/api/` routes |
| **Tests Passing** | 14/14 ✅ |
| **Documentation** | Complete |
| **GenAI Usage** | Fully disclosed |
| **Live Deployment** | ✅ Render |

---

## 🛠️ Tech Stack

- **Framework:** FastAPI 0.129.1
- **ORM:** SQLAlchemy 2.0.46
- **Validation:** Pydantic 2.12.5
- **Database:** SQLite locally; configurable via `DATABASE_URL` env var
- **Testing:** Pytest 9.0.2
- **Hosting:** Render (free tier, auto-deploy from `main`)

---

## 🌐 Deployment

**Live URL:** https://comp3011-cw1-habit-api.onrender.com

- ✅ Hosted on Render (free tier)
- ✅ Auto-deployed from GitHub `main` branch
- ✅ HTTPS enabled
- ✅ Health checks operational
- ✅ Database configured via `DATABASE_URL` environment variable

---

**Status:** ✅ READY FOR SUBMISSION  
**Deadline:** 13 March 2026
