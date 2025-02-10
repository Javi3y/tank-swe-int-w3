from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    Table,
)


def get_client_db(metadata):
    client_db = Table(
        "client",
        metadata,
        Column("id", Integer(), primary_key=True, nullable=False),
        Column("balance", Integer(), nullable=False),
        ForeignKeyConstraint(
            ["id"],
            ["user.id"],
        ),
    )
    return client_db
