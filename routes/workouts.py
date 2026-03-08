from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
import os
import requests

from config.database import SessionLocal
from routes.auth import get_current_user
from models.workout import WorkoutPlan
from models.workout_history import WorkoutHistory
from services.workout_service import generate_workout_plan

router = APIRouter()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class WorkoutRequest(BaseModel):
    goal: str
    level: str
    days: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# YouTube Exercise Video
# -----------------------------
def get_youtube_video(exercise_name: str):

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": f"{exercise_name} exercise tutorial",
        "key": YOUTUBE_API_KEY,
        "maxResults": 1,
        "type": "video"
    }

    try:
        res = requests.get(url, params=params)

        data = res.json()

        video_id = data["items"][0]["id"]["videoId"]

        return f"https://www.youtube.com/embed/{video_id}"

    except:
        return None


# -----------------------------
# Generate Workout Plan
# -----------------------------
@router.post("/plan")
def generate_plan(
    data: WorkoutRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    goal = data.goal.replace("-", "_")

    level = data.level

    days = data.days

    plan = generate_workout_plan(goal, level, days)

    workout = WorkoutPlan(
        user_id=user_id,
        goal=goal,
        level=level,
        days=days,
        plan_json=json.dumps(plan)
    )

    db.add(workout)
    db.commit()

    return plan


# -----------------------------
# Get Workout Day
# -----------------------------
@router.get("/day/{day}")
def get_workout_day(
    day: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    workout = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user_id
    ).order_by(WorkoutPlan.id.desc()).first()

    if not workout:
        return {"error": "No workout plan found"}

    plan = json.loads(workout.plan_json)

    for d in plan["plan"]:

        if d["day"] == f"Day {day}":

            return d

    return {"error": "Day not found"}


# -----------------------------
# Get Single Exercise
# -----------------------------
@router.get("/exercise/{day}/{exercise_index}")
def get_single_exercise(
    day: int,
    exercise_index: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    workout = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user_id
    ).order_by(WorkoutPlan.id.desc()).first()

    if not workout:
        return {"error": "No workout plan"}

    plan = json.loads(workout.plan_json)

    for d in plan["plan"]:

        if d["day"] == f"Day {day}":

            exercises = d["exercises"]

            if exercise_index >= len(exercises):
                return {"error": "Exercise not found"}

            exercise = exercises[exercise_index]

            exercise["video"] = get_youtube_video(exercise["name"])

            sets = exercise.get("sets", 1)

            reps = exercise.get("reps", 10)

            exercise["calories"] = round(sets * reps * 0.3, 2)

            exercise["exercise_index"] = exercise_index

            exercise["total_exercises"] = len(exercises)

            return exercise

    return {"error": "Exercise not found"}


# -----------------------------
# Complete Workout Day
# -----------------------------
@router.post("/complete-day/{day}")
def complete_day(
    day: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    workout = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user_id
    ).order_by(WorkoutPlan.id.desc()).first()

    if not workout:
        return {"error": "No workout plan found"}

    existing = db.query(WorkoutHistory).filter(
        WorkoutHistory.workout_id == workout.id,
        WorkoutHistory.day == day
    ).first()

    if existing:
        return {"message": f"Day {day} already completed"}

    history = WorkoutHistory(
        user_id=user_id,
        workout_id=workout.id,
        day=day,
        calories=100
    )

    db.add(history)

    db.commit()

    return {"message": f"Day {day} completed successfully"}


# -----------------------------
# Get Today's Workout
# -----------------------------
@router.get("/today")
def get_today_workout(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    workout = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user_id
    ).order_by(WorkoutPlan.id.desc()).first()

    if not workout:
        return {"error": "No workout plan generated"}

    completed_days = db.query(WorkoutHistory).filter(
        WorkoutHistory.workout_id == workout.id
    ).all()

    completed_count = len(completed_days)

    next_day = completed_count + 1

    if next_day > workout.days:

        return {
            "status": "finished",
            "message": "Workout plan completed"
        }

    return {
        "day": next_day
    }