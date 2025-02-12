from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.domain.entities.book_author import BookAuthor, BookAuthorCreate


class BookAuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_item(
        self, book_author: BookAuthorCreate
    ) -> BookAuthor:
        data = book_author.model_dump()
        new_book = BookAuthor(**data)
        self.session.add(new_book)
        await self.session.flush()

        return new_book

    async def get_item(self, id: int):
        item = await self.session.execute(select(BookAuthor).where(BookAuthor.id == id))
        return item.scalar()

    async def get_with_book_author(
        self, book_id: int, author_id: int
    ):
        item = await self.session.execute(
            select(BookAuthor)
            .where(BookAuthor.book_id == book_id)
            .where(BookAuthor.author_id == author_id)
        )
        item = item.scalar()
        return item 

    async def delete_item(self, id: int):
        book_author = await self.get_item(id)
        await self.session.delete(book_author)
