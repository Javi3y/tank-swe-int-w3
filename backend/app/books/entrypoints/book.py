from typing import List
from fastapi import APIRouter, Depends, Response
from starlette.status import HTTP_204_NO_CONTENT

from app.auth.service.dependencies.permissions import current_author_or_admin
from app.books.domain.entities.book import BookCreate, BookOut
from app.books.domain.entities.book_author import BookAuthorCreate
from app.books.service.book import BookService
from app.books.service.book_author import BookAuthorService
from app.unit_of_work import UnitOfWork, get_uow


router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookOut])
async def get_books():
    async with UnitOfWork() as uow:
        book_service = BookService()
        books = await book_service.get_items(uow)
        BookOut.model_rebuild()
        return books


@router.get("/{id}")
async def get_book(
    id: int,
):
    async with UnitOfWork() as uow:
        book_service = BookService()
        books = await book_service.get_item(id, uow)
        parsed = [book._mapping for book in books]
        return {"list": parsed}


@router.post("/", response_model=BookOut)
async def create_book(
    book: BookCreate,
):
    async with UnitOfWork() as uow:
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
async def delete_book(book_id: int):
    async with UnitOfWork() as uow:
        book_service = BookService()
        await book_service.delete_item(book_id, uow)
        await uow.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)


########## BookAuhtor ##########


@router.post("/{book_id}/{author_id}", dependencies=[Depends(current_author_or_admin)])
async def create_book_author(book_id: int, author_id: int):
    async with UnitOfWork() as uow:
        book_author_service = BookAuthorService()
        new_book_author = await book_author_service.create_item(
            BookAuthorCreate(book_id=book_id, author_id=author_id), uow
        )
        await uow.commit()
        await uow.refresh(new_book_author)
        return new_book_author

@router.delete("/{book_id}/{author_id}", dependencies=[Depends(current_author_or_admin)])
async def delete_book_author(book_id: int, author_id: int):
    async with UnitOfWork() as uow:
        book_author_service = BookAuthorService()
        await book_author_service.delete_item(book_id, author_id, uow)
        await uow.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
