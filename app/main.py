import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import DATABASE_URL, ENVIRONMENT
from app.db.base import Base
from app.db.session import engine

from app.routers.habits import router as habits_router
from app.routers.logs import router as logs_router
from app.routers.analytics import router as analytics_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def apply_schema_on_startup() -> None:
    """Create all tables if they don't exist."""
    logger.info(f"Startup: CWD = {os.getcwd()}")
    logger.info(f"Startup: DATABASE_URL = {DATABASE_URL}")
    logger.info(f"Startup: ENVIRONMENT = {ENVIRONMENT}")

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created/verified.")
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {repr(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    apply_schema_on_startup()
    yield


app = FastAPI(
    title="Habit & Productivity Analytics API",
    version="1.0.0",
    description="A comprehensive API for tracking habits, logging completions, and analyzing productivity patterns.",
    contact={
        "name": "API Support",
        "email": "support@habitapi.dev"
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    logger.info(f"→ {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"← {request.method} {request.url.path} | Status: {response.status_code} | Time: {process_time:.3f}s")
    
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {repr(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__}
    )


# Register routers
app.include_router(habits_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")


# Serve static files (front-end)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="static")
    logger.info(f"✅ Static files mounted at /ui from {static_dir}")
else:
    logger.warning(f"Static directory not found at {static_dir}")


@app.get("/health", tags=["health"], summary="Health Check")
def health_check():
    """Check if the API is running and healthy."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "environment": ENVIRONMENT
    }


@app.get("/", tags=["root"], summary="API Info")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Habit & Productivity Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }