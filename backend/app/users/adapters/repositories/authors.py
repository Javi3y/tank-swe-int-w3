from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.entities.author import Author


class AuthorRepository:
    async def get_all(self, db: AsyncSession) -> List[Author]:
        items = await db.execute(select(Author))
        return items.scalars().all()

    async def get_item(self, id: int, db: AsyncSession):
        item = await db.execute(select(Author).where(Author.id == id))
        return item.scalar()
