from typing import List
from fastapi import APIRouter, Depends

from app.unit_of_work import UnitOfWork, get_uow
from app.users.domain.entities.author import AuthorOut
from app.users.domain.entities.client import ClientOut
from app.users.service.author import AuthorService
from app.auth.service.dependencies.permissions import current_user_or_admin


router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=List[AuthorOut])
async def get_authors(
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        author_service = AuthorService()
        return await author_service.get_items(uow)


@router.get("/{id}", response_model=AuthorOut)
async def get_client(
    id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        author_service = AuthorService()
        return await author_service.get_item(id, uow)
