from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.entities.client import Client, ClientCreate


class ClientRepository:
    async def get_all(self, db: AsyncSession) -> List[Client]:
        items = await db.execute(select(Client))
        return items.scalars().all()

    async def create_item(self, client: ClientCreate, db: AsyncSession) -> Client:
        print(client.model_dump())
        #new_client = Client()
        new_client = Client(**client.model_dump())

        db.add(new_client)
        return new_client
