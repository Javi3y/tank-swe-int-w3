from datetime import UTC, datetime
from typing import Optional
from pydantic import EmailStr
from app.users.domain.enums.role import RoleEnum
from app.users.domain.entities.user import User


class Client(User):
    def __init__(
        self,
        email: EmailStr,
        username: str,
        name: str,
        sur_name: str,
        password: str,
        phone_number: str,
    ):
        super().__init__(email, username, name, sur_name, password, phone_number, RoleEnum("client"))


    def __repr__(self):
        return f"<Client {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return other.id == self.id
