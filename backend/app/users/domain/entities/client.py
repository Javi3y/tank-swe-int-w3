from app.users.domain.enums.role import RoleEnum
from app.users.domain.entities.user import User


class Client(User):
    role: RoleEnum = RoleEnum("client")


    def __repr__(self):
        return f"<Client {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return other.id == self.id
