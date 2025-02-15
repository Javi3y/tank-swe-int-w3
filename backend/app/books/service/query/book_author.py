from app.books.domain.entities.book_author import BookAuthor
from app.unit_of_work import UnitOfWork


async def get_item(id: int, uow: UnitOfWork) -> BookAuthor:
    repo = uow.book_author_repo
    return await repo.get_item(id)


async def get_with_book_author(
    book_id: int, author_id: int, uow: UnitOfWork
) -> BookAuthor:
    repo = uow.book_author_repo
    return await repo.get_with_book_author(book_id, author_id)
