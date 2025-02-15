from app.unit_of_work import UnitOfWork
from app.users.domain.entities.client import ClientCreate, ClientUpdate


async def create_client_command(client: ClientCreate, uow: UnitOfWork):
    repo = uow.client_repo
    new_client = await repo.create_item(client)
    return new_client


async def update_client_command(id: int, client: ClientUpdate, uow: UnitOfWork):
    repo = uow.client_repo
    return await repo.update_item(id, client)


async def delete_client_command(id: int, uow: UnitOfWork):
    repo = uow.client_repo
    return await repo.delete_item(id)
