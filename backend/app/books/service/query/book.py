from typing import List
from app.books.domain.entities.book import Book
from app.unit_of_work import UnitOfWork


async def get_book_query(id: int, uow: UnitOfWork) -> Book:
    repo = uow.book_repo
    return await repo.get_item(id)


async def get_books_query(uow: UnitOfWork) -> List[Book]:
    repo = uow.book_repo
    books = await repo.get_all()
    return books
