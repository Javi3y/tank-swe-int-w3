from datetime import UTC, datetime
from typing import Optional


class BookAuthor:
    def __init__(
        self,
        id: Optional[int],
        author_id: int,
        book_id: int,
        created_at: Optional[datetime] = datetime.now(UTC),
    ):
        self.book_id = book_id
        self.author_id = author_id
        self.id = id
        self.created_at = created_at

    def __str__(self):
        return f"<Book {self.author_id}-{self.book_id}>"
