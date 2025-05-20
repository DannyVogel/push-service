from fastapi import APIRouter, HTTPException
from app.db.supabase import SupabaseDatabase
from app.models.subscription import Subscription, UnsubscribeRequest
from app.utils import success_response

router = APIRouter()
supabase = SupabaseDatabase()

@router.post("/subscribe")
def subscribe(subscription: Subscription):
    try:
        result = supabase.add_subscription(subscription.model_dump())
        return success_response(
            data=result,
            message="Subscribed successfully",
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription failed: {str(e)}")

@router.post("/unsubscribe")
def unsubscribe(unsubscribe_request: UnsubscribeRequest):
    try:
        result = supabase.remove_subscription(unsubscribe_request.endpoint)
        if not result:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return success_response(
            data=result,
            message="Unsubscribed successfully",
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unsubscribe failed: {str(e)}") 