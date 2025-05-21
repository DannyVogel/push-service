from fastapi import Header, HTTPException, Request
from app.config import API_KEY, ALLOWED_ORIGINS

async def verify_api_key(request: Request, x_api_key: str = Header(default=None)):
    expected_key = API_KEY
    if x_api_key and x_api_key == expected_key:
        return

    origin = request.headers.get("origin")
    if origin and origin in ALLOWED_ORIGINS:
        return

    raise HTTPException(
        status_code=403,
        detail="Forbidden: Invalid API key or origin not allowed"
    )