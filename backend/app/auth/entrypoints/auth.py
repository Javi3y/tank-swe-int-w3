from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED
from app.auth.domain.entities.auth import Auth
from app.auth.service.auth import check_user, create_access_token, create_otp, get_token
from app.unit_of_work import UnitOfWork, get_uow
from random import randint


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/")
async def login(
    request: Request,
    user_credentials: Auth,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        await create_otp(request, user_credentials, uow)
        return {"msg": "enter the otp code in /login/otp"}


@router.post("/opt")
async def verify_otp(
    request: Request,
    user_credentials: Auth,
    otp: int,
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        access_token = await get_token(request, user_credentials, otp, uow)

    return {"access_token": access_token, "token_type": "bearer"}
