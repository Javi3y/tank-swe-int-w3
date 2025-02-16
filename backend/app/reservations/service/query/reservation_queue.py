from typing import List

from app.reservations.domain.entities.reservation_queue import ReservationQueue
from app.unit_of_work import UnitOfWork


async def get_latest_reservation_queue_query(book_id: int, uow: UnitOfWork) -> List[ReservationQueue]:
    repo = uow.reservation_queue_repo
    return await repo.get_latest(book_id)

