from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.entities.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_item(self, id: int) -> User:
        item = await self.session.execute(select(User).where(User.id == id))
        return item.scalar()

    async def get_by_user_or_email(self, username) -> User | None:
        results = await self.session.execute(
            select(User).where((User.username == username) | (User.email == username))
        )
        return results.scalar()
