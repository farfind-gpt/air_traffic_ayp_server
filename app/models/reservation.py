from app.models.passenger import Passenger
from app.models.flight import Flight
from app.models.plane_seat import PlaneSeat
from app.models.reservation_group import ReservationGroup

from sqlmodel import SQLModel, Field, Relationship, CheckConstraint

from datetime import datetime


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"
    reservation_id: int = Field(default=None, primary_key=True)
    fk_flight_id: int = Field(default=None, foreign_key="flights.flight_id")
    fk_passenger_id: int | None = Field(default=None, foreign_key="passengers.passenger_id", ondelete="SET NULL")
    fk_seat_id: int = Field(default=None, foreign_key="plane_seats.seat_id")
    reservation_time: datetime = Field(default=None)
    fk_reservation_group_id: int = Field(default=None, foreign_key="reservation_groups.reservation_group_id")
    price: int = Field(default=None)
    canceled: bool = Field(default=False)

    __table_args__ = tuple(
        CheckConstraint("price > 0")
    )

    flight: Flight = Relationship(back_populates="reservations")
    seat: PlaneSeat = Relationship()
    passenger: Passenger = Relationship(back_populates="reservations")
    reservation_group: ReservationGroup | None = Relationship(back_populates="reservations")
