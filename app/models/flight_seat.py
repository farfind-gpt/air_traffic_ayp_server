from app.models.plane_seat import PlaneSeat
from app.models.flight import Flight

from sqlmodel import SQLModel, Field, Relationship, PrimaryKeyConstraint, CheckConstraint


class FlightSeat(SQLModel, table=True):
    __tablename__ = "flight_seats"
    fk_plane_seat_id: int = Field(default=None, foreign_key="plane_seats.seat_id")
    fk_flight_id: int = Field(default=None, foreign_key="flights.flight_id")
    # if seat price is 0, you cannot reserve it
    price: int = Field(default=None)

    __table_args__ = (
        PrimaryKeyConstraint("fk_plane_seat_id", "fk_flight_id"),
        CheckConstraint("price >= 0")
    )

    plane_seat: PlaneSeat = Relationship(back_populates="flight_seats")
    flight: Flight = Relationship(back_populates="flight_seats")
