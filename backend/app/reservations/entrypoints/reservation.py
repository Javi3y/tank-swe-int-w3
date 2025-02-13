from fastapi import APIRouter, Depends
from app.reservations.domain.entities.reservation import ReservationOut
from app.reservations.service.reservation import ReservationService
from app.unit_of_work import UnitOfWork
from app.auth.service.dependencies.permissions import (
    CurrentUser,
    client_permission,
)


router = APIRouter(prefix="/reservation", tags=["Reservation"])


@router.post(
    "/{book_id}",
    response_model=ReservationOut,
    dependencies=[Depends(client_permission)],
)
async def reserve(book_id: int, client: CurrentUser):
    async with UnitOfWork() as uow:
        reservation_service = ReservationService()
        reservation = await reservation_service.reserve(client.id, book_id, uow)
        await uow.commit()
        await uow.refresh(reservation)
        return reservation


@router.post("/{book_id}/return", dependencies=[Depends(client_permission)])
async def return_reservation(book_id: int, client: CurrentUser):
    async with UnitOfWork() as uow:
        reservation_service = ReservationService()
        await reservation_service.return_reservation(book_id, client.id, uow)
        await uow.commit()
        return {"msg": "book was returned successfully"}
