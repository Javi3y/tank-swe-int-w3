from sqlalchemy.orm import properties, relationship
from app.books.adapters.data_models.book import get_book_db
from app.books.adapters.data_models.book_author import get_book_author_db
from app.books.adapters.data_models.genre import get_genre_db
from app.books.domain.entities.book import Book
from app.books.domain.entities.book_author import BookAuthor
from app.books.domain.entities.genre import Genre
from sqlalchemy.orm import registry


def genre_mapper(mapper_registry: registry, metadata):
    mapper_registry.map_imperatively(Genre, get_genre_db(metadata))


def book_author_mapper(mapper_registry: registry, metadata):
    mapper_registry.map_imperatively(BookAuthor, get_book_author_db(metadata))


def book_mapper(mapper_registry: registry, metadata):
    mapper_registry.map_imperatively(
        Book,
        get_book_db(metadata),
        properties={
            "authors": relationship(
                "Author",
                secondary="book_author",
                back_populates="books",
                lazy="selectin",
            )
        },
    )
