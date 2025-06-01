from typing import Dict, Any
import json
from pywebpush import webpush
from app.utils.vapid import get_vapid_config

class WebPushSender:
    """Handles actual web push notification sending"""
    
    def __init__(self):
        self.vapid_private_key, self.vapid_public_key, self.vapid_email = get_vapid_config()
    
    def send_notification(self, subscription_info: Dict[str, Any], payload: Dict[str, Any]) -> bool:
        """Send notification to a single subscription. Returns True if successful."""
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=self.vapid_private_key,
            vapid_claims={"sub": f"mailto:{self.vapid_email}"}
        )
        return True 