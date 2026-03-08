from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.health_profile import HealthProfile
from routes.auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Save / Update Health Assessment
# -----------------------------
@router.post("/assessment")
def save_health_assessment(
    data: dict, current_user=Depends(get_current_user), db: Session = Depends(get_db)
):

    user_id = current_user["id"]

    # Check if profile already exists
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()

    # If not, create new profile
    if not profile:
        profile = HealthProfile(user_id=user_id)
        db.add(profile)

    # Update fields
    profile.heart_conditions = data.get("heart_conditions")
    profile.diabetes = data.get("diabetes")
    profile.blood_pressure = data.get("blood_pressure")

    profile.knee_injury = data.get("knee_injury")
    profile.back_pain = data.get("back_pain")
    profile.other_injuries = data.get("other_injuries")

    profile.food_allergies = data.get("food_allergies")
    profile.medication_allergies = data.get("medication_allergies")

    profile.current_medication = data.get("current_medication")
    profile.supplements = data.get("supplements")

    profile.fitness_goal = data.get("fitness_goal")

    db.commit()

    return {"message": "Health profile saved"}


# -----------------------------
# Check if profile exists
# -----------------------------
@router.get("/profile")
def check_health_profile(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):

    profile = (
        db.query(HealthProfile)
        .filter(HealthProfile.user_id == current_user["id"])
        .first()
    )

    if not profile:
        return {"profile_completed": False}

    return {"profile_completed": True}


# -----------------------------
# Debug route (for development)
# -----------------------------
@router.get("/debug")
def debug_profiles(db: Session = Depends(get_db)):

    profiles = db.query(HealthProfile).all()

    return {
        "count": len(profiles),
        "profiles": [{"id": p.id, "user_id": p.user_id} for p in profiles],
    }


# -----------------------------
# Clear all profiles (testing)
# -----------------------------
@router.delete("/clear")
def clear_profiles(db: Session = Depends(get_db)):

    db.query(HealthProfile).delete()
    db.commit()

    return {"message": "All health profiles deleted"}
