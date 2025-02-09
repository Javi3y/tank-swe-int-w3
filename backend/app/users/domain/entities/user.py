from datetime import UTC, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.users.domain.enums.role import RoleEnum


class User(BaseModel):
    id: Optional[int]
    email: EmailStr
    username: str
    name: str
    sur_name: str
    password: str
    phone_number: str

    token_expire: Optional[datetime] = None
    created_at: Optional[datetime] = datetime.now(UTC)


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


class UserBase(BaseModel):
    email: EmailStr
    username: str
    name: str
    sur_name: str
    phone_number: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
