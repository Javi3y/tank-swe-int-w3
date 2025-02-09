from typing import List


from app.unit_of_work import UnitOfWork
from app.users.domain.entities.client import Client, ClientCreate


class ClientService:
    async def get_items(self, uow: UnitOfWork) -> List[Client]:
        repo = uow.client_repo
        return await repo.get_all(uow.session)

    async def create_item(self, client: ClientCreate, uow: UnitOfWork):
        repo = uow.client_repo
        return await repo.create_item(client, uow.session)


async def get_client_service() -> ClientService:
    return ClientService()
