from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.entities.client import Client, ClientCreate, ClientUpdate


class ClientRepository:
    async def get_all(self, db: AsyncSession) -> List[Client]:
        items = await db.execute(select(Client))
        return items.scalars().all()

    async def create_item(self, client: ClientCreate, db: AsyncSession) -> Client:
        data = client.model_dump()
        new_client = Client(**data)
        db.add(new_client)
        await db.flush()

        return new_client

    async def get_item(self, id: int, db: AsyncSession):
        item = await db.execute(select(Client).where(Client.id == id))
        return item.scalar()

    async def update_item(self, id: int, client: ClientUpdate, db: AsyncSession):
        current_client = await self.get_item(id, db)
        client_dict = client.model_dump(exclude_none=True)
        current_client.update(client_dict)
        return current_client

    async def delete_item(self, id: int, db: AsyncSession):
        client = await self.get_item(id, db)
        await db.delete(client)
