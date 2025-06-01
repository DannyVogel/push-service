from fastapi import HTTPException, Request
from app.db.methods import add_subscription, remove_subscriptions
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
                "endpoint": subscription_request.subscription.endpoint,
                "device_id": subscription_request.device_id,
                "client_ip": request.client.host if request.client else None
            }
        )
        
        result = add_subscription(subscription_request)
        
        await logger.info(
            "Subscription successful",
            source=LogSource.SERVICE,
            metadata={
                "endpoint": result[0]["endpoint"],
                "device_id": subscription_request.device_id,
                "result_count": len(result)
            }
        )
        
        return success_response(
            data={"endpoint": result[0]["endpoint"], "device_id": subscription_request.device_id},
            message="Subscribed successfully",
            status_code=201
        )
    except Exception as e:
        await logger.error(
            f"Subscription failed: {str(e)}",
            source=LogSource.SERVICE,
            metadata={
                "error_type": type(e).__name__,
                "endpoint": subscription_request.subscription.endpoint,
                "device_id": subscription_request.device_id,
                "error_details": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Subscription failed: {str(e)}")

@router.post("/unsubscribe")
async def unsubscribe(unsubscribe_request: UnsubscribeRequest, request: Request):
    try:
        await logger.info(
            f"Processing batch unsubscribe request for {len(unsubscribe_request.device_ids)} devices",
            source=LogSource.SERVICE,
            metadata={
                "device_ids": unsubscribe_request.device_ids,
                "device_count": len(unsubscribe_request.device_ids),
                "client_ip": request.client.host if request.client else None
            }
        )
        
        result = remove_subscriptions(unsubscribe_request.device_ids)
        if not result:
            await logger.warn(
                "Unsubscribe failed: no subscriptions found for provided device IDs",
                source=LogSource.SERVICE,
                metadata={"device_ids": unsubscribe_request.device_ids}
            )
            raise HTTPException(status_code=404, detail="No subscriptions found for provided device IDs")
        
        await logger.info(
            f"Batch unsubscribe successful: removed {len(result)} subscriptions",
            source=LogSource.SERVICE,
            metadata={
                "device_ids": unsubscribe_request.device_ids,
                "removed_count": len(result)
            }
        )
        
        return success_response(
            data={
                "device_ids": unsubscribe_request.device_ids,
                "removed_count": len(result),
                "removed_subscriptions": result
            },
            message=f"Successfully unsubscribed {len(result)} devices",
            status_code=200
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        await logger.error(
            f"Batch unsubscribe failed: {str(e)}",
            source=LogSource.SERVICE,
            metadata={
                "error_type": type(e).__name__,
                "device_ids": unsubscribe_request.device_ids,
                "error_details": str(e)
            }
        )
        raise HTTPException(status_code=500, detail=f"Batch unsubscribe failed: {str(e)}")