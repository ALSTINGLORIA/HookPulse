import json
import os

import httpx
import redis

from app.core.celery_app import celery_app
from dotenv import load_dotenv
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)


@celery_app.task(name="deliver_event")
def deliver_event(event_id: str):

    event_key = f"event:{event_id}"

    event_data = redis_client.get(event_key)

    if event_data is None:
        raise ValueError(f"Event {event_id} not found")

    event = json.loads(event_data)

    target_url = event["target_url"]
    payload = event["payload"]

    try:

        response = httpx.post(
            target_url,
            json=payload,
            timeout=10.0
        )

        response.raise_for_status()

        event["status"] = "delivered"

        redis_client.set(
            event_key,
            json.dumps(event)
        )

        return {
            "event_id": event_id,
            "status": "delivered"
        }

    except httpx.HTTPError as error:

        event["status"] = "failed"

        redis_client.set(
            event_key,
            json.dumps(event)
        )

        raise error