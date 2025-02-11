from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.entities.user import User


class UserRepository:
    async def get_item(self, id: int, db: AsyncSession) -> User:
        item = await db.execute(select(User).where(User.id == id))
        return item.scalar()

    async def get_by_user_or_email(self, username, db: AsyncSession) -> User:
        results = await db.execute(
            select(User).where((User.username == username) | (User.email == username))
        )
        return results.scalar()
