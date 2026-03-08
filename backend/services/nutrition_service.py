import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_nutrition_plan(
    calories, diet, allergies, health_profile=None, body_metrics=None
):

    health_context = ""

    if health_profile:
        health_context += f"""
Medical conditions: {health_profile.heart_conditions}, {health_profile.diabetes}, {health_profile.blood_pressure}
Food allergies: {health_profile.food_allergies}
"""

    if body_metrics:
        health_context += f"""
Height: {body_metrics.height} cm
Weight: {body_metrics.weight} kg
BMI: {body_metrics.bmi}
"""

    prompt = f"""
You are a professional nutritionist.

Create a weekly meal plan.

Calories per day: {calories}
Diet type: {diet}
Allergies: {allergies}

User health information:
{health_context}

Rules:
- Avoid foods that trigger allergies
- Suggest meals that support the fitness goal
- If BMI is high → suggest weight loss meals

Return ONLY valid JSON.

Format exactly like this:

{{
  "macros": {{
    "protein": "120g",
    "carbs": "220g",
    "fats": "60g"
  }},
  "todayMeals": [
    "Meal 1",
    "Meal 2",
    "Meal 3"
  ],
  "weeklyPlan": [
    {{
      "day": "Monday",
      "meals": ["Meal 1", "Meal 2", "Meal 3"]
    }}
  ],
  "groceryList": [
    "Item 1",
    "Item 2"
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional nutritionist."},
            {"role": "user", "content": prompt},
        ],
    )

    text = response.choices[0].message.content.strip()

    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception as e:
        return {"error": "AI response parsing failed", "details": str(e), "raw": text}
