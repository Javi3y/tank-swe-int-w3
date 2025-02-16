from typing import List
from sqlalchemy import select, text
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

    async def get_latest(self, book_id: int) -> ReservationQueue:
        query = await self.session.execute(
            text(
                f"""
            WITH RankedReservations AS (
                SELECT
                    rq.id,
                    rq.book_id,
                    rq.client_id,
                    rq.created_at,
                    ROW_NUMBER() OVER (
                        PARTITION BY rq.book_id
                        ORDER BY
                            CASE
                                WHEN s.subscription_model = 'premium' THEN 1
                                WHEN s.subscription_model = 'plus' THEN 2
                                ELSE 3
                            END,
                            rq.created_at
                    ) AS rank
                FROM reservation_queue rq
                JOIN client c ON rq.client_id = c.id
                JOIN subscription s ON c.id = s.client_id
            )
            SELECT id, book_id, client_id, created_at
            FROM RankedReservations
            WHERE rank = { book_id }
            """
            )
        )
        result = query.fetchone()
        if not result:
            return None
        reservation = await self.get_item(result.id)

        return reservation


#    async def delete_item(self, id: int):
#        client = await self.get_item(id)
#        await self.session.delete(client)
