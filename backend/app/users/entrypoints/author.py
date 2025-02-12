from typing import List
from fastapi import APIRouter

from app.unit_of_work import UnitOfWork
from app.users.domain.entities.author import AuthorOut
from app.users.service.author import AuthorService


router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=List[AuthorOut])
async def get_authors():
    async with UnitOfWork() as uow:
        author_service = AuthorService()
        return await author_service.get_items(uow)


@router.get("/{id}", response_model=AuthorOut)
async def get_author(
    id: int,
):
    async with UnitOfWork() as uow:
        author_service = AuthorService()
        return await author_service.get_item(id, uow)
