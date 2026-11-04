from app.models.user import User
from app.models.flight import Flight
from app.models.plane_seat import PlaneSeat
from app.models.reservation_group import ReservationGroup

from sqlmodel import SQLModel, Field, Relationship

from datetime import datetime


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"
    reservation_id: int = Field(default=None, primary_key=True)
    fk_flight_id: int = Field(default=None, foreign_key="flights.flight_id")
    fk_seat_id: int = Field(default=None, foreign_key="plane_seats.seat_id")
    reservation_time: datetime = Field(default=None)
    reserved_by_user: bool = Field(default=True)
    reservation_comment: str | None = Field(default=None)
    fk_user_id: int | None = Field(default=None, foreign_key="users.user_id")
    fk_reservation_group_id: int | None = Field(default=None, foreign_key="reservation_groups.reservation_group_id")

    flight: Flight = Relationship(back_populates="reservations")
    seat: PlaneSeat = Relationship()
    user: User | None = Relationship(back_populates="reservations")
    reservation_group: ReservationGroup | None = Relationship(back_populates="reservations")
