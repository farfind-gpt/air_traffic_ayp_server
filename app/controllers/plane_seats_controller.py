from app.models.plane_seat import PlaneSeat
from app.models.plane import Plane
from app.schemas.plane_schemas import *

from fastapi import HTTPException, status
from sqlmodel import Session, select


class PlaneSeatsController:

    @staticmethod
    def get_all_for_plane(session: Session, plane_id: int) -> list[PlaneSeat]:
        if session.get(Plane, plane_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"there is no plane with id {plane_id}")

        return list(session.exec(select(PlaneSeat).where(PlaneSeat.fk_plane_id == plane_id)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> PlaneSeat | None:
        return session.get(PlaneSeat, id)

    @staticmethod
    def add_plane_seat(session: Session, plane_id: int, number: int) -> PlaneSeat:
        if session.get(Plane, plane_id) is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"no plane with id {plane_id}")

        search_res = session.exec(select(PlaneSeat).where(PlaneSeat.fk_plane_id == plane_id and PlaneSeat.number == number)).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "plane seat with this number already exists in this plane")

        seat = PlaneSeat(fk_plane_id=plane_id, number=number)

        session.add(seat)
        session.commit()
        session.refresh(seat)

        return seat
