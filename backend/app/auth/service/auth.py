from datetime import datetime, timedelta, UTC
from random import randint
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy import select
from starlette.status import HTTP_401_UNAUTHORIZED
from app.auth.domain.entities.auth import Auth
from app.auth.domain.entities.token import TokenData

from app.config import settings
from app.unit_of_work import UnitOfWork, get_uow
from app.users.domain.entities.user import User

# from .database import get_db
# from .models import users

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


async def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded, expire


async def verify_access_token(token: str, credentials_exception, uow: UnitOfWork):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str | None = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = TokenData(id=int(id))
        async with uow:
            user_repo = uow.user_repo
            user = await user_repo.get_item(id)
            if user is None:  # Explicitly check if user exists
                raise credentials_exception
            if not user.token_expire:
                raise credentials_exception
    except JWTError:
        raise credentials_exception
    return token_data


async def get_current_user(
    request: Request, uow: UnitOfWork = Depends(get_uow)
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"www-Authenticate": "Bearer"},
    )
    try:
        raw_token = request.headers.get("Authorization")
        if not raw_token:
            raise credentials_exception
        scheme, token = raw_token.split()
        if scheme.lower() != "bearer":
            raise credentials_exception
    except ValueError:
        raise credentials_exception

    user_repo = uow.user_repo
    user_token = await verify_access_token(token, credentials_exception, uow)
    return await user_repo.get_item(user_token.id)


async def check_user(user_credentials: Auth, uow: UnitOfWork) -> User:
    user_repo = uow.user_repo
    user = await user_repo.get_by_user_or_email(user_credentials.username)
    if not user or not user_credentials.password == user.password:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="invalid credentails"
        )
    return user


async def create_otp(request: Request, user_credentials: Auth, uow):
    user = await check_user(user_credentials, uow)
    otp = str(randint(100000, 999999))
    await request.app.state.n_client.insert_string(user.id, otp, expiry_seconds=120)
    print(otp)


async def get_token(
    request: Request, user_credentials: Auth, otp: int, uow: UnitOfWork
):
    user = await check_user(user_credentials, uow)
    key = await request.app.state.n_client.query_key(user.id)

    if str(otp) != key:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="invalid credentails"
        )

    access_token, expire = await create_access_token(data={"user_id": user.id})
    user.set_expire(expire)
    await uow.commit()
    await uow.refresh(user)
    return access_token
