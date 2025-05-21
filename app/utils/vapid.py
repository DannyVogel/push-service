from fastapi import HTTPException
from app.config import VAPID_PRIVATE_KEY, VAPID_PUBLIC_KEY, VAPID_EMAIL

def get_vapid_config():
    if not (VAPID_PRIVATE_KEY and VAPID_PUBLIC_KEY and VAPID_EMAIL):
        raise HTTPException(status_code=500, detail="VAPID keys or email not configured.")
    return VAPID_PRIVATE_KEY, VAPID_PUBLIC_KEY, VAPID_EMAIL 