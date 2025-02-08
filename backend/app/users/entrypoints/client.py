from fastapi import APIRouter, Depends

from app.unit_of_work import UnitOfWork, get_uow
from app.users.service.client import ClientService, get_client_service


router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/")
async def get_clients(
    client_service: ClientService = Depends(get_client_service),
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow :
        return await client_service.get_items(uow, uow.session)

