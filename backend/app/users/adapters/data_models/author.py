from sqlalchemy import (
    column,
    foreignkeyConstraint,
    integer,
    string,
    table,
    uniqueconstraint,
)
from sqlalchemy_utils import urltype


def get_author_db(metadata):
    author_db = table(
        "author",
        metadata,
        column("id", integer(), primary_key=true, nullable=false),
        column("city_id", integer(), nullable=false),
        column("goodreads", urltype(), nullable=false),
        column("bank_acount", string(), nullable=false),
        foreignkeyConstraint(["city_id"], ["city.id"], ondelete="cascade"),
        foreignkeyConstraint(
            ["id"],
            ["user.id"],
        ),
        uniqueconstraint("bank_acount"),
        uniqueconstraint("goodreads"),
    )
    return author_db
