from app.models.countries import Country

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError


class CountriesController:

    @staticmethod
    def get_all(session: Session) -> list[Country]:
        return list(session.exec(select(Country)).all())

    @staticmethod
    def get_by_id(session: Session, id: int) -> Country | None:
        return session.get(Country, id)

    @staticmethod
    def add_country(session: Session, name: str) -> Country:
        search_res = session.exec(select(Country).where(Country.name == name)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "country with this name already exists")

        new_country = Country(name=name)

        session.add(new_country)
        session.commit()
        session.refresh(new_country)
        return new_country

    @staticmethod
    def update_country(session: Session, country_id: int, name: str) -> Country:
        country = session.get(Country, country_id)

        if not country:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "country with this id not found")

        search_res = session.exec(select(Country).where(Country.name == name)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "country with this name already exists")

        country.name = name

        session.add(country)
        session.commit()
        session.refresh(country)
        return country

    @staticmethod
    def delete_country(session: Session, county_id: int) -> bool:
        country: Country | None = CountriesController.get_by_id(session, county_id)

        if not country:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "country with this id not found")

        try:
            cnt: int = session.exec(delete(Country).where(Country.country_id == county_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably country is used somewhere")
