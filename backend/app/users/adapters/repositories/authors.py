from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.entities.author import Author


class AuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Author]:
        items = await self.session.execute(select(Author))
        return items.scalars().all()

    async def get_item(self, id: int):
        item = await self.session.execute(select(Author).where(Author.id == id))
        return item.scalar()
