from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.unit_of_work import UnitOfWork
from app.users.adapters.repositories.client import ClientRepository
from app.users.domain.entities.client import Client


class ClientService():
    async def get_items(self, uow:UnitOfWork, db:AsyncSession) ->List[Client]:
        repo = uow.get_repository(ClientRepository)
        return await repo.get_all(db)

async def get_client_service() -> ClientService:
    return ClientService()

