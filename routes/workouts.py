from fastapi import APIRouter
from services.workout_service import generate_workout_plan

router = APIRouter()

@router.get("/plan")
def get_workout_plan():

    return generate_workout_plan("weight_loss", 30)