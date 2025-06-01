from typing import List, Optional, Dict, Any
from app.db.supabase import SupabaseDatabase
from app.models.subscription import SubscriptionRequest

db = SupabaseDatabase()

def add_subscription(subscription: SubscriptionRequest) -> List[Dict[str, Any]]:
    return db.add_subscription(subscription)

def remove_subscription(device_id: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    return db.remove_subscription(device_id, user_id)

def remove_user_subscriptions(user_id: str) -> List[Dict[str, Any]]:
    return db.remove_user_subscriptions(user_id)

def get_subscriptions(metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    return db.get_subscriptions(metadata_filter) 