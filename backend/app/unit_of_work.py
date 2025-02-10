from sqlalchemy.ext.asyncio import AsyncSession


from app.adapters.postgres import SessionLocal
from app.users.adapters.repositories.client import ClientRepository
from app.users.adapters.repositories.user import UserRepository


class UnitOfWork:
    def __init__(self):
        self.session: AsyncSession = SessionLocal()
        self.client_repo = ClientRepository()
        self.user_repo = UserRepository()

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
