from app.models.city import City

from sqlmodel import SQLModel, Field, Relationship


class Airport(SQLModel, table=True):
    __tablename__ = "airports"
    airport_id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    icao_index: str = Field(min_length=4, max_length=4)
    fk_city_id: int = Field(default=None, foreign_key="cities.city_id")

    city: City = Relationship(back_populates="airports")
