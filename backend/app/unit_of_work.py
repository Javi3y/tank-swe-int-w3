from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.adapters.postgres import SessionLocal
from app.users.adapters.repositories.client import ClientRepository

class UnitOfWork:
    def __init__(self):
        self.session: AsyncSession = SessionLocal()
        self.client_repo = ClientRepository()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

async def get_uow() -> UnitOfWork:
    return UnitOfWork()


