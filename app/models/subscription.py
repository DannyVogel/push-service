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

class UnsubscribeRequest(BaseModel):
    endpoint: str
