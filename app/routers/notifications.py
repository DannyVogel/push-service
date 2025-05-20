from fastapi import APIRouter, Depends
from app.dependencies import verify_api_key

router = APIRouter()

@router.post("/notify")
def notify(api_key: str = Depends(verify_api_key)):
    # Placeholder for notification logic
    return {"message": "Notification sent (placeholder)"} 