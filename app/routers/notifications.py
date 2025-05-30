from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.notification import NotificationRequest
from app.utils.response import success_response
from pywebpush import webpush, WebPushException
from app.utils.vapid import get_vapid_config
from app.utils.router import create_protected_router
from app.utils.logger import logger
from app.models.log import LogSource
import json

router = create_protected_router()

@router.post("/notify")
async def notify(
    request: NotificationRequest,
    req: Request
):
    try:
        vapid_private_key, vapid_public_key, vapid_email = get_vapid_config()

        # Log notification attempt
        await logger.info(
            "Sending push notification",
            source=LogSource.SERVICE,
            metadata={
                "subscription_endpoint": request.subscription.endpoint,
                "payload_title": request.payload.title if hasattr(request.payload, 'title') else None
            }
        )

        result = webpush(
            subscription_info=request.subscription.model_dump(),
            data=json.dumps(request.payload.model_dump()),
            vapid_private_key=vapid_private_key,
            vapid_claims={"sub": f"mailto:{vapid_email}"}
        )
        
        # Log successful notification
        await logger.info(
            "Push notification sent successfully",
            source=LogSource.SERVICE,
            metadata={"subscription_endpoint": request.subscription.endpoint, "subscription": request.subscription.keys.model_dump_json(), "result": result.json()}
        )
        
        return success_response(
            message="Notification sent",
            status_code=200
        )
    except WebPushException as ex:
        await logger.error(
            f"Web push failed: {str(ex)}",
            source=LogSource.SERVICE,
            metadata={
                "error_type": "WebPushException",
                "subscription_endpoint": request.subscription.endpoint if request.subscription else None,
                "error_details": str(ex)
            }
        )
        raise HTTPException(status_code=500, detail=f"Web push failed: {str(ex)}")
    except Exception as e:
        await logger.error(
            f"Notification failed: {str(e)}",
            source=LogSource.SERVICE,
            metadata={
                "error_type": type(e).__name__,
                "error_details": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Notification failed: {str(e)}") 