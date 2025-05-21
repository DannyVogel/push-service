from fastapi import APIRouter, Depends, HTTPException, Header
from app.dependencies import verify_api_key
from app.models.notification import NotificationRequest
from app.utils.response import success_response
from pywebpush import webpush, WebPushException
from app.utils.vapid import get_vapid_config
import json
import logging

router = APIRouter()

@router.post("/notify")
def notify(
    request: NotificationRequest,
):
    try:
        vapid_private_key, vapid_email = get_vapid_config()

        webpush(
            subscription_info=request.subscription.model_dump(),
            data=json.dumps(request.payload.model_dump()),
            vapid_private_key=vapid_private_key,
            vapid_claims={"sub": f"mailto:{vapid_email}"}
        )
        
        return success_response(
            message="Notification sent",
            status_code=200
        )
    except WebPushException as ex:
        logging.error(f"Web push failed: {str(ex)}")
        raise HTTPException(status_code=500, detail=f"Web push failed: {str(ex)}")
    except Exception as e:
        logging.error(f"Notification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Notification failed: {str(e)}") 