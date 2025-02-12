from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.domain.entities.genre import Genre


class GenreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Genre]:
        items = await self.session.execute(select(Genre))
        return items.scalars().all()

    async def get_item(self, id: int) -> Genre:
        item = await self.session.execute(select(Genre).where(Genre.id == id))
        return item.scalar()
