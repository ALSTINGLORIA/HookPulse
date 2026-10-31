from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis

from app.schemas.event import EventCreate, EventResponse
from app.core.redis import get_redis
from app.services.event_service import create_event


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_202_ACCEPTED
)
async def submit_event(
    event_data: EventCreate,
    redis_client: Redis = Depends(get_redis)
):
    event_id = await create_event(
        event_data.model_dump(),
        redis_client
    )

    return EventResponse(
        event_id=event_id,
        status="pending",
        message="Event successfully received."
    )