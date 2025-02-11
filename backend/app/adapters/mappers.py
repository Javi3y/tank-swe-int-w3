from app.users.adapters.mappers import (
    author_mapper,
    city_mapper,
    client_mapper,
    user_mapper,
)


def mapper(mapper_registry, metadata):
    user_mapper(mapper_registry, metadata)
    city_mapper(mapper_registry, metadata)
    client_mapper(mapper_registry, metadata)
    author_mapper(mapper_registry, metadata)
