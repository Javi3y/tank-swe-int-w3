from typing import List
from app.unit_of_work import UnitOfWork
from app.users.domain.entities.author import Author


async def get_authors_query(uow: UnitOfWork) -> List[Author]:
    repo = uow.author_repo
    return await repo.get_all()


async def get_author_query(id: int, uow: UnitOfWork) -> Author:
    repo = uow.author_repo
    return await repo.get_item(id)
