from pydantic import BaseModel, HttpUrl, Field
from typing import Any


class EventCreate(BaseModel):
    event_type: str = Field(min_length=1)
    target_url: HttpUrl
    payload: dict[str, Any]


class EventResponse(BaseModel):
    event_id: str
    status: str
    message: str