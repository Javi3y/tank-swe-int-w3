from typing import List
from fastapi import APIRouter, Depends, Response
from starlette.status import HTTP_204_NO_CONTENT

from app.unit_of_work import UnitOfWork, get_uow
from app.users.domain.entities.client import ClientCreate, ClientOut, ClientUpdate
from app.users.service.client import ClientService
from app.auth.service.dependencies.permissions import current_user_or_admin


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=List[ClientOut])
async def get_clients():
    async with UnitOfWork() as uow:
        client_service = ClientService()
        return await client_service.get_items(uow)


@router.get("/{id}", response_model=ClientOut)
async def get_client(
    id: int,
):
    async with UnitOfWork() as uow:
        client_service = ClientService()
        return await client_service.get_item(id, uow)


@router.post("/", response_model=ClientOut)
async def create_clients(
    client: ClientCreate,
):
    async with UnitOfWork() as uow:
        client_service = ClientService()
        client = await client_service.create_item(client, uow)
        await uow.commit()
        await uow.refresh(client)
        return client


@router.patch(
    "/{user_id}",
    response_model=ClientOut,
    dependencies=[Depends(current_user_or_admin)],
)
async def update_client(user_id: int, client: ClientUpdate):
    async with UnitOfWork() as uow:
        client_service = ClientService()
        client = await client_service.update_item(user_id, client, uow)
        await uow.commit()
        await uow.refresh(client)
        return client


@router.delete("/{user_id}", dependencies=[Depends(current_user_or_admin)])
async def delete_client(user_id: int):
    async with UnitOfWork() as uow:
        client_service = ClientService()
        await client_service.delete_item(user_id, uow)
        await uow.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
