from typing import List


from app.unit_of_work import UnitOfWork
from app.users.domain.entities.client import Client, ClientCreate, ClientUpdate


class ClientService:
    async def get_items(self, uow: UnitOfWork) -> List[Client]:
        repo = uow.client_repo
        return await repo.get_all(uow.session)

    async def create_item(self, client: ClientCreate, uow: UnitOfWork):
        repo = uow.client_repo
        new_client = await repo.create_item(client, uow.session)
        return new_client

    async def get_item(self, id: int, uow: UnitOfWork) -> Client:
        repo = uow.client_repo
        return await repo.get_item(id, uow.session)

    async def update_item(self, id: int, client: ClientUpdate, uow: UnitOfWork):
        repo = uow.client_repo
        return await repo.update_item(id, client, uow.session)

    async def delete_item(self, id: int, uow: UnitOfWork):
        repo = uow.client_repo
        return await repo.delete_item(id, uow.session)


async def get_client_service() -> ClientService:
    return ClientService()
