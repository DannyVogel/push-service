from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routers import subscriptions, notifications

app = FastAPI()

app.include_router(subscriptions.router)
app.include_router(notifications.router) 

@app.get("/")
def read_root():
    return "Welcome to the Notification Service"


