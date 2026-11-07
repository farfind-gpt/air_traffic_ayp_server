from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(default=None, primary_key=True)
    # deleted users and only them have None as email
    email: str | None = Field(default=None, unique=True)
    password_hash: str = Field(default=None)

    reservations: list["Reservation"] = Relationship(back_populates="user")
    owned_reservation_groups: list["ReservationGroup"] = Relationship(back_populates="owner")
    reservation_requests: list["ReservationRequest"] = Relationship(back_populates="user")
