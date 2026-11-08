from sqlmodel import CheckConstraint, SQLModel, Field, UniqueConstraint, Relationship
from datetime import date


class Passenger(SQLModel, table=True):
    __tablename__ = "passengers"
    passenger_id: int = Field(default=None, primary_key=True)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    patronymic: str | None = Field(default=None)
    birth_date: date = Field(default=None)
    series: int = Field(default=None, ge=0, le=9999)
    number: int = Field(default=None, ge=0, le=999999)
    issuer: str = Field(default=None)
    issurance_date: date = Field(default=None)

    __table_args__ = (
        UniqueConstraint("series", "number"),
        CheckConstraint("series > 0 and series <= 9999"),
        CheckConstraint("number > 0 and number <= 999999")
    )

    reservations: list["Reservation"] = Relationship(back_populates="passenger")
    reservation_groups_owned: list["ReservationGroup"] = Relationship(back_populates="owner")
