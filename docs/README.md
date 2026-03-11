# Documentation - Habit & Productivity Analytics API

**Project:** COMP3011 Coursework 1 - Individual Web Services API Development  
**Author:** Nicolas Issa  
**Submission Date:** March 10, 2026  
**Deadline:** 13 March 2026

---

## 📑 Contents

This folder contains all required deliverables for the COMP3011 coursework submission:

### **1. API Documentation**
- **File:** `api_documentation.pdf`
- **Description:** Generated from FastAPI Swagger UI
- **Contents:** All 12 endpoints, examples, status codes, error handling

### **2. Technical Report**
- **File:** `TECHNICAL_REPORT.pdf` (5 pages max)
- **Contents:** Architecture, design choices, testing, limitations, GenAI declaration

### **3. Presentation Slides**
- **File:** `PRESENTATION.pptx` (13 slides)
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

## 🚀 Quick Start (Three Options)

### **Option 1: Web Dashboard (Recommended for Quick Demo) ⭐**

The **graphical dashboard** at `/ui/` is the most user-friendly way to interact:

**Local:**
```
http://localhost:8000/ui/
```

**Live:**
```
https://comp3011-cw1-habit-api.onrender.com/ui/
```

**What you get:**
- ✅ Beautiful, responsive interface
- ✅ Create, list, delete habits with buttons
- ✅ Real-time search and filtering
- ✅ View habit streaks and analytics
- ✅ Default API key pre-filled: `test-api-key-12345`
- ✅ All requests go to `/api/...` routes under the hood

**No installation needed** — just open the link!

---

### **Option 2: Interactive API Docs (For Endpoint Testing)**

The **Swagger UI** at `/docs` lets you test each endpoint directly:

**Local:**
```
http://localhost:8000/docs
```

**Live:**
```
https://comp3011-cw1-habit-api.onrender.com/docs
```

**What you get:**
- ✅ Auto-generated OpenAPI documentation
- ✅ "Try it out" button for each endpoint
- ✅ Fill in request body, see response
- ✅ See all endpoint details, parameters, schemas
- ✅ Test authentication and error responses

**How to use:**
1. Open the Swagger link above
2. Click on any endpoint (e.g., `GET /api/habits`)
3. Click "Try it out"
4. Enter request body if needed
5. Click "Execute"
6. See live response

---

### **Option 3: Run Locally (For Development & Testing)**

Clone and run the full application locally:

```bash
git clone https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API.git
cd COMP3011-CW1-HABIT-API

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload
```

Then access all three interfaces:
- **Dashboard:** http://localhost:8000/ui/
- **Swagger Docs:** http://localhost:8000/docs
- **Raw API:** http://localhost:8000/api/habits

```bash
# Run tests
python -m pytest -v
```

---

### **All Three Interfaces Use The Same API**

```
┌─────────────────────────────────────┐
│   Backend API (/api/...routes)      │
│  - All business logic here           │
│  - Database operations               │
│  - Authentication required           │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┬───────────┐
       │                │           │
   ┌───▼──────┐  ┌──────▼──┐  ┌───▼────┐
   │  /docs   │  │  /ui/   │  │ /api/  │
   │ (Swagger)│  │(Frontend)│  │(Raw)   │
   └──────────┘  └─────────┘  └────────┘

All three access the exact same backend endpoints.
Authentication and business logic are identical.
```

---

## ✅ Deliverables Checklist

- [x] Code Repository (GitHub with commit history)
- [x] API Documentation (PDF)
- [x] Technical Report (PDF, 5 pages)
- [x] Presentation Slides (PPTX)
- [x] GenAI Declaration (with evidence)
- [x] Tests (10/10 passing)
- [x] Live Deployment (Render)

---

## 📊 Project Summary

| Item | Status |
|------|--------|
| **API Endpoints** | 12 (CRUD + Analytics) |
| **Tests Passing** | 10/10 ✅ |
| **Documentation** | Complete |
| **Git Commits** | 20+ with history |
| **Code Quality** | Clean, modular |
| **GenAI Usage** | Fully disclosed |
| **Live Deployment** | ✅ Render |

---

## 🛠️ Tech Stack

- **Framework:** FastAPI 0.129.1
- **ORM:** SQLAlchemy 2.0.46
- **Validation:** Pydantic 2.12.5
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Testing:** Pytest 9.0.2
- **Hosting:** Render (PaaS)

---

## 🌐 Deployment

**Live URL:** https://comp3011-cw1-habit-api.onrender.com

- ✅ Hosted on Render
- ✅ PostgreSQL database
- ✅ HTTPS enabled
- ✅ Auto-deployed from GitHub
- ✅ Health checks operational

---

**Status:** ✅ READY FOR SUBMISSION  
**Deadline:** 13 March 2026  
**Deployment:** ✅ LIVE
