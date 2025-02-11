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


def get_genre_db(metadata):
    genre_db = Table(
        "genre",
        metadata,
        Column("name", String(), nullable=False),
        Column("id", Integer(), nullable=False),
        Column("created_at", DateTime(), nullable=False, default=current_timestamp()),
        PrimaryKeyConstraint("id"),
        UniqueConstraint("name"),
    )
    return genre_db
