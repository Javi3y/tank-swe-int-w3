from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel


class BookAuthor:
    id: Optional[int]

    def __init__(
        self,
        author_id: int,
        book_id: int,
        id: Optional[int] = None,
        created_at: Optional[datetime] = datetime.now(UTC),
    ):
        self.book_id = book_id
        self.author_id = author_id
        self.id = id
        self.created_at = created_at

    def __str__(self):
        return f"<Book {self.author_id}-{self.book_id}>"


class BookAuthorCreate(BaseModel):
    book_id: int
    author_id: int

    class Config:
        from_attributes = True
