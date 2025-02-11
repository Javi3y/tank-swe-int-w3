from typing import List
from app.users.domain.entities.author import Author

from app.unit_of_work import UnitOfWork


class AuthorService:
    async def get_items(self, uow: UnitOfWork) -> List[Author]:
        repo = uow.author_repo
        return await repo.get_all(uow.session)

    async def get_item(self, id: int, uow: UnitOfWork) -> Author:
        repo = uow.author_repo
        return await repo.get_item(id, uow.session)


async def get_author_service() -> AuthorService:
    return AuthorService()
