from fastapi import APIRouter, Depends

from app.auth.service.auth import get_current_user
from app.reservations.domain.entities.reservation import ReservationOut
from app.reservations.service.reservation import ReservationService
from app.unit_of_work import UnitOfWork
from app.auth.service.dependencies.permissions import (
    CurrentUser,
    client_permission,
)
from app.users.domain.entities.user import User


router = APIRouter(prefix="/reservation", tags=["Reservation"])


@router.post(
    "/{book_id}",
    response_model=ReservationOut,
    dependencies=[Depends(client_permission)],
)
async def reserve(book_id: int, client: User = Depends(get_current_user)):
    async with UnitOfWork() as uow:
        reservation_service = ReservationService()
        reservation = await reservation_service.reserve(client.id, book_id, uow)
        await uow.commit()
        await uow.refresh(reservation)
        return reservation
