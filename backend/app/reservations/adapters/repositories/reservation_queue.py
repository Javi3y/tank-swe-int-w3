from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reservations.domain.entities.reservation_queue import (
    ReservationQueue,
    ReservationQueueCreate,
)


class ReservationQueueRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[ReservationQueue]:
        items = await self.session.execute(select(ReservationQueue))
        return items.scalars().all()

    async def create_item(
        self, reservation_queue: ReservationQueueCreate
    ) -> ReservationQueue:
        data = reservation_queue.model_dump()
        new_reservation_queue = ReservationQueue(**data)
        self.session.add(new_reservation_queue)
        await self.session.flush()

        return new_reservation_queue

    async def get_item(self, id: int) -> ReservationQueue:
        item = await self.session.execute(
            select(ReservationQueue).where(ReservationQueue.id == id)
        )
        return item.scalar()


#    async def delete_item(self, id: int):
#        client = await self.get_item(id)
#        await self.session.delete(client)
