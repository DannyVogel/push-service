from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import subscriptions, notifications
from app.exceptions import http_exception_handler, validation_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(ALLOWED_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(subscriptions.router)
app.include_router(notifications.router) 

@app.get("/")
def read_root():
    return "Welcome to the Notification Service"