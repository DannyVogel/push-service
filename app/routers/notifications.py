from fastapi import HTTPException, Request
from app.models.notification import NotificationRequest
from app.utils.response import success_response
from app.utils.router import create_protected_router
from app.utils.logger import logger
from app.models.log import LogSource
from app.services.notification_service import NotificationService

router = create_protected_router()

@router.post("/notify")
async def notify(request: NotificationRequest, req: Request):
    try:
        notification_service = NotificationService()
        response_data = await notification_service.send_batch_notifications(
            request.device_ids, 
            request.payload.model_dump()
        )
        
        status_code, message = notification_service.result_processor.get_status_code_and_message()
        
        return success_response(
            data=response_data,
            message=message,
            status_code=status_code
        )
        
    except Exception as e:
        await logger.error(
            f"Batch notification failed: {str(e)}",
            source=LogSource.SERVICE,
            metadata={
                "error_type": type(e).__name__,
                "error_details": str(e),
                "device_count": len(request.device_ids)
            }
        )
        raise HTTPException(status_code=500, detail=f"Batch notification failed: {str(e)}") 