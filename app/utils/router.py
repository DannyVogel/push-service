from fastapi import APIRouter, Depends
from app.dependencies import verify_api_key

def create_protected_router():
    return APIRouter(
        prefix="/api",
        dependencies=[Depends(verify_api_key)]
    )

def create_logger_router():
    return APIRouter(
        prefix="/logs",
        dependencies=[Depends(verify_api_key)]
    )
