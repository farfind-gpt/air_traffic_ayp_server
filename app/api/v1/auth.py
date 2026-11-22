from app.models.user import User
from app.controllers.users_controller import UsersController
from app.schemas.auth_schemas import TokensSchema, RefreshTokenSchema
from app.utils.jwt import TokenInfo
from app.api.v1.helpers.auth_helpers import *
from app.db.session import get_session

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", summary="login with username and password")
def login_route(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> TokensSchema:
    user = UsersController.authenticate(session, data.username, data.password)

    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "authentication failed: wrong password or username")

    return TokensSchema(
        access_token=str(TokenInfo.create_for_user(user, type="access")),
        refresh_token=str(TokenInfo.create_for_user(user, type="refresh"))
    )

@router.post("/refresh", summary="refresh tokens using refresh token")
def refresh_route(data: RefreshTokenSchema, session: Session = Depends(get_session)) -> TokensSchema:
    refresh_token_info = TokenInfo.decode(data.refresh_token)

    if refresh_token_info is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "bad refresh token")

    user = UsersController.get_by_id(session, refresh_token_info.user_id)

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "bad refresh token")

    return TokensSchema(
        access_token=str(TokenInfo.create_for_user(user, type="access")),
        refresh_token=str(TokenInfo.create_for_user(user, type="refresh"))
    )
