from fastapi import FastAPI
from app.routers import subscriptions, notifications

app = FastAPI()

app.include_router(subscriptions.router)
app.include_router(notifications.router) 