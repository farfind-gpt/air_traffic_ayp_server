from app.models.reservation_group import ReservationGroup
from app.models.passenger import Passenger
from app.models.reservation import Reservation
from app.utils.reservation_groups import *
from app.schemas.reservation_group_schemas import ReservationGroupEditSchema
from app.config import PAGE_LIMIT

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError

from datetime import datetime


class ReservationGroupsController:

    @staticmethod
    def get_paginated(session: Session, offset: int = 0, limit: int = 0) -> list[ReservationGroup]:
        if limit > PAGE_LIMIT:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"maximal limit is {PAGE_LIMIT}")

        return list(session.exec(select(ReservationGroup).offset(offset).limit(limit)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> ReservationGroup | None:
        return session.get(ReservationGroup, id)

    @staticmethod
    def get_by_code(session: Session, code: str) -> ReservationGroup | None:
        if not is_valid_reservation_group_code(code):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid reservation code format")

        return session.exec(select(ReservationGroup).where(ReservationGroup.reservation_group_code == code)).first()

    @staticmethod
    def get_by_passenger_in_members(session: Session, passenger_id: int) -> list[ReservationGroup]:
        return list(session.exec(
            select(ReservationGroup).join(
                Reservation,
                ReservationGroup.reservation_group_id == Reservation.fk_reservation_group_id
            ).where(Reservation.fk_passenger_id == passenger_id)
        ).all())

    @staticmethod
    def get_by_owner(session: Session, owner_id: int) -> list[ReservationGroup]:
        return list(session.exec(
            select(ReservationGroup).where(ReservationGroup.fk_owner_id == owner_id)
        ).all())

    @staticmethod
    def add_reservation_group(session: Session, owner_id: int) -> ReservationGroup:
        if session.get(Passenger, owner_id) is None:
            raise HTTPException(status.HTTP_404_CONFLICT, f"no passenger with id {owner_id}")

        group_code: str = ""

        for _ in range(30):
            generated_code: str = generate_reservation_group_code()

            if session.exec(select(ReservationGroup).where(ReservationGroup.reservation_group_code == generated_code)).first() is None:
                group_code = generated_code
                break
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "could not generate unique reservation group code in 30 attempts, it is a bug or just very bad luck, please try again")

        group = ReservationGroup(
            reservation_group_code=group_code,
            fk_owner_id=owner_id,
            created_at=datetime.now(),
            paid=False
        )

        session.add(group)
        session.commit()
        session.refresh(group)
        return group

    @staticmethod
    def change_paid(session: Session, id: int, paid: bool) -> ReservationGroup:
        reservation_group = session.get(ReservationGroup, id)

        if reservation_group is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")

        reservation_group.paid = not reservation_group.paid

        session.add(reservation_group)
        session.commit()
        session.refresh(reservation_group)
        return reservation_group

    @staticmethod
    def update_reservation_group(session: Session, id: int, data: ReservationGroupEditSchema) -> ReservationGroup:
        reservation_group = session.get(ReservationGroup, id)

        if not reservation_group:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "reservation group with this id not found")

        if reservation_group.reservation_group_code != data.reservation_group_code:
            if session.exec(select(ReservationGroup).where(ReservationGroup.reservation_group_code == data.reservation_group_code)).first() is not None:
                raise HTTPException(status.HTTP_409_CONFLICT, "reservation group with this code already exists")

        if reservation_group.fk_owner_id != data.fk_owner_id:
            if data.fk_owner_id is None:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "you cannot manually set fk_owner_id to null, only database can do it when owner is deleted")

            if session.get(Passenger, data.fk_owner_id) is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"passanger with id {data.fk_owner_id} not found")

        data.apply_to_model(reservation_group)

        session.add(reservation_group)
        session.commit()
        session.refresh(reservation_group)
        return reservation_group

    @staticmethod
    def delete_reservation_group(session: Session, id: int) -> bool:
        reservation_group: ReservationGroup | None = ReservationGroupsController.get_by_id(session, id)

        if not reservation_group:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "reservation group with this id not found")

        try:
            cnt: int = session.exec(delete(ReservationGroup).where(ReservationGroup.reservation_group_id == id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably reservation group is used somewhere")
