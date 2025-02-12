from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.entities.client import Client, ClientCreate, ClientUpdate


class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Client]:
        items = await self.session.execute(select(Client))
        return items.scalars().all()

    async def create_item(self, client: ClientCreate) -> Client:
        data = client.model_dump()
        new_client = Client(**data)
        self.session.add(new_client)
        await self.session.flush()

        return new_client

    async def get_item(self, id: int):
        item = await self.session.execute(select(Client).where(Client.id == id))
        return item.scalar()

    async def update_item(self, id: int, client: ClientUpdate):
        current_client = await self.get_item(id)
        client_dict = client.model_dump(exclude_none=True)
        current_client.update(client_dict)
        return current_client

    async def delete_item(self, id: int):
        client = await self.get_item(id)
        await self.session.delete(client)
