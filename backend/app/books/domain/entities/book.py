from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel


class Book:
    id: Optional[int]

    def __init__(
        self,
        title: str,
        isbn: str,
        price: int,
        units: int,
        description: str,
        created_at: Optional[datetime] = datetime.now(UTC),
        id: Optional[int]=None,
    ):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.units = units
        self.description = description
        self.id = id
        self.created_at = created_at

    def __str__(self):
        return f"<Book {self.title}>"


class BookBase(BaseModel):
    title: str
    isbn: str
    units: int
    description: str
    price:int


class BookCreate(BookBase):
    #author: int
    pass


class BookOut(BookBase):
    id: int
    created_at: datetime
