from app.models.plane import Plane

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


class PlaneSeat(SQLModel, table=True):
    __tablename__ = "plane_seats"
    seat_id: int = Field(default=None, primary_key=True)
    fk_plane_id: int = Field(default=None, foreign_key="planes.plane_id")
    number: int = Field(default=None)
    with_window: bool = Field(default=False)

    __table_args__ = tuple(
        UniqueConstraint("fk_plane_id", "number")
    )

    plane: Plane = Relationship(back_populates="seats")
