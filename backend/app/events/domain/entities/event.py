from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel, Json

from app.events.domain.enums.event_status import EventStatusEnum
from app.events.domain.enums.event_type import EventTypeEnum


class Event:
    id: Optional[int]
    created_at: Optional[datetime] = datetime.now(UTC)

    def __init__(self, timestamp: datetime, payload: Json, event_type: EventTypeEnum):
        self.timestamp = timestamp
        self.payload = payload
        self.event_type = event_type
        self.event_status = EventStatusEnum.pending

    def __str__(self):
        return f"<Event {self.id}>"

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return other.id == self.id

    def delete(self):
        self.event_status = EventStatusEnum.deleted

    def cancel(self):
        self.event_status = EventStatusEnum.canceled

    def fail(self):
        self.event_status = EventStatusEnum.failed

    def resolve(self):
        self.event_status = EventStatusEnum.resolved


class EventBase(BaseModel):
    payload: Json
    event_type: EventTypeEnum
    timestamp: datetime


class EventCreate(EventBase):
    pass


class EventOut(EventBase):
    pass
