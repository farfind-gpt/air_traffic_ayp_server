from app.models.city import City

from sqlmodel import SQLModel, Field, ForeignKey, Relationship


class Airport(SQLModel, table=True):
    __tablename__ = "airports"
    airport_id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    fk_city_id: int = ForeignKey("cities.city_id", default=None)

    city: City = Relationship(back_populates="airports")
    route_points: list["RoutePoint"] = Relationship(back_populates="airports")
