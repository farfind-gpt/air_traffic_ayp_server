from sqlmodel import SQLModel, Field, ForeignKey, Relationship, UniqueConstraint


class PlaneSeat(SQLModel, table=True):
    __tablename__ = "plane_seats"
    seat_id: int = Field(default=None, primary_key=True)
    fk_plane_id: int = ForeignKey("planes.plane_id")
    number: int = Field(default=None)
    with_window: bool = Field(default=False)

    __table_args__ = (
        UniqueConstraint("fk_plane_id", "number")
    )

    plane: "Plane" = Relationship(back_populates="seats")
