from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from config.database import Base, engine

from routes.auth import router as auth_router
from routes.workouts import router as workout_router
from routes.nutrition import router as nutrition_router
from routes.progress import router as progress_router
from routes.ai import router as ai_router
from routes.calendar import router as calendar_router
from routes.health import router as health_router
from routes.dashboard import router as dashboard_router

from models import user, workout, nutrition, progress, health, workout_history
import models.body_metrics
import models.health_profile
import models.health_profile

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "ArogyaMitra API Running 🚀"}


app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(workout_router, prefix="/api/workouts", tags=["Workouts"])
app.include_router(nutrition_router, prefix="/api/nutrition", tags=["Nutrition"])
app.include_router(progress_router, prefix="/api/progress", tags=["Progress"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI"])
app.include_router(calendar_router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(health_router, prefix="/api/health", tags=["Health"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])
