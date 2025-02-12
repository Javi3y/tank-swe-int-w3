from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    Table,
)


def get_admin_db(metadata):
    admin_db = Table(
        "admin",
        metadata,
        Column("id", Integer(), primary_key=True, nullable=False),
        ForeignKeyConstraint(
            ["id"],
            ["user.id"],
        ),
    )
    return admin_db
