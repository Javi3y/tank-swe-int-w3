from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel
from app.users.domain.enums.sub import SubEnum


class Subscription:
    def __init__(
        self,
        client_id: int,
        sub_start: datetime,
        sub_end: datetime,
        subscription_model: SubEnum,
        id: Optional[int] = None,
    ):
        self.client_id = client_id
        self.sub_start = sub_start
        self.sub_end = sub_end
        self.subscription_model = subscription_model
        self.id = id

    def __repr__(self):
        return f"<Subscription {self.client_id}-{self.subscription_model}>"

    def __eq__(self, other):
        if not isinstance(other, Subscription):
            return False
        return other.id == self.id


class SubOut(BaseModel):
    id: int
    client_id: int
    sub_start: datetime
    sub_end: datetime
