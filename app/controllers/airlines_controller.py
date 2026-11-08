from app.models.airline import Airline
from app.utils.airlines import is_valid_airline_code

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError


class AirlinesController:

    @staticmethod
    def get_all(session: Session) -> list[Airline]:
        return list(session.exec(select(Airline)).all())

    @staticmethod
    def get_by_id(session: Session, id: int) -> Airline | None:
        return session.get(Airline, id)

    @staticmethod
    def add_airline(session: Session, code: str, name: str) -> Airline:
        if not is_valid_airline_code(code):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "airline code is not valid")

        search_res = session.exec(select(Airline).where(Airline.airline_code == code)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "airline with this code already exists")

        search_res = session.exec(select(Airline).where(Airline.name == name)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "airline with this name already exists")

        airline = Airline(name=name, airline_code=code)

        session.add(airline)
        session.commit()
        session.refresh(airline)
        return airline

    @staticmethod
    def update_airline(session: Session, airline_id: int, code: str, name: str) -> Airline:
        airline = session.get(Airline, airline_id)

        if not airline:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "airline with this id not found")

        if airline.name != name:
            search_res = session.exec(select(Airline).where(Airline.name == name)).first()

            if search_res:
                raise HTTPException(status.HTTP_409_CONFLICT, "airline with this name already exists")

        if airline.airline_code != code:
            if not is_valid_airline_code(code):
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "airline code is not valid")

            search_res = session.exec(select(Airline).where(Airline.airline_code == code)).first()

            if search_res:
                raise HTTPException(status.HTTP_409_CONFLICT, "airline with this code already exists")

        airline.name = name
        airline.airline_code = code

        session.add(airline)
        session.commit()
        session.refresh(airline)
        return airline

    @staticmethod
    def delete_airline(session: Session, airline_id: int) -> bool:
        airline: Airline | None = AirlinesController.get_by_id(session, airline_id)

        if not airline:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "airline with this id not found")

        try:
            cnt: int = session.exec(delete(Airline).where(Airline.airline_id == airline_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably airline is used somewhere")
