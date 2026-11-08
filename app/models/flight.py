from app.models.plane import Plane
from app.models.airline import Airline

from sqlmodel import CheckConstraint, SQLModel, Field, Relationship

from datetime import datetime


class Flight(SQLModel, table=True):
    __tablename__ = "flights"
    flight_id: int = Field(default=None, primary_key=True)
    fk_plane_id: int = Field(default=None, foreign_key="planes.plane_id")
    fk_orig_airport_id: int = Field(default=None, foreign_key="airports.airport_id")
    fk_dest_airport_id: int = Field(default=None, foreign_key="airports.airport_id")
    fk_airline_id: int = Field(default=None, foreign_key="airlines.airline_id")
    departure_datetime: datetime = Field(default=None)
    planed_arrival_datetime: datetime = Field(default=None)

    __table_args__ = tuple(
        CheckConstraint("seat_price > 0")
    )

    plane: Plane = Relationship(back_populates="flights")
    airline: Airline = Relationship(back_populates="flights")
    flight_seats: list["FlightSeat"] = Relationship(back_populates="flights")
    reservations: list["Reservation"] = Relationship(back_populates="flight")
