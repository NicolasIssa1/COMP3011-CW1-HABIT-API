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
- **API Docs:** See `api_documentation.pdf`
- **Technical Report:** See `TECHNICAL_REPORT.pdf`
- **Presentation:** See `PRESENTATION.pptx`

---

## 🚀 Quick Start

### **1. Review Documentation**
```bash
# Technical Report
open TECHNICAL_REPORT.pdf

# API Documentation
open api_documentation.pdf

# GenAI Declaration
open GENAI_DECLARATION.pdf
```

### **2. Run the Code**
```bash
git clone https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API.git
cd COMP3011-CW1-HABIT-API

# Install & run
pip install -r requirements.txt
python -m pytest -v                    # Run tests (10/10 ✅)
python -m uvicorn app.main:app --reload

# View API docs
open http://localhost:8000/docs
```

### **3. Check Git History**
```bash
git log --oneline | head -20
```

---

## ✅ Deliverables Checklist

- [x] Code Repository (GitHub with commit history)
- [x] API Documentation (PDF)
- [x] Technical Report (PDF, 5 pages)
- [x] Presentation Slides (PPTX)
- [x] GenAI Declaration (with evidence)
- [x] Tests (10/10 passing)

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

---

## 🛠️ Tech Stack

- **Framework:** FastAPI 0.129.1
- **ORM:** SQLAlchemy 2.0.46
- **Validation:** Pydantic 2.12.5
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Testing:** Pytest 9.0.2

---

**Status:** ✅ READY FOR SUBMISSION  
**Deadline:** 13 March 2026
