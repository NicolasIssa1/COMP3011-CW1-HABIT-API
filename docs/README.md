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

- **GitHub Repository:** https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API
- **Live API (Render):** https://comp3011-cw1-habit-api.onrender.com
- **Interactive API Docs:** https://comp3011-cw1-habit-api.onrender.com/docs
- **Health Check:** https://comp3011-cw1-habit-api.onrender.com/health

---

## 🚀 Quick Start

### **Option 1: Test Live API (No Installation Required) ⭐ EASIEST**

Simply visit the live deployment on Render:

**Interactive API Docs (Swagger UI):**
```
https://comp3011-cw1-habit-api.onrender.com/docs
```

**Try it now:**
- Open the Swagger UI link above
- Click on any endpoint (e.g., `GET /habits`)
- Click "Try it out"
- Click "Execute"
- See live responses

No installation, no setup needed! ✅

---

### **Option 2: Run Locally (For Testing & Development)**

```bash
git clone https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API.git
cd COMP3011-CW1-HABIT-API

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload

# Run tests
python -m pytest -v
```

Visit: http://localhost:8000/docs

---

### **Option 3: Review Documentation**
```bash
open TECHNICAL_REPORT.pdf
open api_documentation.pdf
open GENAI_DECLARATION.pdf
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
