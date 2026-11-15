from app.models.reservation_group import ReservationGroup

from pydantic import BaseModel, Field

from datetime import datetime


class ReservationGroupCreationSchema(BaseModel):
    fk_owner_id: int = Field(examples=[98])


class ReservationGroupEditSchema(BaseModel):
    reservation_group_code: str = Field(min_length=5, max_length=6, examples=["UIF77Q", "FJ33E"])
    fk_owner_id: int | None = Field(examples=[43, None])
    paid: bool = Field(examples=[False, True])

    def apply_to_model(self, reservation_group: ReservationGroup):
        """
        sets ReservationGroup model fields to contain values from this object
        """

        reservation_group.reservation_group_code = self.reservation_group_code
        reservation_group.fk_owner_id = self.fk_owner_id
        reservation_group.paid = self.paid
