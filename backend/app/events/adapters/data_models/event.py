from sqlalchemy import (
    JSON,
    Enum,
    Column,
    Integer,
    PrimaryKeyConstraint,
    DateTime,
    Table,
)

from sqlalchemy.sql.functions import current_timestamp

from app.events.domain.enums.event_status import EventStatusEnum
from app.events.domain.enums.event_type import EventTypeEnum


def get_event_db(metadata):
    event_db = Table(
        "event",
        metadata,
        Column("id", Integer(), nullable=False),
        Column(
            "timestamp",
            DateTime(timezone=True),
            nullable=False,
        ),
        Column(
            "created_at",
            DateTime(timezone=True),
            nullable=False,
            default=current_timestamp(),
        ),
        Column("payload", JSON, nullable=False),
        Column("event_type", Enum(EventTypeEnum), nullable=False),
        Column(
            "event_status",
            Enum(EventStatusEnum),
            nullable=False,
            default=EventStatusEnum.pending,
        ),
        PrimaryKeyConstraint("id"),
    )
    return event_db
