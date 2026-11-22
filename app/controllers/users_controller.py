from app.models.user import User
from app.schemas.user_schemas import UserCreationSchema, UserEditSchema
from app.utils.passwords import verify as verify_password
from app.utils.passwords import hash as hash_password
from app.utils.passwords import is_weak as is_password_weak
from app.core.config import ADMIN_NAME, ADMIN_PWD

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError

import logging


logger = logging.getLogger(__name__)


class UsersController:

    @staticmethod
    def on_startup(session: Session):
        if ADMIN_NAME and ADMIN_PWD:
            if is_password_weak(ADMIN_PWD):
                logger.error("bug: weak admin pwd in UsersController.on_startup")
                raise RuntimeError("bug: weak admin pwd in UsersController.on_startup")

            if session.exec(select(User).where(User.user_name == ADMIN_NAME)).first():
                logger.warn("not creating admin: user name taken")
                return

            try:
                admin = User(
                    user_name=ADMIN_NAME,
                    password_hash=hash_password(ADMIN_PWD),
                    real_id="system created admin",
                    is_admin=True
                )

                session.add(admin)
                session.commit()
                logger.warn("admin was created")
            except IntegrityError:
                logger.error("bug: integrity error on admin creation in UsersController.on_startup")
                raise RuntimeError("bug: integrity error on admin creation in UsersController.on_startup")

    @staticmethod
    def get_all(session: Session) -> list[User]:
        return list(session.exec(select(User)).all())

    @staticmethod
    def get_by_id(session: Session, id: int) -> User | None:
        return session.get(User, id)

    @staticmethod
    def get_by_name(session: Session, name: str) -> User | None:
        return session.exec(select(User).where(User.user_name == name)).first()

    @staticmethod
    def authenticate(session: Session, user_name: str, password: str) -> User | None:
        user = UsersController.get_by_name(session, user_name)

        if user is None:
            return None

        if verify_password(password, user.password_hash):
            return user
        else:
            return None

    @staticmethod
    def add_user(session: Session, data: UserCreationSchema) -> User:
        search_res = session.exec(select(User).where(User.user_name == data.user_name)).first()

        if reason := is_password_weak(data.password):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, reason)

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "this user name is already taken")

        user = data.to_model()

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update_user(session: Session, user_id: int, data: UserEditSchema, allow_privs_elevation: bool = False) -> User:
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user with this id not found")

        if user.user_name != data.user_name:
            search_res = session.exec(select(User).where(User.user_name == data.user_name)).first()

            if search_res:
                raise HTTPException(status.HTTP_409_CONFLICT, "this user name is already taken")

        if not user.is_admin and data.is_admin and not allow_privs_elevation:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "privileges elevation is forbidden in this case")

        data.apply_to_model(user)

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    # TODO: revoke tokens
    @staticmethod
    def change_password(session: Session, user_id: int, old: str, new: str) -> User:
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user with this id not found")

        if reason := is_password_weak(new):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, reason)

        if not verify_password(old, user.password_hash):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "old password is wrong")

        user.password_hash = hash_password(new)

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
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably user is used somewhere")
