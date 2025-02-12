from pydantic import EmailStr
from app.users.domain.enums.role import RoleEnum
from app.users.domain.entities.user import User


class Admin(User):
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
            email, username, name, sur_name, password, phone_number, RoleEnum.author
        )
        self.id = super().id

    def __str__(self):
        return f"<Admin {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, Admin):
            return False
        return other.id == self.id


