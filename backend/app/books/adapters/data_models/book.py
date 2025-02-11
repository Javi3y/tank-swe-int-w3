from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    DateTime,
    Table,
    UniqueConstraint,
)

# from sqlalchemy.func import now
from sqlalchemy.sql.functions import current_timestamp


def get_book_db(metadata):
    genre_db = Table(
        "book",
        metadata,
        Column("title", String(), nullable=False),
        Column("isbn", String(), nullable=False),
        Column("price", Integer(), nullable=False),
        Column("units", Integer(), nullable=False),
        Column("description", String(), nullable=False),
        Column("id", Integer(), nullable=False),
        Column(
            "created_at",
            DateTime(timezone=True),
            nullable=False,
            default=current_timestamp(),
        ),
        PrimaryKeyConstraint("id"),
        UniqueConstraint("isbn"),
    )
    return genre_db
