from sqlmodel import SQLModel, Field, Relationship, CheckConstraint

from datetime import datetime


class ReservationGroup(SQLModel, table=True):
    __tablename__ = "reservation_groups"
    reservation_group_id: int = Field(default=None, primary_key=True)
    reservation_group_code: str = Field(default=None, max_length=6)
    fk_owner_user_id: int = ForeignKey("users.user_id", default=None)
    created_at: datetime = Field(default=None)
    price: int = Field(default=None, gt=0)
    paid: bool = Field(default=False)

    __table_args__ = (
        CheckConstraint("price > 0")
    )

    owner: "User" = Relationship(back_populates="owned_reservation_groups")
    reservation_requests: list["ReservationRequest"] = Relationship(back_populates="reservation_group")
    reservations: list["Reservation"] = Relationship(back_populates="reservation_group")
