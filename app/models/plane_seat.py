from app.models.plane import Plane

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


class PlaneSeat(SQLModel, table=True):
    __tablename__ = "plane_seats"
    seat_id: int = Field(default=None, primary_key=True)
    fk_plane_id: int = Field(default=None, foreign_key="planes.plane_id", ondelete="CASCADE")
    number: int = Field(default=None)

    __table_args__ = tuple(
        UniqueConstraint("fk_plane_id", "number")
    )

    plane: Plane = Relationship(back_populates="seats")
    flight_seats: list["FlightSeat"] = Relationship(back_populates="plane_seat")
