from sqlmodel import SQLModel, Field, ForeignKey, Relationship
from countries import Country


class City(SQLModel, table=True):
    __tablename__ = "cities"
    city_id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    fk_country_id: int = ForeignKey("countries.country_id", default=None)

    country: Country = Relationship(back_populates="cities")
    airports: list["Airport"] = Relationship(back_populates="city")
