from app.books.domain.entities.book_author import BookAuthor, BookAuthorCreate
from app.unit_of_work import UnitOfWork


class BookAuthorService:
    async def create_item(
        self, book_author: BookAuthorCreate, uow: UnitOfWork
    ) -> BookAuthor:
        repo = uow.book_author_repo
        new_book = await repo.create_item(book_author)
        return new_book

    async def get_with_book_author(
        self, book_id: int, author_id: int, uow: UnitOfWork
    ) -> BookAuthor:
        repo = uow.book_author_repo
        return await repo.get_with_book_author(book_id, author_id)

    async def delete_item(self, book_id, author_id, uow: UnitOfWork):
        repo = uow.book_author_repo
        id = await self.get_with_book_author(book_id, author_id, uow)
        return await repo.delete_item(id.id)
