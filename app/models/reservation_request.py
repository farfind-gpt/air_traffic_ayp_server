from app.models.user import User
from app.models.reservation_group import ReservationGroup

from sqlmodel import SQLModel, Field, Relationship, ForeignKey


class ReservationRequest(SQLModel, table=True):
    __tablename__ = "reservation_requests"
    reservation_request_id: int = Field(default=None, primary_key=True)
    fk_reservation_group_id: int = ForeignKey("reservation_groups.reservation_group_id", default=None)
    fk_user_id: int = ForeignKey("users.user_id", default=None)
    accepted: bool = Field(default=False)

    reservation_group: ReservationGroup = Relationship(back_populates="reservation_requests")
    user: User = Relationship(back_populates="reservation_requests")
