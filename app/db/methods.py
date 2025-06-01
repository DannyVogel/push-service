from typing import List, Optional, Dict, Any
from app.db.supabase import SupabaseDatabase
from app.models.subscription import SubscriptionRequest

db = SupabaseDatabase()

def add_subscription(subscription: SubscriptionRequest) -> List[Dict[str, Any]]:
    return db.add_subscription(subscription)

def remove_subscriptions(device_ids: List[str]) -> List[Dict[str, Any]]:
    return db.remove_subscriptions(device_ids)

def get_subscriptions(metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    return db.get_subscriptions(metadata_filter) 