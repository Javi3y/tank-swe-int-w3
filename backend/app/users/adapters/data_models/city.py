from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    DateTime,
    Table,
    UniqueConstraint,
)


def get_city_db(metadata):
    city_db = Table(
        "city",
        metadata,
        Column("id", Integer(), nullable=False, primary_key=True),
        Column("created_at", DateTime(), nullable=False),
        Column("name", String, nullable=False, unique=True),
        PrimaryKeyConstraint("id"),
        UniqueConstraint("name"),
    )
    return city_db
