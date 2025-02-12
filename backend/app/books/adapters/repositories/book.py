from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.books.domain.entities.book import Book, BookCreate


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Book]:
        #items = await self.session.execute(select(Book).options(joinedload(Book.authors)))
        items = await self.session.execute(select(Book))
        # return [x for x in items.scalars().all()]
        items = items.scalars().all()
        return items

    async def create_item(self, book: BookCreate) -> Book:
        data = book.model_dump()
        new_book = Book(**data)
        self.session.add(new_book)
        await self.session.flush()

        return new_book

    async def get_item(self, id: int):
        item = await self.session.execute(select(Book).where(Book.id == id))
        return item.scalar()

    # async def update_item(self, id: int, client: ClientUpdate, db: AsyncSession):
    #    current_client = await self.get_item(id, db)
    #    client_dict = client.model_dump(exclude_none=True)
    #    current_client.update(client_dict)
    #    return current_client

    async def delete_item(self, id: int):
        client = await self.get_item(id)
        await self.session.delete(client)
