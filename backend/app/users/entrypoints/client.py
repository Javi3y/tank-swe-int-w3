from typing import List
from fastapi import APIRouter, Depends, Response
from starlette.status import HTTP_204_NO_CONTENT

from app.unit_of_work import UnitOfWork
from app.users.domain.entities.client import ClientCreate, ClientOut, ClientUpdate
from app.auth.service.dependencies.permissions import current_user_or_admin
from app.users.service.commands.client import create_client_command, delete_client_command, update_client_command
from app.users.service.query.client import get_client_query, get_clients_query


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=List[ClientOut])
async def get_clients():
    async with UnitOfWork() as uow:
        return await get_clients_query(uow)


@router.get("/{id}", response_model=ClientOut)
async def get_client(
    id: int,
):
    async with UnitOfWork() as uow:
        client = await get_client_query(id, uow)
        return client


@router.post("/", response_model=ClientOut)
async def create_clients(
    client: ClientCreate,
):
    async with UnitOfWork() as uow:
        new_client = await create_client_command(client, uow)
        await uow.commit()
        await uow.refresh(new_client)
        return new_client


@router.patch(
    "/{user_id}",
    response_model=ClientOut,
    dependencies=[Depends(current_user_or_admin)],
)
async def update_client(user_id: int, client: ClientUpdate):
    async with UnitOfWork() as uow:
        updated_client = await update_client_command(user_id, client, uow)
        await uow.commit()
        await uow.refresh(updated_client)
        return updated_client


@router.delete("/{user_id}", dependencies=[Depends(current_user_or_admin)])
async def delete_client(user_id: int):
    async with UnitOfWork() as uow:
        await delete_client_command(user_id, uow)
        await uow.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
