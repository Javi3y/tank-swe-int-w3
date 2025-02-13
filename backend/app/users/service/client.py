from typing import List


from app.unit_of_work import UnitOfWork
from app.users.domain.entities.client import Client, ClientCreate, ClientUpdate
from app.users.domain.enums.sub import SubEnum


class ClientService:
    async def get_items(self, uow: UnitOfWork) -> List[Client]:
        repo = uow.client_repo
        return await repo.get_all()

    async def create_item(self, client: ClientCreate, uow: UnitOfWork):
        repo = uow.client_repo
        new_client = await repo.create_item(client)
        return new_client

    async def get_item(self, id: int, uow: UnitOfWork) -> Client:
        repo = uow.client_repo
        return await repo.get_item(id)

    async def update_item(self, id: int, client: ClientUpdate, uow: UnitOfWork):
        repo = uow.client_repo
        return await repo.update_item(id, client)

    async def delete_item(self, id: int, uow: UnitOfWork):
        repo = uow.client_repo
        return await repo.delete_item(id)

    async def get_subscription(self, id: int, uow: UnitOfWork) -> SubEnum | None:
        client = await self.get_item(id, uow)
        if client.current_subscription:
            return client.current_subscription.subscription_model
        return None


async def get_client_service() -> ClientService:
    return ClientService()
