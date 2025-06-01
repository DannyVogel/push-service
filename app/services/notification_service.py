from typing import List, Dict, Any
from pywebpush import WebPushException
from app.models.notification_result import NotificationResult
from app.services.subscription_service import SubscriptionLookupService
from app.services.webpush_service import WebPushSender
from app.services.result_processor import NotificationResultProcessor
from app.utils.logger import logger
from app.models.log import LogSource

class NotificationService:
    """Main service that orchestrates notification sending"""
    
    def __init__(self):
        self.subscription_service = SubscriptionLookupService()
        self.web_push_sender = WebPushSender()
        self.result_processor = NotificationResultProcessor()
    
    async def send_to_device(self, device_id: str, payload: Dict[str, Any]) -> NotificationResult:
        """Send notification to a single device"""
        try:
            # Find subscription
            device_subscription = self.subscription_service.get_device_subscription(device_id)
            
            if not device_subscription:
                await logger.warn(
                    f"Subscription not found for device {device_id}",
                    source=LogSource.SERVICE,
                    metadata={"device_id": device_id}
                )
                return NotificationResult(device_id, False, "Subscription not found")
            
            # Build subscription info for webpush
            subscription_info = {
                "endpoint": device_subscription["endpoint"],
                "keys": device_subscription["keys"]
            }
            
            # Send notification
            self.web_push_sender.send_notification(subscription_info, payload)
            
            await logger.info(
                f"Push notification sent successfully to device {device_id}",
                source=LogSource.SERVICE,
                metadata={
                    "device_id": device_id, 
                    "endpoint": device_subscription["endpoint"]
                }
            )
            
            return NotificationResult(device_id, True)
            
        except WebPushException as ex:
            await logger.error(
                f"Web push failed for device {device_id}: {str(ex)}",
                source=LogSource.SERVICE,
                metadata={
                    "error_type": "WebPushException",
                    "device_id": device_id,
                    "error_details": str(ex)
                }
            )
            return NotificationResult(device_id, False, f"Web push failed: {str(ex)}")
            
        except Exception as e:
            await logger.error(
                f"Notification failed for device {device_id}: {str(e)}",
                source=LogSource.SERVICE,
                metadata={
                    "error_type": type(e).__name__,
                    "device_id": device_id,
                    "error_details": str(e)
                }
            )
            return NotificationResult(device_id, False, f"Notification failed: {str(e)}")
    
    async def send_batch_notifications(self, device_ids: List[str], payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send notifications to multiple devices and return response data"""
        await logger.info(
            f"Processing batch notification for {len(device_ids)} devices",
            source=LogSource.SERVICE,
            metadata={
                "device_count": len(device_ids),
                "payload_title": payload.get('title')
            }
        )
        
        # Send to each device
        for device_id in device_ids:
            result = await self.send_to_device(device_id, payload)
            self.result_processor.add_result(result)
        
        # Log final results
        total, successful, failed = self.result_processor.get_summary()
        await logger.info(
            f"Batch notification completed: {successful} successful, {failed} failed",
            source=LogSource.SERVICE,
            metadata={
                "total_devices": total,
                "successful_count": successful,
                "failed_count": failed
            }
        )
        
        return self.result_processor.get_response_data() 