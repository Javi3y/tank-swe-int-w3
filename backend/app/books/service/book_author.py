from typing import List


from app.books.domain.entities.book_author import BookAuthor, BookAuthorCreate
from app.unit_of_work import UnitOfWork


class BookAuthorService:
    async def create_item(
        self, book_author: BookAuthorCreate, uow: UnitOfWork
    ) -> BookAuthor:
        repo = uow.book_author_repo
        new_book = await repo.create_item(book_author, uow.session)
        return new_book

    async def get_item(self, id: int, uow: UnitOfWork) -> BookAuthor:
        repo = uow.book_repo
        return await repo.get_item(id)

    async def delete_item(self, id: int, uow: UnitOfWork):
        repo = uow.book_repo
        return await repo.delete_item(id)


async def get_book_author_service() -> BookAuthorService:
    return BookAuthorService()
