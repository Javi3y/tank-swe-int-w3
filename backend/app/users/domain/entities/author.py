from pydantic import EmailStr
from app.users.domain.enums.role import RoleEnum
from app.users.domain.entities.user import User


class Author(User):
    def __init__(
        self,
        email: EmailStr,
        username: str,
        name: str,
        sur_name: str,
        password: str,
        phone_number: str,
    ):
        super().__init__(email, username, name, sur_name, password, phone_number, RoleEnum("Author"))


    def __repr__(self):
        return f"<Author {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, Author):
            return False
        return other.id == self.id
