import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_workout_plan(goal, level, days, health_profile=None, body_metrics=None):

    health_context = ""

    if health_profile:
        health_context += f"""
Medical conditions: {health_profile.heart_conditions}, {health_profile.diabetes}, {health_profile.blood_pressure}
Injuries: knee {health_profile.knee_injury}, back {health_profile.back_pain}, other {health_profile.other_injuries}
"""

    if body_metrics:
        health_context += f"""
Height: {body_metrics.height} cm
Weight: {body_metrics.weight} kg
BMI: {body_metrics.bmi}
"""

    prompt = f"""
Create a {days}-day workout plan.

Goal: {goal}
Experience level: {level}

User health information:
{health_context}

Important rules:
- Avoid exercises that worsen injuries
- Avoid high intensity if user has medical issues
- Create safe workouts based on BMI

Return ONLY valid JSON in this format:

{{
  "plan": [
    {{
      "day": "Day 1",
      "workout": "Upper Body Strength",
      "exercises": [
        {{
          "name": "Push-ups",
          "sets": 3,
          "reps": 12,
          "rest": "30s",
          "difficulty": "{level.capitalize()}"
        }}
      ]
    }}
  ]
}}

Rules:
- Create exactly {days} workout days
- Each day must contain exactly 3 exercises
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional fitness trainer. Return ONLY JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response.choices[0].message.content

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return json.loads(match.group())

        return {"plan": []}