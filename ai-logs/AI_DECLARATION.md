# Generative AI Declaration (COMP3011 Coursework 1)

This repository contains a Habit & Productivity Analytics REST API built with FastAPI, SQLAlchemy, Alembic, and pytest, deployed on Render.

This is a GREEN light GenAI assessment. I used GenAI tools as a productivity and learning assistant while ensuring that:
- I remained responsible for all design decisions and final code.
- I validated outputs through documentation, testing, and runtime verification.
- I kept evidence logs to demonstrate methodological usage.

---

## 1) GenAI tools used

### Tool A — ChatGPT (OpenAI)
**Usage:** planning, design discussion, code suggestions, debugging support, test strategy.

### Tool B — [ADD if used: GitHub Copilot / Copilot Chat]
**Usage:** inline code suggestions during development; minor refactors and boilerplate completion.

### Tool C — [ADD if used: Microsoft Copilot / Claude / Gemini / Perplexity]
**Usage:** [briefly state what for, e.g., alternative explanations, documentation phrasing].

> If a tool was installed but not used, it is not listed.

---

## 2) Purposes and how GenAI was used (methodological workflow)

I used GenAI in a structured way across these stages:

1. **Architecture & design exploration**
   - Asked for multiple architectural options (e.g., folder structure / router-service-repo layering).
   - Compared trade-offs (maintainability, testability, clarity).
   - Selected and implemented the final approach.

2. **REST API design & schema shaping**
   - Generated candidate endpoint sets and refined them into RESTful resource naming.
   - Confirmed request/response schemas and status codes.
   - Considered edge cases (validation errors, duplicates, not-found).

3. **Implementation assistance (non-blind use)**
   - Used GenAI for examples/patterns (FastAPI dependencies, SQLAlchemy session patterns).
   - I integrated these patterns into my codebase with project-specific adjustments.

4. **Debugging and iteration**
   - Described concrete errors and logs (tracebacks, failing tests).
   - Evaluated proposed fixes and applied only the ones consistent with my architecture.
   - Re-ran pytest and/or exercised endpoints to confirm the fix.

5. **Testing & quality**
   - Used GenAI to propose a test plan (happy path + negative tests).
   - Wrote/adapted tests to my actual API behaviours and database setup.
   - Confirmed test outcomes using `pytest`.

6. **Deployment support**
   - Used GenAI for deployment checklists (Render settings, env vars, Alembic migrations).
   - Verified the deployed API using real requests (status codes + JSON responses).

---

## 3) Verification steps (how I ensured correctness)

I did not accept GenAI output without checking. My verification included:

- **Automated tests:** ran `pytest` and ensured tests passed after changes.
- **Local runtime checks:** started the API locally and tested endpoints (Swagger UI / curl / HTTP client).
- **Database checks:** verified migrations and data persistence (Alembic upgrade + CRUD operations).
- **Deployed checks:** verified the Render deployment by calling live endpoints and checking responses.
- **Documentation consistency:** ensured the implemented behaviour matches `docs/api_documentation.pdf`.

---

## 4) What I wrote myself vs what GenAI assisted with

### Written primarily by me
- Overall project idea and feature selection (Habit & Productivity Analytics API).
- Final architecture decisions and repository structure.
- Final implementations after adaptation (routers, models, schemas, services).
- Database design decisions and migration choices.
- Test coverage decisions (what behaviours to test and why).
- Technical report and API documentation content/structure (with optional proofreading assistance).

### GenAI-assisted (with human selection/adaptation)
- Alternative architecture suggestions and trade-off discussion.
- Example patterns/snippets (FastAPI dependency injection, SQLAlchemy session usage).
- Debugging hypotheses and potential fixes (validated by tests).
- Suggestions for additional tests and error handling improvements.
- Deployment checklists and “what to verify” steps.

---

## 5) Evidence: exported conversation logs included in this repo

All evidence logs are stored in: `ai-logs/logs/`

| Log file | What it demonstrates | Why it matters |
|---|---|---|
| `01_architecture_alternatives.[pdf/md]` | multiple design options + trade-offs + final decision | shows non-arbitrary, method-based use |
| `02_api_design_iteration.[pdf/md]` | REST endpoints, schemas, status codes, edge cases | shows careful API design reasoning |
| `03_debugging_verification_loop.[pdf/md]` | real error → GenAI suggestions → pytest/curl verification | shows validation + iteration |
| `04_testing_strategy_negative_tests.[pdf/md]` | test plan + negative tests + adaptations | shows quality-focused AI usage |
| `05_deployment_production_checks.[pdf/md]` | Render deployment + env vars + live verification | shows real-world engineering thinking |

(If fewer logs are submitted, the remaining ones were selected to cover the above stages end-to-end.)

---

## 6) Usage level justification (Good / Very Good / Excellent)

My GenAI use is **methodological** rather than arbitrary: I used it to explore alternatives, compare trade-offs, and iterate through a verify-and-improve loop (tests + runtime checks) before accepting changes. The attached logs show decision-making, evaluation, and validation steps, demonstrating medium-to-high level use aligned with the “Good/Very Good/Excellent” descriptors in the COMP3011 brief. 

---

## 7) Notes on academic integrity

- GenAI outputs were treated as suggestions, not authoritative sources.
- Final responsibility for correctness, security, and design decisions remains mine.
- All deliverables (code, documentation, testing, deployment) reflect my understanding and were verified by execution.