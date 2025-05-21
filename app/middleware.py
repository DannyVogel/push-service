from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import ALLOWED_ORIGINS

class OriginRestrictionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        if origin and origin not in ALLOWED_ORIGINS:
            return JSONResponse(
                status_code=403,
                content={"detail": f"Origin '{origin}' not allowed"}
            )
        return await call_next(request)
