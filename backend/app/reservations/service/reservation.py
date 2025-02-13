from datetime import UTC, datetime, timedelta
from typing import List

from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.events.domain.entities.event import EventCreate
from app.events.domain.enums.event_type import EventTypeEnum
from app.reservations.domain.entities.reservation import Reservation, ReservationCreate
from app.unit_of_work import UnitOfWork
from app.users.domain.enums.sub import SubEnum
from app.users.service.client import ClientService
import json


class ReservationService:
    async def get_items(self, uow: UnitOfWork) -> List[Reservation]:
        repo = uow.reservation_repo
        return await repo.get_all()

    async def create_item(self, reservation: ReservationCreate, uow: UnitOfWork):
        repo = uow.reservation_repo
        new_client = await repo.create_item(reservation)
        return new_client

    async def get_item(self, id: int, uow: UnitOfWork) -> Reservation:
        repo = uow.reservation_repo
        return await repo.get_item(id)

    async def get_reservations(self, id: id, uow: UnitOfWork) -> List[Reservation]:
        reservation_repo = uow.reservation_repo
        return await reservation_repo.get_client_all(id)

    async def reserve_or_queue(self, book_id: int, uow: UnitOfWork):
        book_repo = uow.book_repo
        book = await book_repo.get_item(book_id)
        if not book:
            raise HTTPException(HTTP_404_NOT_FOUND)
        return True if book.units > 0 else False

    async def can_reserve(
        self, id: int, reservations: List[Reservation], uow: UnitOfWork
    ) -> None:
        client_service = ClientService()
        reservations_count = len(reservations)
        sub = await client_service.get_subscription(id, uow)
        if not sub:
            raise HTTPException(
                HTTP_403_FORBIDDEN, detail="purchase a subscription to reserve"
            )
        if sub == SubEnum.plus:
            if reservations_count >= 5:
                raise HTTPException(
                    HTTP_403_FORBIDDEN, detail="you can't reserve any more books"
                )
        if sub == SubEnum.premium:
            if reservations_count >= 10:
                raise HTTPException(
                    HTTP_403_FORBIDDEN, detail="you can't reserve any more books"
                )

    async def reserve(
        self, client_id: int, book_id: int, uow: UnitOfWork
    ) -> Reservation:
        prev_reservations = await self.get_reservations(client_id, uow)
        await self.can_reserve(client_id, prev_reservations, uow)
        if self.reserve_or_queue(book_id, uow):
            start = datetime.now(UTC)
            end = datetime.now(UTC) + timedelta(days=7)
            new_reservation = await self.create_item(
                ReservationCreate(
                    res_start=start, res_end=end, book_id=book_id, client_id=client_id
                ),
                uow,
            )
            event_repo = uow.event_repo
            payload = json.dumps(
                {
                    "reservation": new_reservation.id,
                    "book": book_id,
                    "client": client_id,
                },
                indent=4,
            )
            await event_repo.create_item(
                EventCreate(
                    timestamp=end, payload=payload, event_type=EventTypeEnum.reservation
                )
            )
            return new_reservation
        else:
            pass

    async def get_by_book_client(
        self, client_id: int, book_id: int, uow: UnitOfWork
    ) -> Reservation:
        repo = uow.reservation_repo
        return await repo.get_by_book_client(book_id, client_id)

    async def return_reservation(self, client_id: int, book_id: int, uow: UnitOfWork):
        event_repo = uow.event_repo
        reservation_repo = uow.reservation_repo
        reservation = await self.get_by_book_client(client_id, book_id, uow)
        await reservation_repo.return_item(reservation)
        event = await event_repo.get_item(reservation.id)
        await event_repo.change_time(
            event.id, datetime.now(UTC) + timedelta(seconds=70)
        )

    # async def delete_item(self, id: int, uow: UnitOfWork):
    #    repo = uow.reservation_repo
    #    return await repo.delete_item(id)


async def get_reservation_service() -> ReservationService:
    return ReservationService()
