from datetime import UTC, datetime, timedelta
from app.events.domain.entities.event import EventCreate
from app.events.domain.enums.event_type import EventTypeEnum
from app.reservations.domain.entities.reservation import ReservationCreate
from app.reservations.domain.entities.reservation_queue import ReservationQueue
from app.reservations.service.commands.reservation import create_reservation_command
from app.reservations.service.query.reservation import (
    can_reserve,
    get_reservations_by_client_query,
    reserve_or_queue,
)
from app.reservations.service.query.reservation_queue import (
    get_latest_reservation_queue_query,
)
from app.unit_of_work import UnitOfWork
import json
from app.users.service.commands.client import delete_client_command


async def delete_reservation_queue_command(
    reservation: ReservationQueue, uow: UnitOfWork
):
    repo = uow.reservation_queue_repo
    await repo.delete_item(reservation.id)


async def resolve_reservation_command(book_id: int, uow: UnitOfWork):
    print(book_id)
    reservation = await get_latest_reservation_queue_query(book_id, uow)
    print(reservation)
    if reservation:
        prev_reservations = await get_reservations_by_client_query(
            reservation.client_id, uow
        )
        try:
            await can_reserve(reservation.client_id, prev_reservations, uow)
        except Exception:
            await delete_reservation_queue_command(reservation, uow)
            return None

        book_repo = uow.book_repo
        book = await book_repo.get_item(book_id)
        book.increment_units()
        await uow.flush()
        await uow.refresh(book)

        start = datetime.now(UTC)
        end = datetime.now(UTC) + timedelta(days=7)
        new_reservation = await create_reservation_command(
            ReservationCreate(
                res_start=start,
                res_end=end,
                book_id=book_id,
                client_id=reservation.client_id,
            ),
            uow,
        )
        event_repo = uow.event_repo
        payload = json.dumps(
            {
                "reservation": new_reservation.id,
                "book": book_id,
                "client": reservation.client_id,
            },
            indent=4,
        )
        book_repo = uow.book_repo
        book = await book_repo.get_item(book_id)
        book.decrement_units()
        await uow.flush()
        await uow.refresh(book)
        await event_repo.create_item(
            EventCreate(
                timestamp=end, payload=payload, event_type=EventTypeEnum.reservation
            )
        )
        await delete_reservation_queue_command(reservation, uow)
        return new_reservation
    else:
        book_repo = uow.book_repo
        book = await book_repo.get_item(book_id)
        book.increment_units()
        await uow.flush()
        await uow.refresh(book)
        return None
