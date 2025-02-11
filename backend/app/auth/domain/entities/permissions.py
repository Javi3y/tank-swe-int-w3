from fastapi import HTTPException, Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from abc import ABC, abstractmethod
from app.users.domain.entities.user import User
from app.users.domain.enums.role import RoleEnum


def any_permission(permissions: list, request: Request) -> bool:
    for p in permissions:
        try:
            p(request=request)
            return True
        except HTTPException:
            pass
    return False


class BasePermission(ABC):
    def __init__(self, request: Request, user: User):
        self.request = request
        self.user = user
        self.role = user.role

    @abstractmethod
    def has_permission(self) -> bool:
        pass

    def __call__(self) -> bool:
        if not self.has_permission():
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return True


class AdminPermission(BasePermission):
    def __init__(self, request: Request, user: User):
        self.user = user
        self.role = user.role
        self.request = request

    def has_permission(self) -> bool:
        return self.role == RoleEnum.admin


class CurrentUserPermission(BasePermission):
    def __init__(self, request: Request, user: User):
        self.user_id = int(request.path_params["user_id"])
        self.user = user

    def has_permission(self) -> bool:
        return self.user.id == self.user_id


class CurrentUserOrAdminPermission(BasePermission):
    def __init__(self, request: Request, user: User):
        self.user = user
        self.user_id = int(request.path_params["user_id"])

    def has_permission(self) -> bool:
        return any([self.user.id == self.user_id, self.user.role == RoleEnum.admin])


class AuthorOrAdminPermission(BasePermission):
    def __init__(self, request: Request, user: User):
        self.user = user
        self.request = request

    def has_permission(self) -> bool:
        return any(
            [self.user.role == RoleEnum.author, self.user.role == RoleEnum.admin]
        )
