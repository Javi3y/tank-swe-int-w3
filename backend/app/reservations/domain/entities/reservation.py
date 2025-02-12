from datetime import UTC, datetime
from typing import Optional
from app.users.domain.entities.client import Client
from app.books.domain.entities.book import Book


class Reservation:
    id: Optional[int]
    client_id: int
    client: Client
    book_id: int
    book: Book
    res_start: datetime
    res_end: datetime
    created_at: Optional[datetime] = datetime.now(UTC)

    def __init__(
        self,
        client_id: int,
        book_id: int,
        res_start: datetime,
        res_end: datetime,
    ):
        self.client_id = client_id
        self.book_id = book_id
        self.res_start = res_start
        self.res_end = res_end

    def __str__(self):
        return f"<Reservation {self.client_id}-{self.book_id}>"

    def __eq__(self, other):
        if not isinstance(other, Reservation):
            return False
        return other.id == self.id
