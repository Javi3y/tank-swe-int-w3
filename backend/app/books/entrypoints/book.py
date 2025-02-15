from typing import List
from fastapi import APIRouter, Depends, Response
from starlette.status import HTTP_204_NO_CONTENT

from app.auth.service.dependencies.permissions import current_author_or_admin
from app.books.domain.entities.book import BookCreate, BookOut
from app.books.domain.entities.book_author import BookAuthorCreate
from app.books.service.commands.book import create_book_command, delete_book_command
from app.books.service.commands.book_author import (
    create_book_author_command,
    delete_book_author_command,
)
from app.books.service.query.book import get_book_query, get_books_query
from app.unit_of_work import UnitOfWork


router = APIRouter(prefix="/books", tags=["Books"])


# Done
@router.get("/", response_model=List[BookOut])
async def get_books():
    async with UnitOfWork() as uow:
        books = await get_books_query(uow)
        return books


# Done
@router.get("/{id}", response_model=BookOut)
async def get_book(
    id: int,
):
    async with UnitOfWork() as uow:
        book = await get_book_query(id, uow)
        return book


# Done
@router.post("/", response_model=BookOut)
async def create_book(
    book: BookCreate,
):
    async with UnitOfWork() as uow:
        new_book = await create_book_command(book, uow)
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


# Done
@router.delete("/{book_id}")
async def delete_book(book_id: int):
    async with UnitOfWork() as uow:
        await delete_book_command(book_id, uow)
        await uow.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)


########## BookAuhtor ##########


@router.post("/{book_id}/{author_id}", dependencies=[Depends(current_author_or_admin)])
async def create_book_author(book_id: int, author_id: int):
    async with UnitOfWork() as uow:
        new_book_author = await create_book_author_command(
            BookAuthorCreate(book_id=book_id, author_id=author_id), uow
        )
        await uow.commit()
        await uow.refresh(new_book_author)
        return new_book_author


@router.delete(
    "/{book_id}/{author_id}", dependencies=[Depends(current_author_or_admin)]
)
async def delete_book_author(book_id: int, author_id: int):
    async with UnitOfWork() as uow:
        await delete_book_author_command(book_id, author_id, uow)
        await uow.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
