from sqlmodel import CheckConstraint, SQLModel, Field, Relationship, ForeignKey

from datetime import datetime


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"
    reservation_id: int = Field(default=None, primary_key=True)
    fk_flight_id: int = ForeignKey("flights.flight_id", default=None)
    fk_seat_id: int = ForeignKey("seats.seat_id", default=None)
    reservation_time: datetime = Field(default=None)
    reserved_by_user: bool = Field(default=True)
    reservation_comment: str | None = Field(default=None)
    fk_user_id: int | None = ForeignKey("users.user_id", default=None)
    fk_reservation_group_id: int | None = ForeignKey("reservation_groups.reservation_group_id", default=None)

    flight: "Flight" = Relationship(back_populates="reservations")
    seat: "Seat" = Relationship()
    user: "User" | None = Relationship(back_populates="reservations")
    reservation_group: "ReservationGroup" | None = Relationship(back_populates="reservations")
