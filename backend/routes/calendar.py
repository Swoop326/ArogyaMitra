from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_calendar():
    return {"message": "Calendar integration working"}
