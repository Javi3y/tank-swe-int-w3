from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reservations.domain.entities.reservation import Reservation, ReservationCreate


class ReservationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Reservation]:
        items = await self.session.execute(select(Reservation))
        return items.scalars().all()

    async def create_item(self, reservation: ReservationCreate) -> Reservation:
        data = reservation.model_dump()
        new_reservation = Reservation(**data)
        self.session.add(new_reservation)
        await self.session.flush()

        return new_reservation

    async def get_item(self, id: int) -> Reservation:
        item = await self.session.execute(
            select(Reservation).where(Reservation.id == id)
        )
        return item.scalar()

    async def get_client_all(self, client_id: int) -> List[Reservation]:
        items = await self.session.execute(
            select(Reservation).where(Reservation.client_id == client_id)
        )
        return items.scalars().all()

    async def get_by_book_client(self, client_id: int, book_id: int):
        item = await self.session.execute(
            select(Reservation)
            .where(Reservation.returned == False)
            .where(Reservation.book_id == book_id)
            .where(Reservation.client_id == client_id)
        )
        item = item.scalar()
        print(item)
        return item

    async def return_item(self,reservation: Reservation):
        reservation.return_item()
        await self.session.flush()



#    async def delete_item(self, id: int):
#        client = await self.get_item(id)
#        await self.session.delete(client)
