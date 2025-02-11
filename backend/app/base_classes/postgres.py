from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import as_declarative
from sqlalchemy.sql.functions import current_timestamp


@as_declarative()
class Base:
    id = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(
        "created_at", DateTime(timezone=True), default=current_timestamp(), nullable=False
    )
