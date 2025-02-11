from typing import List


from app.books.domain.entities.book import Book, BookCreate
from app.unit_of_work import UnitOfWork


class BookService:
    async def get_items(self, uow: UnitOfWork) -> List[Book]:
        repo = uow.book_repo
        return await repo.get_all(uow.session)

    async def create_item(self, book: BookCreate, uow: UnitOfWork) -> Book:
        repo = uow.book_repo
        new_book = await repo.create_item(book, uow.session)
        return new_book

    async def get_item(self, id: int, uow: UnitOfWork) -> Book:
        repo = uow.book_repo
        return await repo.get_item(id, uow.session)

    #async def update_item(self, id: int, client: ClientUpdate, uow: UnitOfWork):
    #    repo = uow.client_repo
    #    return await repo.update_item(id, client, uow.session)

    async def delete_item(self, id: int, uow: UnitOfWork):
        repo = uow.book_repo
        return await repo.delete_item(id, uow.session)


async def get_book_service() -> BookService:
    return BookService()
