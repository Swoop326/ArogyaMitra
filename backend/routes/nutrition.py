from fastapi import APIRouter
from pydantic import BaseModel
from services.nutrition_service import generate_nutrition_plan
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

router = APIRouter()


class NutritionRequest(BaseModel):
    calories: int
    diet: str
    allergies: str


# -----------------------------
# Helper: Find Recipe For Meal
# -----------------------------
def find_recipe(meal_name: str):

    # simplify meal name to improve match
    simplified = meal_name.split(" with ")[0]

    url = "https://api.spoonacular.com/recipes/complexSearch"

    params = {
        "query": simplified,
        "number": 1,
        "apiKey": SPOONACULAR_API_KEY
    }

    try:

        res = requests.get(url, params=params)

        if res.status_code == 402:
            print("Spoonacular API limit reached")
            return None

        if res.status_code != 200:
            print("Spoonacular error:", res.text)
            return None

        data = res.json()

        results = data.get("results", [])

        if not results:
            print("No recipe found for:", simplified)
            return None

        recipe = results[0]

        recipe_id = recipe.get("id")
        image = recipe.get("image")

        if not image:
            image = f"https://img.spoonacular.com/recipes/{recipe_id}-312x231.jpg"

        return {
            "recipe_id": recipe_id,
            "image": image
        }

    except Exception as e:

        print("Recipe search error:", e)
        return None


# -----------------------------
# Generate AI Nutrition Plan
# -----------------------------
@router.post("/plan")
def generate_plan(data: NutritionRequest):

    result = generate_nutrition_plan(
        data.calories,
        data.diet,
        data.allergies
    )

    weekly = result.get("weeklyPlan", [])

    # detect today's day
    today = datetime.today().strftime("%A")

    for day in weekly:

        enriched_meals = []

        for meal in day.get("meals", []):

            # Only fetch recipe for today's meals
            if day.get("day") == today:

                recipe = find_recipe(meal)

                if recipe:

                    enriched_meals.append({
                        "name": meal,
                        "recipe_id": recipe["recipe_id"],
                        "image": recipe["image"]
                    })

                    print(f"Mapped: {meal} -> {recipe['recipe_id']}")

                else:

                    enriched_meals.append({
                        "name": meal,
                        "recipe_id": None,
                        "image": "https://placehold.co/300x200?text=Food"
                    })

            else:
                # skip API call for other days
                enriched_meals.append({
                    "name": meal,
                    "recipe_id": None,
                    "image": "https://placehold.co/300x200?text=Food"
                })

        day["meals"] = enriched_meals

    result["weeklyPlan"] = weekly

    return result


# -----------------------------
# Random Recipes
# -----------------------------
@router.get("/recipes")
def get_recipes(diet: str = "vegetarian"):

    url = "https://api.spoonacular.com/recipes/random"

    params = {
        "number": 6,
        "apiKey": SPOONACULAR_API_KEY
    }

    if diet == "vegetarian":
        params["tags"] = "vegetarian"

    elif diet == "vegan":
        params["tags"] = "vegan"

    try:

        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"error": "Spoonacular API failed"}

        data = response.json()

        recipes = []

        for r in data.get("recipes", []):

            recipe_id = r.get("id")
            image = r.get("image")

            if image and image.endswith("."):
                image = image + "jpg"

            if not image:
                image = f"https://img.spoonacular.com/recipes/{recipe_id}-312x231.jpg"

            recipes.append({
                "id": recipe_id,
                "title": r.get("title"),
                "image": image,
                "readyInMinutes": r.get("readyInMinutes"),
                "servings": r.get("servings")
            })

        return recipes

    except Exception as e:

        return {
            "error": "Failed to fetch recipes",
            "details": str(e)
        }


# -----------------------------
# Recipe Details
# -----------------------------
@router.get("/recipe/{recipe_id}")
def get_recipe_details(recipe_id: int):

    try:

        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"

        params = {
            "apiKey": SPOONACULAR_API_KEY,
            "includeNutrition": True
        }

        res = requests.get(url, params=params)

        if res.status_code != 200:
            print("Recipe details error:", res.text)
            return {"error": "Recipe fetch failed"}

        data = res.json()

        return {
            "title": data.get("title"),
            "image": data.get("image"),
            "readyInMinutes": data.get("readyInMinutes"),
            "servings": data.get("servings"),
            "summary": data.get("summary"),
            "instructions": data.get("instructions"),
            "ingredients": [
                i["original"] for i in data.get("extendedIngredients", [])
            ]
        }

    except Exception as e:

        return {"error": str(e)}