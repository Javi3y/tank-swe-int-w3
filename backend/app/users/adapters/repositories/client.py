from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.entities.client import Client




class ClientRepository:
    session: AsyncSession
    def __init__(self, session):
        self.session = session

    async def get_all(self, db):
        items = await db.execute(select(Client))
        return items.scalars().all()
