from sqlmodel import CheckConstraint, SQLModel, Field, Relationship


class Plane(SQLModel, table=True):
    __tablename__ = "planes"
    plane_id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)

    __table_args__ = (
        CheckConstraint("default_seat_price > 0")
    )

    seats: list["PlaneSeat"] = Relationship(back_populates="plane")
    flights: list["Flight"] = Relationship(back_populates="plane")
