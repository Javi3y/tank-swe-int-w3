from sqlalchemy.ext.asyncio import AsyncSession


from app.adapters.postgres import SessionLocal
from app.books.adapters.repositories.book import BookRepository
from app.books.adapters.repositories.genre import GenreRepository
from app.users.adapters.repositories.authors import AuthorRepository
from app.users.adapters.repositories.client import ClientRepository
from app.users.adapters.repositories.user import UserRepository


class UnitOfWork:
    def __init__(self):
        self.session: AsyncSession = SessionLocal()
        self.client_repo = ClientRepository()
        self.user_repo = UserRepository()
        self.author_repo = AuthorRepository()
        self.genre_repo = GenreRepository()
        self.book_repo = BookRepository()

    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def rollback(self):
        await self.session.rollback()

    async def refresh(self, item):
        await self.session.refresh(item)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()


async def get_uow() -> UnitOfWork:
    return UnitOfWork()
