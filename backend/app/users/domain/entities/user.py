from datetime import UTC, datetime
import re
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from app.users.domain.enums.role import RoleEnum
from starlette.status import HTTP_400_BAD_REQUEST


class User:
    id: Optional[int]
    email: EmailStr
    username: str
    name: str
    sur_name: str
    password: str
    phone_number: str
    role: RoleEnum
    token_expire: Optional[datetime] = None
    created_at: Optional[datetime] = datetime.now(UTC)

    def __init__(
        self,
        email: EmailStr,
        username: str,
        name: str,
        sur_name: str,
        password: str,
        phone_number: str,
        role: RoleEnum,
    ):
        self.email = email
        self.username = username
        self.name = name
        self.sur_name = sur_name
        self.password = password
        self.phone_number = phone_number
        self.role = role

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

    def is_valid_phone_number(self, phone_number):
        if re.fullmatch(r"^(?:\+98|0)?9\d{9}$", phone_number):
            return phone_number
        raise HTTPException(HTTP_400_BAD_REQUEST, "invalid phone number")
    def set_expire(self, expire):
        self.token_expire = expire


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


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    name: Optional[str] = None
    sur_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
