from typing import Optional, Dict, Any
from app.db.methods import get_subscriptions

class SubscriptionLookupService:
    """Handles finding device subscriptions"""
    
    def __init__(self):
        self.subscriptions_cache = None
    
    def get_device_subscription(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription data for a specific device"""
        if self.subscriptions_cache is None:
            self.subscriptions_cache = get_subscriptions()
        
        return next(
            (sub for sub in self.subscriptions_cache if sub.get("device_id") == device_id), 
            None
        ) 