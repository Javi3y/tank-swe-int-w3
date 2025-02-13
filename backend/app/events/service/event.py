from typing import List

from app.unit_of_work import UnitOfWork


class EventService:
    pass


async def get_event_service() -> EventService:
    return EventService()
