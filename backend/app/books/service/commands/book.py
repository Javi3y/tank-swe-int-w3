from app.books.domain.entities.book import Book, BookCreate
from app.unit_of_work import UnitOfWork


async def delete_book_command(id: int, uow: UnitOfWork) -> None:
    repo = uow.book_repo
    await repo.delete_item(id)


async def create_book_command(book: BookCreate, uow: UnitOfWork) -> Book:
    repo = uow.book_repo
    new_book = await repo.create_item(book)
    return new_book
