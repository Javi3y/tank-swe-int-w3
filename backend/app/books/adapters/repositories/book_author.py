from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.domain.entities.book_author import BookAuthor, BookAuthorCreate


class BookAuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_item(
        self, book_author: BookAuthorCreate, db: AsyncSession
    ) -> BookAuthor:
        data = book_author.model_dump()
        new_book = BookAuthor(**data)
        db.add(new_book)
        await db.flush()

        return new_book

    async def get_item(self, id: int, db: AsyncSession):
        item = await db.execute(select(BookAuthor).where(BookAuthor.id == id))
        return item.scalar()

    async def delete_item(self, id: int, db: AsyncSession):
        book_author = await self.get_item(id, db)
        await db.delete(book_author)
