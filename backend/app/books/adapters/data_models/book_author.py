from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    DateTime,
    Table,
)

from sqlalchemy.sql.functions import current_timestamp


def get_book_author_db(metadata):
    genre_db = Table(
        "book_author",
        metadata,
        Column("author_id", Integer(), nullable=False),
        Column("book_id", Integer(), nullable=False),
        Column("id", Integer(), nullable=False),
        Column("created_at", DateTime(), nullable=False, default=current_timestamp()),
        ForeignKeyConstraint(["author_id"], ["author.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["book_id"], ["book.id"], ondelete="CASCADE"),
        PrimaryKeyConstraint("id"),
    )
    return genre_db
