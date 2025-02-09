from datetime import UTC, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.users.domain.enums.role import RoleEnum


#class User:
#    id: int
#    email: EmailStr
#    username: str
#    name: str
#    sur_name: str
#    password: str
#    phone_number: str
#    role: RoleEnum
#    token_expire: Optional[datetime] = None
#    created_at: Optional[datetime] = datetime.now(UTC)
#    def __init__(
#        self,
#        email: EmailStr,
#        username: str,
#        name: str,
#        sur_name: str,
#        password: str,
#        phone_number: str,
#        role: RoleEnum,
#    ):
#        self.email = email
#        self.username = username
#        self.name = name
#        self.sur_name = sur_name
#        self.password = password
#        self.phone_number = phone_number
#        self.role = role
#
#    def is_token_expired(self) -> bool:
#        """Checks if the token has expired."""
#        if not self.token_expire:
#            return True
#        return datetime.now(UTC) > self.token_expire
#
#    def __repr__(self):
#        return f"<User {self.username}>"
#
#    def __eq__(self, other):
#        if not isinstance(other, User):
#            return False
#        return other.id == self.id

class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    name: str
    sur_name: str
    password: str
    phone_number: str
    role: RoleEnum

    token_expire: Optional[datetime] = None
    created_at: Optional[datetime] = datetime.now(UTC)

    class Config:
        from_attributes = True

    def is_token_expired(self) -> bool:
        """Checks if the token has expired."""
        if not self.token_expire:
            return True
        return datetime.now(UTC) > self.token_expire

    def __str__(self):
        return f"<User {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.id == self.id
