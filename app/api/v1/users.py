from app.models.user import User
from app.utils.jwt import TokenInfo
from app.schemas.user_schemas import *
from app.schemas.count_shema import CountSchema
from app.controllers.users_controller import UsersController
from app.db.session import get_session
from app.api.v1.helpers.auth_helpers import *

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", summary="get all users")
def get_all_users_route(session: Session = Depends(get_session), admin: User = Depends(get_admin)) -> list[UserNoPasswordSchema]:
    return [UserNoPasswordSchema.from_model(u) for u in UsersController.get_all(session)]

@router.get("/{id}", summary="get user by id")
def get_user_by_id_route(id: int, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    user = UsersController.get_by_id(session, id)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return UserNoPasswordSchema.from_model(user)

@router.get("/by_name/{name}", summary="get user by name")
def get_user_by_name_route(name: str, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    user = UsersController.get_by_name(session, name)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return UserNoPasswordSchema.from_model(user)

@router.post("", summary="add user")
def add_user_route(data: UserCreationSchema, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    return UserNoPasswordSchema.from_model(UsersController.add_user(session, data))

@router.put("/{id}", summary="edit user")
def edit_user_route(id: int, data: UserEditSchema, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    return UserNoPasswordSchema.from_model(UsersController.update_user(session, id, data))

@router.post("/change_password/{id}", summary="change user password")
def change_password_route(id: int, data: UserChangePasswordSchema, session: Session = Depends(get_session)) -> Response:
    user: User = UsersController.change_password(session, id, data.old_password, data.new_password)

    token: str = str(TokenInfo.create_for_user(user, type="access"))

    return Response(status_code=status.HTTP_200_OK)

@router.delete("/{id}", summary="delete user by id")
def delete_user_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if UsersController.delete_user(session, id) else 0))
