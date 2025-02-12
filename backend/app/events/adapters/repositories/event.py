from datetime import UTC, datetime, timedelta
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.events.domain.entities.event import Event, EventCreate
from app.events.domain.enums.event_status import EventStatusEnum


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Event]:
        items = await self.session.execute(select(Event))
        return items.scalars().all()

    async def create_item(self, client: EventCreate) -> Event:
        data = client.model_dump()
        new_event = Event(**data)
        self.session.add(new_event)
        await self.session.flush()

        return new_event

    async def get_item(self, id: int) -> Event:
        item = await self.session.execute(select(Event).where(Event.id == id))
        return item.scalar()

    async def delete_item(self, id: int) -> Event:
        event = await self.get_item(id)
        event.delete()
        await self.session.flush()
        return event

    async def cancel_item(self, id: int) -> Event:
        event = await self.get_item(id)
        event.cancel()
        await self.session.flush()
        return event

    async def fail_item(self, id: int) -> Event:
        event = await self.get_item(id)
        event.fail()
        await self.session.flush()
        return event

    async def resolve_item(self, id: int) -> Event:
        event = await self.get_item(id)
        event.resolve()
        await self.session.flush()
        return event

    async def get_current_pending(self) -> List[Event]:
        items = await self.session.execute(
            select(Event)
            .where(Event.event_status == EventStatusEnum.pending)
            .where(Event.timestamp >= datetime.now(UTC))
            .where(Event.timestamp <= datetime.now(UTC) + timedelta(seconds=61))
        )
        return items.scalars().all()
