from app.events.adapters.data_models.event import get_event_db
from app.events.domain.entities.event import Event


def event_mapper(mapper_registry, metadata):
    mapper_registry.map_imperatively(
        Event,
        get_event_db(metadata),
    )
