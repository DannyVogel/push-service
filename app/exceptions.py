from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "message": exc.detail if isinstance(exc.detail, str) else "An error occurred.",
            "error": exc.detail,
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "status_code": 400,
            "message": "Validation error",
            "error": [
                {
                    "loc": err["loc"],
                    "msg": err["msg"],
                    "type": err["type"],
                    "input": str(err.get("input")) if "input" in err else None,
                }
                for err in exc.errors()
            ],
        },
    )
