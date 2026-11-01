from app.models.passport_info import PassportInfo
from app.models.user import User
from app.schemas.passport_info_schemas import *

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError


class PassportInfoController:

    @staticmethod
    def get_all(session: Session) -> list[PassportInfo]:
        return list(session.exec(select(PassportInfo)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> PassportInfo | None:
        return session.get(PassportInfo, id)

    @staticmethod
    def add_passport_info(session: Session, data: PassportInfoNoIDSchema) -> PassportInfo:
        if session.get(User, data.fk_user_id) is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"no user with id {data.fk_user_id}")

        passport_info: PassportInfo = PassportInfo()
        data.apply_to_passport_info(passport_info)

        session.add(passport_info)
        session.commit()

        return passport_info

    @staticmethod
    def update_passport_info(session: Session, passport_info_id: int, data: PassportInfoNoIDSchema) -> PassportInfo:
        passport_info = session.get(PassportInfo, passport_info_id)

        if not passport_info:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "passport info with this id not found")

        if not session.get(User, data.fk_user_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"user with id {data.fk_user_id} not found")

        data.apply_to_passport_info(passport_info)

        session.add(passport_info)
        session.commit()
        session.refresh(passport_info)
        return passport_info

    @staticmethod
    def delete_passport_info(session: Session, passport_info_id: int) -> bool:
        passport_info: PassportInfo | None = PassportInfoController.get_by_id(session, passport_info_id)

        if not passport_info:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "passport info with this id not found")

        try:
            cnt: int = session.exec(delete(PassportInfo).where(PassportInfo.entry_id == passport_info_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably passport info is used somewhere")
