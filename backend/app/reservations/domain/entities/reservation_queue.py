from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel
from app.users.domain.entities.client import Client, ClientOut
from app.books.domain.entities.book import Book, BookOut


class ReservationQueue:
    id: Optional[int]
    client_id: int
    client: Client
    book_id: int
    book: Book
    created_at: Optional[datetime] = datetime.now(UTC)

    def __init__(
        self,
        client_id: int,
        book_id: int,
        id:Optional[int]=None,
    ):
        self.id = id
        self.client_id = client_id
        self.book_id = book_id

    def __str__(self):
        return f"<ReservationQueue {self.client_id}-{self.book_id}>"

    def __eq__(self, other):
        if not isinstance(other, ReservationQueue):
            return False
        return other.id == self.id


class ReservationQueueBase(BaseModel):
    pass


class ReservationQueueCreate(ReservationQueueBase):
    book_id: int
    client_id: int


class ReservationQueueOut(ReservationQueueBase):
    book: BookOut
    client: ClientOut
