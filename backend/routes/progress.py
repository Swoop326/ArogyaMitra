from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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


# -----------------------------
# Overview Stats
# -----------------------------
@router.get("/overview")
def get_overview(current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    user_id = current_user["id"]

    workouts = db.query(WorkoutHistory).filter(WorkoutHistory.user_id == user_id).all()

    workouts_completed = len(workouts)

    calories_burned = sum([w.calories for w in workouts])

    meals_tracked = 0

    return {
        "workouts_completed": workouts_completed,
        "calories_burned": calories_burned,
        "meals_tracked": meals_tracked,
    }


# -----------------------------
# Workout Frequency
# -----------------------------
@router.get("/workouts")
def workout_frequency(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    workouts = db.query(WorkoutHistory).filter(WorkoutHistory.user_id == user_id).all()

    frequency = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}

    for w in workouts:

        day = w.completed_at.strftime("%a")

        if day in frequency:
            frequency[day] += 1

    return [{"day": k, "workouts": v} for k, v in frequency.items()]


# -----------------------------
# Calories Chart
# -----------------------------
@router.get("/calories")
def calories_chart(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    workouts = db.query(WorkoutHistory).filter(WorkoutHistory.user_id == user_id).all()

    weekly = {"W1": 0, "W2": 0, "W3": 0, "W4": 0}

    for i, w in enumerate(workouts):

        week = f"W{(i//5)+1}"

        if week in weekly:
            weekly[week] += w.calories

    return [{"week": k, "calories": v} for k, v in weekly.items()]


# -----------------------------
# Weight History
# -----------------------------
@router.get("/weight-history")
def weight_history(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    weights = (
        db.query(BodyMetrics)
        .filter(BodyMetrics.user_id == user_id)
        .order_by(BodyMetrics.created_at)
        .all()
    )

    return [{"month": w.created_at.strftime("%b"), "weight": w.weight} for w in weights]


# -----------------------------
# Save Body Metrics
# -----------------------------
@router.post("/body")
def save_body(
    data: dict, current_user=Depends(get_current_user), db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    height = data["height"]
    weight = data["weight"]

    height_m = height / 100

    bmi = round(weight / (height_m**2), 1)

    body_fat = round(bmi * 0.7)
    muscle_mass = round(weight * 0.6)

    body = BodyMetrics(
        user_id=user_id,
        height=height,
        weight=weight,
        bmi=bmi,
        body_fat_percent=body_fat,
        muscle_mass=muscle_mass,
    )

    db.add(body)
    db.commit()

    return {"message": "Body metrics saved"}


# -----------------------------
# Get Latest Body Metrics
# -----------------------------
@router.get("/body")
def get_body(current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    user_id = current_user["id"]

    body = (
        db.query(BodyMetrics)
        .filter(BodyMetrics.user_id == user_id)
        .order_by(BodyMetrics.id.desc())
        .first()
    )

    if not body:

        return {
            "height": 0,
            "weight": 0,
            "bmi": 0,
            "body_fat_percent": 0,
            "muscle_mass": 0,
        }

    return {
        "height": body.height,
        "weight": body.weight,
        "bmi": body.bmi,
        "body_fat_percent": body.body_fat_percent,
        "muscle_mass": body.muscle_mass,
    }


@router.get("/achievements")
def get_achievements(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    workouts = (
        db.query(WorkoutHistory).filter(WorkoutHistory.user_id == user_id).count()
    )

    achievements = [
        {
            "title": "First Workout",
            "description": "Complete your first workout",
            "earned": workouts >= 1,
        },
        {
            "title": "Workout Beginner",
            "description": "Complete 5 workouts",
            "earned": workouts >= 5,
        },
        {
            "title": "Fitness Warrior",
            "description": "Complete 20 workouts",
            "earned": workouts >= 20,
        },
    ]

    return achievements
