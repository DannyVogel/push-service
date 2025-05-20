from pydantic import BaseModel

class Subscription(BaseModel):
    endpoint: str
    keys: dict
    spaceId: str 