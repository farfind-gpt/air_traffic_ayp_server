from app.models.airport import Airport
from app.models.city import City
from app.schemas.airport_schemas import AirportNoIdSchema
from app.utils.airports import is_valid_icao_index

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError


class AirportsController:

    @staticmethod
    def get_all(session: Session) -> list[Airport]:
        return list(session.exec(select(Airport)))

    @staticmethod
    def get_all_in_city(session: Session, city_id: int) -> list[Airport]:
        if session.get(City, city_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"there is no city with id {city_id}")

        return list(session.exec(select(Airport).where(Airport.fk_city_id == city_id)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> Airport | None:
        return session.get(Airport, id)

    @staticmethod
    def add_airport(session: Session, data: AirportNoIdSchema) -> Airport:
        if not is_valid_icao_index(data.icao_index):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid ICAO index")

        search_res = session.exec(select(Airport).where(Airport.name == data.name)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "airport with this name already exists")

        search_res = session.exec(select(Airport).where(Airport.icao_index == data.icao_index)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "airport with this ICAO index already exists")

        if session.get(City, data.fk_city_id) is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"no city with id {data.fk_city_id}")

        airport = data.to_airport()

        session.add(airport)
        session.commit()
        session.refresh(airport)

        return airport

    @staticmethod
    def update_airport(session: Session, airport_id: int, data: AirportNoIdSchema) -> Airport:
        airport = session.get(Airport, airport_id)

        if not airport:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "airport with this id not found")

        if airport.name != data.name:
            search_res = session.exec(select(Airport).where(Airport.name == data.name)).first()

            if search_res:
                raise HTTPException(status.HTTP_409_CONFLICT, "airport with this name already exists")

        if airport.icao_index != data.icao_index:
            search_res = session.exec(select(Airport).where(Airport.icao_index == data.icao_index)).first()

            if search_res:
                raise HTTPException(status.HTTP_409_CONFLICT, "airport with this ICAO index already exists")

        if airport.fk_city_id != data.fk_city_id:
            if session.get(City, data.fk_city_id) is None:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, f"no city with id {data.fk_city_id}")

        data.apply_to_model(airport)

        session.add(airport)
        session.commit()
        session.refresh(airport)
        return airport

    @staticmethod
    def delete_airport(session: Session, airport_id: int) -> bool:
        airport: Airport | None = AirportsController.get_by_id(session, airport_id)

        if not airport:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "airport with this id not found")

        try:
            cnt: int = session.exec(delete(Airport).where(Airport.airport_id == airport_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably airport is used somewhere")
