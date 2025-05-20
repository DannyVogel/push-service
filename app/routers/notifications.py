from fastapi import APIRouter

router = APIRouter()

@router.post("/notify")
def notify():
    # Placeholder for notification logic
    return {"message": "Notification sent (placeholder)"} 