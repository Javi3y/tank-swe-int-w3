from sqlalchemy.ext.asyncio import AsyncSession


from app.adapters.postgres import SessionLocal
from app.books.adapters.repositories.book import BookRepository
from app.books.adapters.repositories.book_author import BookAuthorRepository
from app.books.adapters.repositories.genre import GenreRepository
from app.events.adapters.repositories.event import EventRepository
from app.users.adapters.repositories.authors import AuthorRepository
from app.users.adapters.repositories.client import ClientRepository
from app.users.adapters.repositories.user import UserRepository
from app.reservations.adapters.repositories.reservation import ReservationRepository
from app.reservations.adapters.repositories.reservation_queue import (
    ReservationQueueRepository,
)


class UnitOfWork:
    def __init__(self):
        self.session: AsyncSession = SessionLocal()

        self.client_repo = ClientRepository(self.session)
        self.user_repo = UserRepository(self.session)
        self.author_repo = AuthorRepository(self.session)
        self.genre_repo = GenreRepository(self.session)
        self.book_repo = BookRepository(self.session)
        self.book_author_repo = BookAuthorRepository(self.session)
        self.reservation_repo = ReservationRepository(self.session)
        self.reservation_queue_repo = ReservationQueueRepository(self.session)
        self.event_repo = EventRepository(self.session)

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

    async def __aexit__(self, exc_type, _exc_val, _exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()


async def get_uow() -> UnitOfWork:
    return UnitOfWork()
