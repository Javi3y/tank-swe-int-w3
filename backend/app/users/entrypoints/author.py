from typing import List
from fastapi import APIRouter

from app.unit_of_work import UnitOfWork
from app.users.domain.entities.author import AuthorOut
from app.users.service.query.author import get_author_query, get_authors_query


router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=List[AuthorOut])
async def get_authors():
    async with UnitOfWork() as uow:
        return await get_authors_query(uow)


@router.get("/{id}", response_model=AuthorOut)
async def get_author(
    id: int,
):
    async with UnitOfWork() as uow:
        return await get_author_query(id, uow)
