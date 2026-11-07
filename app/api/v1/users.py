from app.models.user import User
from app.schemas.user_schemas import UserNoPasswordSchema, UserRegisterSchema, UserEmailSchema, UserPasswordSchema
from app.schemas.count_shema import CountSchema
from app.controllers.users_controller import UsersController
from app.db.session import get_session

from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlmodel import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", summary="get users paginated")
def get_users_paginated(limit: int = Query(default=0), offset: int = Query(default=0), session: Session = Depends(get_session)) -> list[UserNoPasswordSchema]:
    return [UserNoPasswordSchema.from_user(u) for u in UsersController.get_paginated(session, limit, offset)]

@router.get("/{id}", summary="get user by id")
def get_user_by_id_route(id: int, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    user = UsersController.get_by_id(session, id)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return UserNoPasswordSchema.from_user(user)

@router.get("/by_email/{email}", summary="get user by email")
def get_user_by_email_route(email: str, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    user = UsersController.get_by_email(session, email)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return UserNoPasswordSchema.from_user(user)

@router.put("/{id}/change_email", summary="change user email")
def change_user_email_route(id: int, data: UserEmailSchema, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    return UserNoPasswordSchema.from_user(UsersController.change_email(session, id, data.email))

@router.put("/{id}/change_password", summary="change user password")
def change_user_password_route(id: int, data: UserPasswordSchema, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    return UserNoPasswordSchema.from_user(UsersController.change_password(session, id, data.password))

@router.post("", summary="register user")
def register_user_route(registration_data: UserRegisterSchema, session: Session = Depends(get_session)) -> UserNoPasswordSchema:
    return UserNoPasswordSchema.from_user(
        UsersController.register_user(session, registration_data.email, registration_data.password)
    )

@router.delete("/{id}", summary="delete user by id")
def delete_user_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if UsersController.delete_user(session, id) else 0))
