from enum import Enum


class EventStatusEnum(Enum):
    pending = "pending"
    resolved = "resolved"
    deleted = "deleted"
    canceled = "canceled"
    failed = "failed"
