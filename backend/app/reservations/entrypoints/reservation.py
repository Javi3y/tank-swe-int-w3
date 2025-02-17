from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from app.reservations.domain.entities.reservation_queue import ReservationQueueOut
from app.reservations.service.commands.reservation import (
    reserve_command,
    return_reservation_command,
)
from app.reservations.service.commands.reservation_queue import (
    resolve_reservation_command,
)
from app.reservations.service.query.reservation_queue import (
    get_latest_reservation_queue_query,
)
from app.unit_of_work import UnitOfWork
from app.auth.service.dependencies.permissions import (
    CurrentUser,
    client_permission,
)


router = APIRouter(prefix="/reservation", tags=["Reservation"])


@router.post(
    "/{book_id}",
    # response_model=ReservationOut,
    dependencies=[Depends(client_permission)],
)
async def reserve(book_id: int, client: CurrentUser):
    async with UnitOfWork() as uow:
        reservation = await reserve_command(client.id, book_id, uow)
        await uow.commit()
        # await uow.refresh(reservation)
        # return reservation
        return {"msg": "done"}


@router.post("/{book_id}/return", dependencies=[Depends(client_permission)])
async def return_reservation(book_id: int, client: CurrentUser):
    async with UnitOfWork() as uow:
        await return_reservation_command(client.id, book_id, uow)
        await uow.commit()
        return {"msg": "book was returned successfully"}


@router.get("/{book_id}/latest", response_model=ReservationQueueOut)
async def get_latest(book_id: int):
    async with UnitOfWork() as uow:
        reservation = await get_latest_reservation_queue_query(book_id, uow)
        if not reservation:
            raise HTTPException(HTTP_404_NOT_FOUND)
        return reservation


@router.post("/{book_id}/resolve")
async def resolve_latest(book_id: int):
    async with UnitOfWork() as uow:
        reservation = await resolve_reservation_command(book_id, uow)
        await uow.commit()
        return reservation
