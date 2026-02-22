# COMP3011 Coursework 1 — Technical Report
**Project:** Habit & Productivity Analytics API  
**Student:** Nicolas Issa  
**Repository:** https://github.com/NicolasIssa1/COMP3011-CW1-HABIT-API  
**Deployed URL:** https://comp3011-cw1-habit-api.onrender.com  

## 1. Overview
Briefly describe what the API does and the main features (habits CRUD, logs, analytics).

## 2. Technology Stack and Justification
- FastAPI: why chosen (speed, OpenAPI/Swagger, typing)
- SQLAlchemy + Alembic: why (ORM + migrations, maintainable schema evolution)
- SQLite (local) + Render (deployment): trade-offs and rationale

## 3. Architecture and Design
Explain the repository structure:
- routers / schemas / models / services
- DB session dependency (get_db)
Key design choices:
- done-only logs model
- unique constraint (habit_id, date) and 409 Conflict
- analytics computed from logs (no redundant storage)

## 4. API Functionality
Summarise endpoints and behaviour:
- Habits CRUD
- Logs endpoints
- Analytics endpoints (streak, weekly summary)
Mention status codes used and error handling (404/409).

## 5. Testing Approach
Summarise pytest coverage and why these tests matter (core CRUD, duplicates, analytics).

## 6. Deployment
How it is deployed, how to run locally, and what URLs are used (/health, /docs).

## 7. Challenges, Limitations, and Future Work
- Challenge: Alembic autogenerate issue and fix
- Limitations: e.g., no auth (yet), limited analytics
- Future work: bank holidays working-day streak, auth, more validation

## 8. Generative AI Declaration and Usage Analysis
List GenAI tools used, how they were used (planning/debugging/alternatives), what you verified manually, and reference exported logs in `/ai-logs/`.

## References
List any dataset sources, libraries, and external tutorials used (with links).
