from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.postgres import get_db

class UnitOfWork:
    def __init__(self, session:AsyncSession):
        self.session =session
        self.repositories = {}

    def get_repository(self, repo_class):
        if repo_class not in self.repositories:
            self.repositories[repo_class] = repo_class(self.session)
        return self.repositories[repo_class]

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

async def get_uow(db: AsyncSession = Depends(get_db)) -> UnitOfWork:
    return UnitOfWork(db)


