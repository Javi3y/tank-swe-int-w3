from datetime import UTC, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.users.domain.enums.role import RoleEnum
from app.users.domain.entities.user import User, UserBase, UserCreate, UserOut


#class Client(User):
#    role: RoleEnum = RoleEnum("client")
#    balance: int = 0
#
#    #def __init__(
#    #    self,
#    #    email: EmailStr,
#    #    username: str,
#    #    name: str,
#    #    sur_name: str,
#    #    password: str,
#    #    phone_number: str,
#    #    id: Optional[int] = None,
#    #    token_expire: Optional[datetime] = None,
#    #    created_at: Optional[datetime] = datetime.now(UTC),
#    #) -> None:
#    #    super().__init__(
#    #        id=id,
#    #        email=email,
#    #        username=username,
#    #        name=name,
#    #        sur_name=sur_name,
#    #        password=password,
#    #        phone_number=phone_number,
#    #        token_expire=token_expire,
#    #        created_at=created_at,
#    #        role=RoleEnum("client"),
#    #    )
#
#    class Config:
#        from_attributes = True
#
#    def __str__(self):
#        return f"<Client {self.username}>"
#
#    def __eq__(self, other):
#        if not isinstance(other, Client):
#            return False
#        return other.id == self.id
class Client(BaseModel):
    id: Optional[int]
    email: EmailStr
    username: str
    name: str
    sur_name: str
    password: str
    phone_number: str
    balance: int = 0

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
        return f"<Client {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return other.id == self.id



class ClientBase(UserBase):
    pass


class ClientCreate(UserCreate):
    pass


class ClientOut(UserOut):
    balance: int
