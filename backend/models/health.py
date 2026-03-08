from fastapi import APIRouter
import random

router = APIRouter()


# Health check route
@router.get("/")
def health_check():
    return {"status": "ArogyaMitra backend is healthy"}


# Dashboard route
@router.get("/dashboard")
def dashboard():

    weekly = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    return {
        "calories": random.randint(1800, 2600),
        "steps": random.randint(4000, 12000),
        "streak": random.randint(1, 20),
        "activeMinutes": random.randint(30, 120),
        "charityImpact": random.randint(50, 300),
        "weightProgress": random.randint(40, 90),
        "cardioProgress": random.randint(40, 90),
        "strengthProgress": random.randint(40, 90),
        "weeklyActivity": [{"day": d, "value": random.randint(10, 80)} for d in weekly],
    }
