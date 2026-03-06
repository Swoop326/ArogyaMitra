from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.workouts import router as workout_router
from routes.nutrition import router as nutrition_router
from routes.progress import router as progress_router
from routes.ai_coach import router as ai_router
from routes.calendar import router as calendar_router
from routes.health import router as health_router

from config.database import Base, engine
from models import user, workout, nutrition, progress, health

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ArogyaMitra API Running 🚀"}

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(workout_router, prefix="/api/workouts", tags=["Workouts"])
app.include_router(nutrition_router, prefix="/api/nutrition", tags=["Nutrition"])
app.include_router(progress_router, prefix="/api/progress", tags=["Progress"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI Coach"])
app.include_router(calendar_router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(health_router, prefix="/api/health", tags=["Health"])