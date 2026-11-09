from app.models.passenger import Passenger
from app.schemas.passenger_schemas import PassengerNoIdSchema


from fastapi import HTTPException, status
from sqlmodel import Session, select, delete, String, cast
from sqlalchemy.exc import IntegrityError


class PassengersController:

    @staticmethod
    def get_all(session: Session) -> list[Passenger]:
        return list(session.exec(select(Passenger)))

    @staticmethod
    def get_paginated(session: Session, offset: int = 0, limit: int = 0):
        return list(session.exec(select(Passenger).offset(offset).limit(limit)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> Passenger | None:
        return session.get(Passenger, id)

    @staticmethod
    def get_by_series_and_number(session: Session, series: int, number: int) -> Passenger | None:
        return session.exec(select(Passenger).where(
                Passenger.series == series and Passenger.number == number
            )).first()

    @staticmethod
    def search_by_series_and_number(session: Session, series: str, number: str) -> list[Passenger]:
        return list(session.exec(select(Passenger).where(
            cast(Passenger.series, String).contains(series)
            and
            cast(Passenger.number, String).contains(number)
        )))

    @staticmethod
    def search_by_name(session: Session, first_name: str, last_name: str, patronymic: str) -> list[Passenger]:
        if patronymic:
            return list(session.exec(select(Passenger).where(
                Passenger.first_name.contains(first_name)
                and
                Passenger.last_name.contains(last_name)
                and
                Passenger.patronymic.contains(patronymic)
            )))
        else:
            return list(session.exec(select(Passenger).where(
                Passenger.first_name.contains(first_name)
                and
                Passenger.last_name.contains(last_name)
            )))

    @staticmethod
    def add_passenger(session: Session, data: PassengerNoIdSchema) -> Passenger:
        search_res = session.exec(select(Passenger).where(
            Passenger.series == data.series and Passenger.number == data.number
            )).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "passenger with this passport series and number already exists")

        passenger = data.to_model()

        session.add(passenger)
        session.commit()
        session.refresh(passenger)

        return passenger

    @staticmethod
    def update_passenger(session: Session, passenger_id: int, data: PassengerNoIdSchema) -> Passenger:
        passenger = session.get(Passenger, passenger_id)

        if not passenger:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "passenger with this id not found")

        if passenger.series != data.series or passenger.number != data.number:
            search_res = session.exec(select(Passenger).where(
                    Passenger.series == data.series and Passenger.number == data.number
                )).first()

            if search_res:
                raise HTTPException(status.HTTP_409_CONFLICT, "passenger with this passport series and number already exists")

        data.apply_to_model(passenger)

        session.add(passenger)
        session.commit()
        session.refresh(passenger)
        return passenger

    @staticmethod
    def delete_passenger(session: Session, passenger_id: int) -> bool:
        passenger: Passenger | None = PassengersController.get_by_id(session, passenger_id)

        if not passenger:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "passenger with this id not found")

        try:
            cnt: int = session.exec(delete(Passenger).where(Passenger.passenger_id == passenger_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably passenger is used somewhere")
