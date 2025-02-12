from datetime import UTC, datetime
from typing import List, Optional
from pydantic import EmailStr
from app.users.domain.entities.subscription import SubOut, Subscription
from app.users.domain.enums.role import RoleEnum
from app.users.domain.entities.user import (
    User,
    UserBase,
    UserCreate,
    UserOut,
    UserUpdate,
)


class Client(User):
    balance: int
    subscriptions: List[Subscription]

    def __init__(
        self,
        # id: int,
        email: EmailStr,
        username: str,
        name: str,
        sur_name: str,
        password: str,
        phone_number: str,
    ):
        super().__init__(
            email, username, name, sur_name, password, phone_number, RoleEnum.client
        )
        self.id = super().id
        self.balance = 0

    def update(self, updated_client):
        keys = updated_client.keys()
        if "email" in keys:
            self.email = updated_client["email"]
        if "username" in keys:
            self.username = updated_client["username"]
        if "name" in keys:
            self.name = updated_client["name"]
        if "sur_name" in keys:
            self.name = updated_client["sur_name"]
        if "password" in keys:
            self.password = updated_client["password"]
        if "phone_number" in keys:
            self.phone_number = self.is_valid_phone_number(
                updated_client["phone_number"]
            )

    def __repr__(self):
        return f"<Client {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return other.id == self.id

    @property
    def current_subscription(self):
        """Returns the most recent valid subscription if available."""
        now = datetime.now(UTC)
        active_subs = [
            sub for sub in self.subscriptions if sub.sub_start <= now <= sub.sub_end
        ]
        return max(active_subs, key=lambda sub: sub.sub_end, default=None)


class ClientBase(UserBase):
    pass


class ClientCreate(UserCreate):
    pass


class ClientOut(UserOut):
    balance: int
    current_subscription: Optional[SubOut] = None


class ClientUpdate(UserUpdate):
    pass
