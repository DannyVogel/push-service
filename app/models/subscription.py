from typing import Optional, Dict, Any
from pydantic import BaseModel

class Subscription(BaseModel):
    endpoint: str
    keys: Dict[str, str]
    expiration_time: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class UnsubscribeRequest(BaseModel):
    endpoint: str
