from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from config.database import SessionLocal
from routes.auth import get_current_user
from models.workout_history import WorkoutHistory
from models.body_metrics import BodyMetrics

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def get_dashboard(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    workouts = db.query(WorkoutHistory).filter(
        WorkoutHistory.user_id == user_id
    ).all()

    if not workouts:
        return {
            "calories": 0,
            "steps": 0,
            "streak": 0,
            "activeMinutes": 0,
            "charityImpact": 0,
            "weightProgress": 0,
            "cardioProgress": 0,
            "strengthProgress": 0,
            "weeklyActivity": [
                {"day": "Mon", "value": 0},
                {"day": "Tue", "value": 0},
                {"day": "Wed", "value": 0},
                {"day": "Thu", "value": 0},
                {"day": "Fri", "value": 0},
                {"day": "Sat", "value": 0},
                {"day": "Sun", "value": 0},
            ]
        }

    # TOTAL CALORIES
    calories = sum([w.calories for w in workouts])

    # ACTIVE MINUTES ESTIMATE
    active_minutes = len(workouts) * 20

    # STEPS ESTIMATE
    steps = len(workouts) * 2000

    # ---------------------------
    # WEEKLY ACTIVITY
    # ---------------------------

    weekly = {
        "Mon": 0,
        "Tue": 0,
        "Wed": 0,
        "Thu": 0,
        "Fri": 0,
        "Sat": 0,
        "Sun": 0
    }

    for w in workouts:

        day = w.completed_at.strftime("%a")

        if day in weekly:
            weekly[day] += 1

    weekly_activity = []

    for day, count in weekly.items():

        weekly_activity.append({
            "day": day,
            "value": count
        })

    # ---------------------------
    # STREAK CALCULATION
    # ---------------------------

    streak = 0
    today = datetime.now().date()

    for i in range(30):

        check_day = today - timedelta(days=i)

        exists = db.query(WorkoutHistory).filter(
            WorkoutHistory.user_id == user_id,
            WorkoutHistory.completed_at >= check_day,
            WorkoutHistory.completed_at < check_day + timedelta(days=1)
        ).first()

        if exists:
            streak += 1
        else:
            break

    # ---------------------------
    # WEIGHT PROGRESS
    # ---------------------------

    weights = db.query(BodyMetrics).filter(
        BodyMetrics.user_id == user_id
    ).order_by(BodyMetrics.created_at).all()

    weight_progress = 0

    if len(weights) >= 2:
        weight_progress = weights[-1].weight - weights[0].weight

    return {
        "calories": calories,
        "steps": steps,
        "streak": streak,
        "activeMinutes": active_minutes,
        "charityImpact": calories // 10,
        "weightProgress": weight_progress,
        "cardioProgress": len(workouts) * 5,
        "strengthProgress": len(workouts) * 5,
        "weeklyActivity": weekly_activity
    }