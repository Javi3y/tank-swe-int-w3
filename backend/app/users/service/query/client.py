from typing import List
from app.unit_of_work import UnitOfWork
from app.users.domain.entities.client import Client
from app.users.domain.enums.sub import SubEnum


async def get_clients_query(uow: UnitOfWork) -> List[Client]:
    repo = uow.client_repo
    return await repo.get_all()

async def get_client_query(id: int, uow: UnitOfWork) -> Client:
    repo = uow.client_repo
    return await repo.get_item(id)

async def get_subscription_query(id: int, uow: UnitOfWork) -> SubEnum | None:
    client = await get_client_query(id, uow)
    if client.current_subscription:
        return client.current_subscription.subscription_model
    return None
