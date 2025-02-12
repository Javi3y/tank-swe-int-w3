from typing import Annotated
from fastapi import Depends, Request
from app.auth.domain.entities.permissions import (
    AdminPermission,
    AuthorOrAdminPermission,
    CurrentAuthorOrAdminPermission,
    CurrentUserOrAdminPermission,
    CurrentUserOrAdminPermission,
    CurrentUserPermission,
)
from app.auth.service.auth import get_current_user
from app.users.domain.entities.user import User

CurrentUser = Annotated[User, Depends(get_current_user)]


async def admin_permission(request: Request, user: CurrentUser):
    permission = AdminPermission(request=request, user=user)
    permission()
    return user


async def current_user(request: Request, user: CurrentUser):
    permission = CurrentUserPermission(request=request, user=user)
    permission()
    return user


async def current_user_or_admin(request: Request, user: CurrentUser):
    permission = CurrentUserOrAdminPermission(request=request, user=user)
    permission()
    return user


async def author_or_admin(request: Request, user: CurrentUser):
    permission = AuthorOrAdminPermission(request=request, user=user)
    permission()
    return user


async def current_author_or_admin(request: Request, user: CurrentUser):
    permission = CurrentAuthorOrAdminPermission(request=request, user=user)
    permission()
    pass
