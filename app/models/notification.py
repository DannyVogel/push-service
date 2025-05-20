from pydantic import BaseModel

class NotificationPayload(BaseModel):
    title: str
    body: str
    url: str 