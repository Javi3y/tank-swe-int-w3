from typing import List
from pydantic import EmailStr
from app.books.domain.entities.book import Book
from app.users.domain.entities.city import City, CityOut
from app.users.domain.enums.role import RoleEnum
from app.users.domain.entities.user import User, UserCreate, UserOut


class Author(User):
    city: City
    books: List[Book]

    def __init__(
        self,
        # id: int,
        email: EmailStr,
        username: str,
        name: str,
        sur_name: str,
        password: str,
        phone_number: str,
        goodreads: str,
        bank_account: str,
        city: City,
    ):
        super().__init__(
            email, username, name, sur_name, password, phone_number, RoleEnum.author
        )
        self.id = super().id
        self.goodreads = goodreads
        self.bankaccount = bank_account
        self.city = city

    def __str__(self):
        return f"<Author {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, Author):
            return False
        return other.id == self.id


class AuthorCreate(UserCreate):
    bank_account: str


class AuthorOut(UserOut):
    city: CityOut
    # books: List[BookOut]
