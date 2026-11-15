from app.models.reservation_group import ReservationGroup
from app.schemas.reservation_group_schemas import *
from app.schemas.count_shema import CountSchema
from app.controllers.reservation_groups_controller import ReservationGroupsController
from app.db.session import get_session
from app.config import PAGE_LIMIT

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session


router = APIRouter(prefix="/reservation_groups", tags=["Countries"])


@router.get("", summary="get reservation groups paginated")
def get_reservation_group_paginated_route(offset: int = Query(default=0), limit: int = Query(default=0, le=PAGE_LIMIT), session: Session = Depends(get_session)) -> list[ReservationGroup]:
    return ReservationGroupsController.get_paginated(session, offset, limit)

@router.get("/{id}", summary="get reservation group by id")
def get_reservation_group_by_id_route(id: int, session: Session = Depends(get_session)) -> ReservationGroup:
    group = ReservationGroupsController.get_by_id(session, id)

    if group is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return group

@router.get("/by_code/{code}", summary="get reservation group by code")
def get_reservation_group_by_code_route(code: str, session: Session = Depends(get_session)) -> ReservationGroup:
    group = ReservationGroupsController.get_by_code(session, code)

    if group is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return group

@router.put("/{id}", summary="update reservation group")
def update_reservation_group_route(id: int, data: ReservationGroupEditSchema, session: Session = Depends(get_session)) -> ReservationGroup:
    return ReservationGroupsController.update_reservation_group(session, id, data)

@router.post("", summary="add reservation group")
def add_reservation_group_route(data: ReservationGroupCreationSchema, session: Session = Depends(get_session)) -> ReservationGroup:
    return ReservationGroupsController.add_reservation_group(session, data.fk_owner_id)

@router.delete("/{id}", summary="delete reservation group by id")
def delete_reservation_group_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if ReservationGroupsController.delete_reservation_group(session, id) else 0))
