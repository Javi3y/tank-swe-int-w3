from fastapi import APIRouter, Depends, Request
from app.auth.domain.entities.auth import Auth
from app.auth.service.auth import create_otp, get_token
from app.unit_of_work import UnitOfWork, get_uow


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
):
    async with UnitOfWork() as uow:
        access_token = await get_token(request, user_credentials, otp, uow)

    return {"access_token": access_token, "token_type": "bearer"}
