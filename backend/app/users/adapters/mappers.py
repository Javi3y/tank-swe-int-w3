from app.users.adapters.data_models.client import get_client_db
from app.users.adapters.data_models.user import get_user_db
from app.users.adapters.data_models.city import get_city_db

from app.users.domain.entities.client import Client
from app.users.domain.entities.author import Author
from app.users.domain.entities.user import User
from app.users.domain.entities.city import City


def user_mapper(mapper_registry, metadata):
    mapper_registry.map_imperatively(
        User,
        get_user_db(metadata),
        polymorphic_identity="user",
        polymorphic_on="role",
    )


def city_mapper(mapper_registry, metadata):
    mapper_registry.map_imperatively(
        City,
        get_city_db(metadata),
    )


def client_mapper(mapper_registry, metadata):
    mapper_registry.map_imperatively(
        Client,
        get_client_db(metadata),
        polymorphic_identity="client",
    )


#def author_mapper(mapper_registry, metadata):
#    mapper_registry.map_imperatively(
#        Author,
#        get_author_db(metadata),
#        polymorphic_identity="author",
#    )
