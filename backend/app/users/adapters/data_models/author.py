from sqlalchemy import (
    UniqueConstraint,
    Column,
    ForeignKeyConstraint,
    Integer,
    String,
    Table,
)
from sqlalchemy_utils import URLType


def get_author_db(metadata):
    author_db = Table(
        "author",
        metadata,
        Column("id", Integer(), primary_key=True, nullable=False),
        Column("city_id", Integer(), nullable=False),
        Column("goodreads", URLType(), nullable=False),
        Column("bank_acount", String(), nullable=False),
        ForeignKeyConstraint(["city_id"], ["city.id"], ondelete="cascade"),
        ForeignKeyConstraint(
            ["id"],
            ["user.id"],
        ),
        UniqueConstraint("bank_acount"),
        UniqueConstraint("goodreads"),
    )
    return author_db
