from fastapi import APIRouter
from services.nutrition_service import generate_meal_plan

router = APIRouter()

@router.get("/meal-plan")
def get_meal_plan():

    return generate_meal_plan(1800)