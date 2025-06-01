from typing import List, Optional, Dict, Any
from app.db.base import DatabaseBackend
from app.dependencies import get_supabase_client
from app.models.subscription import SubscriptionRequest, UnsubscribeRequest, Subscription

class SupabaseDatabase(DatabaseBackend):
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def add_subscription(self, subscription_request: SubscriptionRequest) -> List[Dict[str, Any]]:
        subscription = subscription_request.subscription
        data = {
            "endpoint": subscription.endpoint,
            "keys": subscription.keys.model_dump(),
            "expiration_time": subscription.expiration_time,
            "metadata": subscription.metadata,
            "device_id": subscription_request.device_id,
        }
        result = self.supabase.table("subscriptions").upsert(
            data,
            on_conflict="endpoint"
        ).execute()
        return result.data

    def remove_subscriptions(self, device_ids: List[str]) -> List[Dict[str, Any]]:
        """Remove subscriptions for multiple device IDs"""
        result = self.supabase.table("subscriptions").delete().in_("device_id", device_ids).execute()
        return result.data

    def get_subscriptions(self, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        query = self.supabase.table("subscriptions").select("*")
        if metadata_filter:
            for key, value in metadata_filter.items():
                query = query.contains("metadata", {key: value})
        result = query.execute()
        return result.data 