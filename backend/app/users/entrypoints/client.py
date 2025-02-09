from fastapi import APIRouter, Depends

from app.unit_of_work import UnitOfWork, get_uow
from app.users.domain.entities.client import ClientCreate, ClientOut
from app.users.service.client import ClientService


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/")
async def get_clients(
    # client_service: ClientService = Depends(get_client_service),
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        client_service = ClientService()
        return await client_service.get_items(uow)


@router.post("/", response_model=ClientOut)
async def create_clients(
    # client_service: ClientService = Depends(get_client_service),
    client: ClientCreate,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        client_service = ClientService()
        return await client_service.create_item(client, uow)
