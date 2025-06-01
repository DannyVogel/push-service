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
            "user_id": subscription_request.user_id,
        }
        result = self.supabase.table("subscriptions").upsert(
            data,
            on_conflict="endpoint"
        ).execute()
        return result.data

    def remove_subscription(self, device_id: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.supabase.table("subscriptions").delete().eq("device_id", device_id)
        
        if user_id is not None:
            query = query.eq("user_id", user_id)
            
        result = query.execute()
        return result.data

    def remove_user_subscriptions(self, user_id: str) -> List[Dict[str, Any]]:
        result = self.supabase.table("subscriptions").delete().eq("user_id", user_id).execute()
        return result.data

    def get_subscriptions(self, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        query = self.supabase.table("subscriptions").select("*")
        if metadata_filter:
            for key, value in metadata_filter.items():
                query = query.contains("metadata", {key: value})
        result = query.execute()
        return result.data 