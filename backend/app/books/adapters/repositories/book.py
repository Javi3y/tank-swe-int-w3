from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.domain.entities.book import Book, BookCreate


class BookRepository:
    async def get_all(self, db: AsyncSession) -> List[Book]:
        items = await db.execute(select(Book))
        return items.scalars().all()

    async def create_item(self, book: BookCreate, db: AsyncSession) -> Book:
        data = book.model_dump()
        new_book = Book(**data)
        db.add(new_book)
        await db.flush()

        return new_book

    async def get_item(self, id: int, db: AsyncSession):
        item = await db.execute(select(Book).where(Book.id == id))
        return item.scalar()

    # async def update_item(self, id: int, client: ClientUpdate, db: AsyncSession):
    #    current_client = await self.get_item(id, db)
    #    client_dict = client.model_dump(exclude_none=True)
    #    current_client.update(client_dict)
    #    return current_client

    async def delete_item(self, id: int, db: AsyncSession):
        client = await self.get_item(id, db)
        await db.delete(client)
