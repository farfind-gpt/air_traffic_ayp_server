from app.models.user import User
from app.controllers.users_controller import UsersController
from app.utils.jwt import TokenInfo
from app.db.session import get_session

from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", refreshUrl="/auth/refresh")


def get_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """
    get User model by provided token
    """

    token_info = TokenInfo.decode(token)

    if not token_info:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")

    user = UsersController.get_by_id(session, token_info.user_id)

    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")

    return user

def get_admin(user: User = Depends(get_user)) -> User:
    """
    only returns user from token if they are admin
    """

    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "admin user required")

    return user


__all__ = ["User", "get_user", "get_admin"]
