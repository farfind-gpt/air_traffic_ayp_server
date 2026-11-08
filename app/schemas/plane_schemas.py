from app.models.plane_seat import PlaneSeat

from pydantic import BaseModel, Field

from typing import Self


class PlaneSeatNoIdNoPlaneSchema(BaseModel):
    number: int = Field(examples=[33])

    """
    construct this object using data from PlaneSeat model
    """
    @staticmethod
    def from_model(model: PlaneSeat) -> Self:
        return PlaneSeatNoIdNoPlaneSchema(
            number=model.number
        )

class PlaneSeatNoPlaneSchema(BaseModel):
    seat_id: int = Field(examples=[332])
    number: int = Field(examples=[33])

    @staticmethod
    def from_model(model: PlaneSeat) -> Self:
        return PlaneSeatNoPlaneSchema(
            seat_id=model.seat_id,
            number=model.number
        )

class PlaneNoIdSchema(BaseModel):
    name: str = Field(examples=["Boeing 737-800"])

class PlaneWithSeatsNoIdSchema(BaseModel):
    name: str = Field(examples=["Boeing 737-800"])
    seats: list[PlaneSeatNoIdNoPlaneSchema] = Field()

class PlaneWithSeatsSchema(BaseModel):
    plane_id: int = Field(examples=[53])
    name: str = Field(examples=["Boeing 737-800"])
    seats: list[PlaneSeatNoPlaneSchema] = Field()
