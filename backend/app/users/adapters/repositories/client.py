from sqlalchemy import select

from app.users.domain.entities.client import Client




class ClientRepository:
    async def get_all(self, db):
        items = await db.execute(select(Client))
        return items.scalars().all()
