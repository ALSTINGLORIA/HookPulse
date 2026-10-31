import json
import uuid

from redis.asyncio import Redis


async def create_event(
    event_data: dict,
    redis_client: Redis
):
    event_id = str(uuid.uuid4())

    event = {
        "event_id": event_id,
        "event_type": event_data["event_type"],
        "target_url": str(event_data["target_url"]),
        "payload": event_data["payload"],
        "status": "pending",
        "attempts": 0
    }

    await redis_client.set(
        f"event:{event_id}",
        json.dumps(event)
    )

    return event_id