from app.users.domain.enums.role import RoleEnum
from app.users.domain.entities.user import User


class Author(User):
    role: RoleEnum= RoleEnum("author")

    def __str__(self):
        return f"<Author {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, Author):
            return False
        return other.id == self.id
