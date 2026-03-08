from fastapi import APIRouter

router = APIRouter()


@router.post("/aromi-chat")
def ai_chat():
    return {"response": "AI Coach response"}
