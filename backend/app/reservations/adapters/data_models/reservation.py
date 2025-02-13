from sqlalchemy import (
    Boolean,
    Column,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    DateTime,
    Table,
)

from sqlalchemy.sql.functions import current_timestamp


def get_reservation_db(metadata):
    reservation_db = Table(
        "reservation",
        metadata,
        Column("client_id", Integer(), nullable=False),
        Column("book_id", Integer(), nullable=False),
        Column(
            "res_start",
            DateTime(timezone=True),
            nullable=False,
        ),
        Column(
            "res_end",
            DateTime(timezone=True),
            nullable=False,
        ),
        Column("id", Integer(), nullable=False),
        Column(
            "created_at",
            DateTime(timezone=True),
            nullable=False,
            default=current_timestamp(),
        ),
        Column("returned", Boolean(), nullable=False, default=False),
        ForeignKeyConstraint(["book_id"], ["book.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["client_id"], ["client.id"], ondelete="CASCADE"),
        PrimaryKeyConstraint("id"),
    )
    return reservation_db
