from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    DateTime,
    Table,
)

from sqlalchemy.sql.functions import current_timestamp


def get_reservation_queue_db(metadata):
    reservation_db = Table(
        "reservation_queue",
        metadata,
        Column("client_id", Integer(), nullable=False),
        Column("book_id", Integer(), nullable=False),
        Column("id", Integer(), nullable=False),
        Column(
            "created_at",
            DateTime(timezone=True),
            nullable=False,
            default=current_timestamp(),
        ),
        ForeignKeyConstraint(["book_id"], ["book.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["client_id"], ["client.id"], ondelete="CASCADE"),
        PrimaryKeyConstraint("id"),
    )
    return reservation_db
