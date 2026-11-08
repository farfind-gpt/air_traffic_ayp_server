from app.models.passenger import Passenger

from sqlmodel import SQLModel, Field, Relationship, CheckConstraint

from datetime import datetime


class ReservationGroup(SQLModel, table=True):
    __tablename__ = "reservation_groups"
    reservation_group_id: int = Field(default=None, primary_key=True)
    reservation_group_code: str = Field(default=None, max_length=6)
    fk_owner_id: int = Field(default=None, foreign_key="passengers.passenger_id")
    created_at: datetime = Field(default=None)
    paid: bool = Field(default=False)

    __table_args__ = tuple(
        CheckConstraint("price > 0")
    )

    owner: Passenger = Relationship(back_populates="reservation_groups_owned")
    reservations: list["Reservation"] = Relationship(back_populates="reservation_group")
