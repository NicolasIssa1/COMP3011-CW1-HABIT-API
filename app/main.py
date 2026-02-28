import os

from fastapi import FastAPI
from alembic import command
from alembic.config import Config

from app.core.config import DATABASE_URL
from app.db.base import Base
from app.db.session import engine

from app.routers.habits import router as habits_router
from app.routers.logs import router as logs_router
from app.routers.analytics import router as analytics_router


def apply_schema_on_startup() -> None:
    """
    Render Free has no Jobs, and SQLite paths can be tricky on ephemeral disks.
    We do:
      1) Alembic upgrade head (so migrations are used)
      2) create_all safety net (guarantees tables exist for SQLite)
    """
    # Helpful debug info in Render logs
    print("Startup: CWD =", os.getcwd())
    print("Startup: DATABASE_URL =", DATABASE_URL)

    # 1) Try Alembic migrations
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
        command.upgrade(alembic_cfg, "head")
        print("✅ Alembic migrations applied (head).")
    except Exception as e:
        print("❌ Alembic upgrade failed:", repr(e))

    # 2) Safety net: ensure tables exist (especially for SQLite on Render)
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Base.metadata.create_all() ensured tables exist.")
    except Exception as e:
        print("❌ create_all failed:", repr(e))


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
    apply_schema_on_startup()


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}