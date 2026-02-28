import os

from fastapi import FastAPI
from alembic import command
from alembic.config import Config

from app.core.config import DATABASE_URL
from app.routers.habits import router as habits_router
from app.routers.logs import router as logs_router
from app.routers.analytics import router as analytics_router


def run_migrations_on_startup() -> None:
    """
    On Render Free, we can't run one-off Jobs, so we apply migrations at startup.
    We also force Alembic to use the same DATABASE_URL as the app.
    """
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

        command.upgrade(alembic_cfg, "head")
        print("✅ Alembic migrations applied (head). Using DATABASE_URL:", DATABASE_URL)
    except Exception as e:
        # If migrations fail, keep the app running so the error is visible in Render logs.
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
    # Always run; it's fast if already up-to-date
    run_migrations_on_startup()


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}