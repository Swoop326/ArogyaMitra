from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat_with_aromi(data: ChatRequest):

    user_message = data.message

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=500,
            messages=[
                {
                    "role": "system",
                    "content": """
You are AROMI, a friendly AI fitness coach in the ArogyaMitra app.

Help users with workouts, injuries, nutrition, travel workouts and motivation.
Keep responses practical and supportive.
""",
                },
                {"role": "user", "content": user_message},
            ],
        )

        reply = response.choices[0].message.content

        return {"reply": reply}

    except Exception:
        return {"reply": "Sorry, AROMI is having trouble right now. Please try again."}
