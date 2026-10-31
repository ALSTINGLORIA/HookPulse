from fastapi import FastAPI
from app.api.events import router as events_router

app = FastAPI(
    title="HookPulse",
    description="An API for submitting and tracking webhook events.",
    version="0.1.0",
)

app.include_router(events_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Webhook Delivery Engine!",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
    }