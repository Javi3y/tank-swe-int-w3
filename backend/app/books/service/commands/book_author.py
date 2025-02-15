from app.books.domain.entities.book_author import BookAuthor, BookAuthorCreate
from app.books.service.query.book_author import get_with_book_author
from app.unit_of_work import UnitOfWork


async def delete_book_author_command(book_id, author_id, uow: UnitOfWork):
    repo = uow.book_author_repo
    id = await get_with_book_author(book_id, author_id, uow)
    return await repo.delete_item(id.id)


async def create_book_author_command(
    book_author: BookAuthorCreate, uow: UnitOfWork
) -> BookAuthor:
    repo = uow.book_author_repo
    new_book = await repo.create_item(book_author)
    return new_book
