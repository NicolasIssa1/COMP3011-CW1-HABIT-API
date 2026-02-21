from fastapi import FastAPI
from app.routers.habits import router as habits_router
from app.routers.logs import router as logs_router

app = FastAPI(
    title="Habit & Productivity Analytics API",
    version="0.1.0",
)

# Register routers
app.include_router(habits_router)
app.include_router(logs_router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
