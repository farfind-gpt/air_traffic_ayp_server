from app.models.city import City
from app.models.countries import Country
from app.schemas.city_shemas import *

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError


class CitiesController:

    @staticmethod
    def get_all(session: Session) -> list[City]:
        return list(session.exec(select(City)))

    @staticmethod
    def get_all_in_country(session: Session, country_id: int) -> list[City]:
        if session.get(Country, country_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"there is not country with id {country_id}")

        return list(session.exec(select(City).where(City.fk_country_id == country_id)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> City | None:
        return session.get(City, id)

    @staticmethod
    def add_city(session: Session, name: str, country_id: int) -> City:
        if session.get(Country, country_id) is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"no country with id {country_id}")

        city = City(name=name, fk_country_id=country_id)

        session.add(city)
        session.commit()

        return city

    @staticmethod
    def update_city(session: Session, city_id: int, data: CityNoIDSchema) -> City:
        city = session.get(City, city_id)

        if not city:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "city with this id not found")

        if not session.get(Country, data.fk_country_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"country with id {data.fk_country_id} not found")

        data.apply_to_city(city)

        session.add(city)
        session.commit()
        session.refresh(city)
        return city

    @staticmethod
    def delete_city(session: Session, city_id: int) -> bool:
        city: City | None = CitiesController.get_by_id(session, city_id)

        if not city:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "city with this id not found")

        try:
            cnt: int = session.exec(delete(City).where(City.city_id == city_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably city is used somewhere")
