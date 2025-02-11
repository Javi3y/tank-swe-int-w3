from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.domain.entities.genre import Genre


class GenreRepository:
    async def get_all(self, db: AsyncSession) -> List[Genre]:
        items = await db.execute(select(Genre))
        return items.scalars().all()

    async def get_item(self, id: int, db: AsyncSession) -> Genre:
        item = await db.execute(select(Genre).where(Genre.id == id))
        return item.scalar()
