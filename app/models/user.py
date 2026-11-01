from app.models.passport_info import PassportInfo

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(default=None, primary_key=True)
    email: str = Field(default=None, unique=True)
    password_hash: str = Field(default=None)

    passport_info: PassportInfo | None = Relationship(back_populates="user")
    reservations: list["Reservation"] = Relationship(back_populates="user")
    owned_reservation_groups: list["ReservationGroup"] = Relationship(back_populates="user")
    reservation_requests: list["ReservationRequest"] = Relationship(back_populates="user")
