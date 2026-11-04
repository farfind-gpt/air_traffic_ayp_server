from app.models.countries import Country

from sqlmodel import SQLModel, Field, Relationship


class City(SQLModel, table=True):
    __tablename__ = "cities"
    city_id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    fk_country_id: int = Field(default=None, foreign_key="countries.country_id")

    country: Country = Relationship(back_populates="cities")
    airports: list["Airport"] = Relationship(back_populates="city")
