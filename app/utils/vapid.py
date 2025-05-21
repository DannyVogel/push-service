import os
from fastapi import HTTPException

def get_vapid_config():
    vapid_private_key = os.environ.get("VAPID_PRIVATE_KEY")
    vapid_public_key = os.environ.get("VAPID_PUBLIC_KEY")
    vapid_email = os.environ.get("VAPID_EMAIL")
    if not (vapid_private_key and vapid_public_key and vapid_email):
        raise HTTPException(status_code=500, detail="VAPID keys or email not configured.")
    return vapid_private_key, vapid_public_key, vapid_email 