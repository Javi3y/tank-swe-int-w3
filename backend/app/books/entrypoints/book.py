from typing import List
from fastapi import APIRouter, Depends, Response
from starlette.status import HTTP_204_NO_CONTENT

from app.books.domain.entities.book import BookCreate, BookOut
from app.books.service.book import BookService
from app.unit_of_work import UnitOfWork, get_uow


router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookOut])
async def get_books(
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        book_service = BookService()
        return await book_service.get_items(uow)


@router.get("/{id}", response_model=BookOut)
async def get_book(
    id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        book_service = BookService()
        return await book_service.get_item(id, uow)


@router.post("/", response_model=BookOut)
async def create_book(
    book: BookCreate,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        book_service = BookService()
        new_book = await book_service.create_item(book, uow)
        await uow.commit()
        await uow.refresh(new_book)
        return new_book


# @router.patch(
#    "/{user_id}",
#    response_model=ClientOut,
#    dependencies=[Depends(current_user_or_admin)],
# )
# async def update_client(
#    user_id: int, client: ClientUpdate, uow: UnitOfWork = Depends(get_uow)
# ):
#    async with uow:
#        client_service = ClientService()
#        client = await client_service.update_item(user_id, client, uow)
#        await uow.commit()
#        await uow.refresh(client)
#        return client


@router.delete("/{book_id}")
async def delete_book(book_id: int, uow: UnitOfWork = Depends(get_uow)):
    async with uow:
        book_service = BookService()
        await book_service.delete_item(book_id, uow)
        await uow.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
