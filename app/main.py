import os

from fastapi import FastAPI
from alembic import command
from alembic.config import Config

from app.routers.habits import router as habits_router
from app.routers.logs import router as logs_router
from app.routers.analytics import router as analytics_router


def run_migrations_on_startup() -> None:
    """
    Render Free doesn't support Jobs, so we run Alembic migrations on app startup.
    This is gated to Render only to avoid slowing local development.
    """
    if os.getenv("RENDER") != "true":
        return

    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("✅ Alembic migrations applied (head).")
    except Exception as e:
        # Log the failure; keep app running so logs are visible in Render.
        print("❌ Failed to run migrations on startup:", repr(e))


app = FastAPI(
    title="Habit & Productivity Analytics API",
    version="0.1.0",
)

# Register routers
app.include_router(habits_router)
app.include_router(logs_router)
app.include_router(analytics_router)


@app.on_event("startup")
def startup_event():
    run_migrations_on_startup()


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}