from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel


class Genre:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        created_at: Optional[datetime] = datetime.now(UTC),
    ):
        self.id = id
        self.created_at = created_at
        self.name = name

    def __repr__(self):
        return f"<City {self.name}>"


class GenreOut(BaseModel):
    name: str
