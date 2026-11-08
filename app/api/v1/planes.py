from app.models.plane import Plane
from app.schemas.plane_schemas import *
from app.schemas.count_shema import CountSchema
from app.controllers.planes_controller import PlanesController
from app.controllers.plane_seats_controller import PlaneSeatsController
from app.db.session import get_session
from app.api.rollback_on_exception import rollback_on_exception

from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlmodel import Session


router = APIRouter(prefix="/planes", tags=["Planes"])


@router.get("", summary="get all planes")
def get_all_planes_route(session: Session = Depends(get_session)) -> list[Plane]:
    return PlanesController.get_all(session)

@router.get("/{id}", summary="get plane by id")
def get_plane_by_id_route(id: int, no_seats: bool = Query(default=False), session: Session = Depends(get_session)) -> Plane | PlaneWithSeatsSchema:
    if no_seats:
        plane = PlanesController.get_by_id(session, id)

        if plane:
            return plane
    else:
        plane = PlanesController.get_by_id(session, id)

        if plane:
            seats = PlaneSeatsController.get_all_for_plane(session, id)

            return PlaneWithSeatsSchema(
                plane_id=plane.plane_id,
                name=plane.name,
                seats=[
                    PlaneSeatNoPlaneSchema.from_model(seat)
                    for seat in seats
                ]
            )

    raise HTTPException(status.HTTP_404_NOT_FOUND, "plane not found")

@router.put("/{id}", summary="update plane")
@rollback_on_exception
def update_plane_route(id: int, data: PlaneNoIdSchema, session: Session = Depends(get_session)) -> Plane:
    return PlanesController.update_plane(session, id, data.name)

@router.post("", summary="add plane")
@rollback_on_exception
def add_plane_route(data: PlaneWithSeatsNoIdSchema, session: Session = Depends(get_session)) -> PlaneWithSeatsSchema:
    plane = PlanesController.add_plane(session, data.name)

    seats: list[PlaneSeat] = []
    for seat in data.seats:
        seats.append(PlaneSeatsController.add_plane_seat(session, plane.plane_id, seat.number))

    return PlaneWithSeatsSchema(
        plane_id=plane.plane_id,
        name=plane.name,
        seats=[
            PlaneSeatNoPlaneSchema.from_model(seat)
            for seat in seats
        ]
    )

@router.delete("/{id}", summary="delete plane by id")
@rollback_on_exception
def delete_plane_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if PlanesController.delete_plane(session, id) else 0))
