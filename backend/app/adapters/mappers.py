from app.reservations.adapters.mappers import (
    reservation_mapper,
    reservation_queue_mapper,
)
from app.users.adapters.mappers import (
    admin_mapper,
    author_mapper,
    city_mapper,
    client_mapper,
    sub_mapper,
    user_mapper,
)
from app.books.adapters.mappers import book_author_mapper, book_mapper, genre_mapper
from app.events.adapters.mappers import event_mapper


def mapper(mapper_registry, metadata):
    user_mapper(mapper_registry, metadata)
    city_mapper(mapper_registry, metadata)
    client_mapper(mapper_registry, metadata)
    author_mapper(mapper_registry, metadata)
    sub_mapper(mapper_registry, metadata)
    admin_mapper(mapper_registry, metadata)

    genre_mapper(mapper_registry, metadata)
    book_author_mapper(mapper_registry, metadata)
    book_mapper(mapper_registry, metadata)

    reservation_mapper(mapper_registry, metadata)
    reservation_queue_mapper(mapper_registry, metadata)

    event_mapper(mapper_registry, metadata)
