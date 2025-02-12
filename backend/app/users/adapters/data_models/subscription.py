from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    Enum,
    PrimaryKeyConstraint,
    DateTime,
    Table,
)
from sqlalchemy.sql.functions import current_timestamp

from app.users.domain.enums.sub import SubEnum


def get_sub_db(metadata):
    sub_db = Table(
        "subscription",
        metadata,
        Column("client_id", Integer(), nullable=False),
        Column("subscription_model", Enum(SubEnum), nullable=False),
        Column("start", DateTime(), nullable=False),
        Column("end", DateTime(), nullable=False),
        Column("id", Integer(), nullable=False),
        Column(
            "created_at",
            DateTime(timezone=True),
            nullable=False,
            default=current_timestamp(),
        ),
        ForeignKeyConstraint(["client_id"], ["client.id"], ondelete="CASCADE"),
        PrimaryKeyConstraint("id"),
    )
    return sub_db
