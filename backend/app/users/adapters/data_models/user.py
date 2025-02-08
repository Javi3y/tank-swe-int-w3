from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    DateTime,
    Enum,
    Table,
    UniqueConstraint,
)
from sqlalchemy_utils import PasswordType, EmailType
from app.users.domain.enums import role


def get_user_db(metadata):
    user_db = Table(
        "user",
        metadata,
        Column("id", Integer(), nullable=False, primary_key=True),
        Column("created_at", DateTime(), nullable=False),
        Column("email", EmailType(), nullable=False),
        Column("username", String(), nullable=False),
        Column("name", String(), nullable=False),
        Column("sur_name", String(), nullable=False),
        Column("token_expire", DateTime(timezone=True), nullable=True),
        Column("password", PasswordType(), nullable=False),
        Column("phone_number", String(), nullable=False),
        Column("role", Enum(role.RoleEnum), nullable=False),
        PrimaryKeyConstraint("id"),
        UniqueConstraint("email"),
        UniqueConstraint("username"),
        CheckConstraint("phone_number ~ '^09[0-9]{9}$'", name='valid_mobile_phone')
    )
    return user_db
