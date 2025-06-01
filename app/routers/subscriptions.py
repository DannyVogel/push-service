from fastapi import HTTPException, Request
from app.db.methods import add_subscription, remove_subscription
from app.models.subscription import SubscriptionRequest, UnsubscribeRequest
from app.utils.response import success_response
from app.utils.router import create_protected_router
from app.utils.logger import logger
from app.models.log import LogSource

router = create_protected_router()

@router.post("/subscribe") 
async def subscribe(subscription_request: SubscriptionRequest, request: Request):
    try:
        await logger.info(
            "Processing subscription request",
            source=LogSource.SERVICE,
            metadata={
                "endpoint": subscription_request.subscription.endpoint if subscription_request and hasattr(subscription_request, 'subscription') else None,
                "client_ip": request.client.host if request.client else None
            }
        )
        
        result = add_subscription(subscription_request)
        
        await logger.info(
            "Subscription successful",
            source=LogSource.SERVICE,
            metadata={
                "endpoint": result[0]["endpoint"],
                "result_count": len(result)
            }
        )
        
        return success_response(
            data={"endpoint": result[0]["endpoint"]},
            message="Subscribed successfully",
            status_code=201
        )
    except Exception as e:
        await logger.error(
            f"Subscription failed: {str(e)}",
            source=LogSource.SERVICE,
            metadata={
                "error_type": type(e).__name__,
                "endpoint": subscription_request.subscription.endpoint if subscription_request and hasattr(subscription_request, 'subscription') else None,
                "error_details": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Subscription failed: {str(e)}")

@router.post("/unsubscribe")
async def unsubscribe(unsubscribe_request: UnsubscribeRequest, request: Request):
    try:
        await logger.info(
            "Processing unsubscribe request",
            source=LogSource.SERVICE,
            metadata={
                "device_id": unsubscribe_request.device_id,
                "user_id": unsubscribe_request.user_id,
                "client_ip": request.client.host if request.client else None
            }
        )
        
        result = remove_subscription(unsubscribe_request.device_id, unsubscribe_request.user_id)
        if not result:
            await logger.warn(
                "Unsubscribe failed: subscription not found",
                source=LogSource.SERVICE,
                metadata={"device_id": unsubscribe_request.device_id, "user_id": unsubscribe_request.user_id}
            )
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        await logger.info(
            "Unsubscribe successful",
            source=LogSource.SERVICE,
            metadata={"device_id": unsubscribe_request.device_id, "user_id": unsubscribe_request.user_id}
        )
        
        return success_response(
            data={"device_id": unsubscribe_request.device_id, "user_id": unsubscribe_request.user_id},
            message="Unsubscribed successfully",
            status_code=200
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        await logger.error(
            f"Unsubscribe failed: {str(e)}",
            source=LogSource.SERVICE,
            metadata={
                "error_type": type(e).__name__,
                "device_id": unsubscribe_request.device_id,
                "user_id": unsubscribe_request.user_id,
                "error_details": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Unsubscribe failed: {str(e)}") 
    
# @router.post("/unsubscribe_user")
# TODO: Implement this