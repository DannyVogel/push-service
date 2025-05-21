from pydantic import BaseModel
from typing import Optional
from app.models.subscription import Subscription

class NotificationData(BaseModel):
    url: str = "/"
    spaceId: Optional[str] = None

class NotificationPayload(BaseModel):
    title: str
    body: str
    icon: Optional[str] = None
    data: Optional[NotificationData] = None

class NotificationRequest(BaseModel):
    payload: NotificationPayload
    subscription: Subscription 