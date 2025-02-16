from datetime import UTC, datetime, timedelta
from app.events.domain.entities.event import EventCreate
from app.events.domain.enums.event_type import EventTypeEnum
from app.reservations.domain.entities.reservation import Reservation, ReservationCreate
from app.reservations.domain.entities.reservation_queue import ReservationQueueCreate
from app.reservations.service.query.reservation import (
    can_reserve,
    get_by_book_client_query,
    get_reservations_by_client_query,
    reserve_or_queue,
)
from app.unit_of_work import UnitOfWork
import json


async def create_reservation_command(
    reservation: ReservationCreate, uow: UnitOfWork
) -> Reservation:
    repo = uow.reservation_repo
    new_client = await repo.create_item(reservation)
    return new_client


async def reserve_command(client_id: int, book_id: int, uow: UnitOfWork) -> Reservation:
    prev_reservations = await get_reservations_by_client_query(client_id, uow)
    await can_reserve(client_id, prev_reservations, uow)
    can = await reserve_or_queue(book_id, uow)
    print("can or not",can )
    if await reserve_or_queue(book_id, uow):
        start = datetime.now(UTC)
        end = datetime.now(UTC) + timedelta(days=7)
        new_reservation = await create_reservation_command(
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
        reservation_queue_repo = uow.reservation_queue_repo
        new_reservation_queue = await reservation_queue_repo.create_item(
            ReservationQueueCreate(book_id=book_id, client_id=client_id)
        )
        return new_reservation_queue


async def return_reservation_command(client_id: int, book_id: int, uow: UnitOfWork):
    event_repo = uow.event_repo
    reservation_repo = uow.reservation_repo
    reservation = await get_by_book_client_query(client_id, book_id, uow)
    await reservation_repo.return_item(reservation)
    event = await event_repo.get_item(reservation.id)
    await event_repo.change_time(event.id, datetime.now(UTC) + timedelta(seconds=70))
