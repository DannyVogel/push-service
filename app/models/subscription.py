from typing import Optional, Dict, Any
from pydantic import BaseModel

class Keys(BaseModel):
    p256dh: str
    auth: str

class Subscription(BaseModel):
    endpoint: str
    keys: Keys
    expiration_time: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class SubscriptionRequest(BaseModel):
    subscription: Subscription
    device_id: str
    user_id: Optional[str] = None

class UnsubscribeRequest(BaseModel):
    device_id: str
    user_id: Optional[str] = None

