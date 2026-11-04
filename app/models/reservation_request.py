from app.models.user import User
from app.models.reservation_group import ReservationGroup

from sqlmodel import SQLModel, Field, Relationship


class ReservationRequest(SQLModel, table=True):
    __tablename__ = "reservation_requests"
    reservation_request_id: int = Field(default=None, primary_key=True)
    fk_reservation_group_id: int = Field(default=None, foreign_key="reservation_groups.reservation_group_id")
    fk_user_id: int = Field(default=None, foreign_key="users.user_id")
    accepted: bool = Field(default=False)

    reservation_group: ReservationGroup = Relationship(back_populates="reservation_requests")
    user: User = Relationship(back_populates="reservation_requests")
