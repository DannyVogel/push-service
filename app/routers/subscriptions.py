from fastapi import APIRouter, HTTPException
from app.db.methods import add_subscription, remove_subscription
from app.models.subscription import Subscription, UnsubscribeRequest
from app.utils.response import success_response
import logging

router = APIRouter()

@router.post("/subscribe")
def subscribe(subscription: Subscription):
    try:
        result = add_subscription(subscription.model_dump())
        return success_response(
            data={"endpoint": result[0]["endpoint"]},
            message="Subscribed successfully",
            status_code=201
        )
    except Exception as e:
        logging.error(f"Subscription failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Subscription failed: {str(e)}")

@router.post("/unsubscribe")
def unsubscribe(unsubscribe_request: UnsubscribeRequest):
    try:
        result = remove_subscription(unsubscribe_request.endpoint)
        if not result:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return success_response(
            data={"endpoint": result["endpoint"]},
            message="Unsubscribed successfully",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Unsubscribe failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unsubscribe failed: {str(e)}") 