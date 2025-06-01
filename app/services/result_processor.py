from typing import List, Dict, Any, Tuple
from app.models.notification_result import NotificationResult

class NotificationResultProcessor:
    """Handles result counting and status code determination"""
    
    def __init__(self):
        self.results: List[NotificationResult] = []
    
    def add_result(self, result: NotificationResult):
        """Add a notification result"""
        self.results.append(result)
    
    def get_summary(self) -> Tuple[int, int, int]:
        """Returns (total, successful, failed) counts"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total - successful
        return total, successful, failed
    
    def get_status_code_and_message(self) -> Tuple[int, str]:
        """Determine appropriate HTTP status code and message"""
        total, successful, failed = self.get_summary()
        
        if successful == 0:
            return 500, "All notifications failed"
        elif failed == 0:
            return 200, "All notifications sent successfully"
        else:
            return 207, f"{successful} notifications sent, {failed} failed"
    
    def get_response_data(self) -> Dict[str, Any]:
        """Build the response data structure"""
        total, successful, failed = self.get_summary()
        
        return {
            "results": [
                {
                    "device_id": r.device_id,
                    "success": r.success,
                    **({"error": r.error} if r.error else {})
                }
                for r in self.results
            ],
            "summary": {
                "total": total,
                "successful": successful,
                "failed": failed
            }
        } 