from typing import List

from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.reservations.domain.entities.reservation import Reservation
from app.unit_of_work import UnitOfWork
from app.users.domain.enums.sub import SubEnum
from app.users.service.query.client import get_subscription_query


async def get_reservations_query(uow: UnitOfWork) -> List[Reservation]:
    repo = uow.reservation_repo
    return await repo.get_all()


async def get_reservation_query(id: int, uow: UnitOfWork) -> Reservation:
    repo = uow.reservation_repo
    return await repo.get_item(id)


async def get_reservations_by_client_query(
    client_id: int, uow: UnitOfWork
) -> List[Reservation]:
    reservation_repo = uow.reservation_repo
    return await reservation_repo.get_client_all(client_id)


async def reserve_or_queue(book_id: int, uow: UnitOfWork):
    book_repo = uow.book_repo
    book = await book_repo.get_item(book_id)
    if not book:
        raise HTTPException(HTTP_404_NOT_FOUND)
    return True if book.units > 0 else False


async def can_reserve(
    id: int, reservations: List[Reservation], uow: UnitOfWork
) -> None:
    # I have to fix this later
    reservations_count = len(reservations)
    sub = await get_subscription_query(id, uow)
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


async def get_by_book_client_query(
    client_id: int, book_id: int, uow: UnitOfWork
) -> Reservation:
    repo = uow.reservation_repo
    return await repo.get_by_book_client(client_id, book_id)
