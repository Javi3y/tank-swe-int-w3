from sqlalchemy.orm import relationship
from app.books.domain.entities.book import Book
from app.reservations.adapters.data_models.reservation import get_reservation_db
from app.reservations.adapters.data_models.reservation_queue import (
    get_reservation_queue_db,
)
from app.reservations.domain.entities.reservation import Reservation
from app.reservations.domain.entities.reservation_queue import ReservationQueue
from app.users.domain.entities.client import Client


def reservation_mapper(mapper_registry, metadata):
    mapper_registry.map_imperatively(
        Reservation,
        get_reservation_db(metadata),
        properties={
            "client": relationship(Client, lazy="selectin"),
            "book": relationship(Book, lazy="selectin"),
        },
    )


def reservation_queue_mapper(mapper_registry, metadata):
    mapper_registry.map_imperatively(
        ReservationQueue,
        get_reservation_queue_db(metadata),
        properties={
            "client": relationship(Client, lazy="selectin"),
            "book": relationship(Book, lazy="selectin"),
        },
    )
