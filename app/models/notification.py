from pydantic import BaseModel
from typing import Optional, List, Union
from enum import Enum
from app.models.subscription import Subscription

class NotificationDirection(str, Enum):
    AUTO = "auto"
    LTR = "ltr"
    RTL = "rtl"

class NotificationAction(BaseModel):
    action: str
    title: str
    icon: Optional[str] = None

class NotificationData(BaseModel):
    url: str = "/"
    spaceId: Optional[str] = None

class NotificationPayload(BaseModel):
    title: str
    body: Optional[str] = None
    icon: Optional[str] = None
    badge: Optional[str] = None
    image: Optional[str] = None
    tag: Optional[str] = None
    requireInteraction: Optional[bool] = None
    silent: Optional[bool] = None
    renotify: Optional[bool] = None
    actions: Optional[List[NotificationAction]] = None
    timestamp: Optional[int] = None
    vibrate: Optional[Union[int, List[int]]] = None
    lang: Optional[str] = None
    dir: Optional[NotificationDirection] = None
    data: Optional[NotificationData] = None

class NotificationRequest(BaseModel):
    payload: NotificationPayload
    device_id: str
    user_id: Optional[str] = None