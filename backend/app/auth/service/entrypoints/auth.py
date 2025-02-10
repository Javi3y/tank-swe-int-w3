from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED
from app.auth.domain.entities.auth import Auth
from app.auth.service.auth import check_user, create_access_token, create_otp
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
    uow:UnitOfWork = Depends(get_uow)
):
    user = await check_user(user_credentials, uow)
    key = await request.app.state.n_client.query_key(user.id)

    if str(otp) != key:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="invalid credentails"
        )

    async with uow:
        access_token, expire = await create_access_token(data={"user_id": user.id})
        user.set_expire(expire)

        await uow.commit()
        await uow.refresh(user)

    return {"access_token": access_token, "token_type": "bearer"}

