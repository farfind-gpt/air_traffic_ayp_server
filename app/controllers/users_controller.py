from app.models.user import User
from app.utils.passwords import hash as hash_password
from app.utils.passwords import verify as verify_password
from app.utils.passwords import is_weak as is_password_weak

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError


class UsersController:

    @staticmethod
    def get_paginated(session: Session, limit: int, offset: int) -> list[User]:
        if limit > 50:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="max limit is 50")

        return list(session.exec(select(User).offset(offset).limit(limit)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> User | None:
        return session.get(User, id)

    @staticmethod
    def get_by_email(session: Session, email: str) -> User | None:
        return session.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def register_user(session: Session, email: str, password: str) -> User:
        if reason := is_password_weak(password):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, reason)

        search_res = session.exec(select(User).where(User.email == email)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "this email is already in use")

        new_user = User(email=email, password_hash=hash_password(password))

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

    @staticmethod
    def change_email(session: Session, user_id: int, new_email: str) -> User:
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user with this id not found")

        search_res = session.exec(select(User).where(User.email == email)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "this email is already in use")

        user.email = new_email

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def change_password(session: Session, user_id: int, new_password: str) -> User:
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user with this id not found")

        if reason := is_password_weak(new_password):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, reason)

        user.password_hash = hash_password(new_password)

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete_user(session: Session, user_id: int) -> bool:
        user: User | None = UsersController.get_by_id(session, user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user with this id not found")

        try:
            cnt: int = session.exec(delete(User).where(User.user_id == user_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably the user is used somewhere")
