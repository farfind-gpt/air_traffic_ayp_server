from app.models.passport_info import PassportInfo
from app.schemas.passport_info_schemas import PassportInfoNoIDSchema
from app.schemas.count_shema import CountSchema
from app.controllers.passport_info_controller import PassportInfoController
from app.db.session import get_session
from app.utils.passport_info import validate_seires_and_number_format

from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlmodel import Session


router = APIRouter(prefix="/passport_info", tags=["Passport info"])


@router.get("", summary="get passport info paginated")
def get_passport_info_paginated(limit: int = Query(default=0), offset: int = Query(default=0), session: Session = Depends(get_session)) -> list[PassportInfo]:
    return PassportInfoController.get_paginated(session, limit, offset)

@router.get("/{id}", summary="get passport info by id")
def get_passport_info_by_id_route(id: int, session: Session = Depends(get_session)) -> PassportInfo:
    passport_info = PassportInfoController.get_by_id(session, id)

    if passport_info is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return passport_info

@router.get("/by_series_and_number/{series_and_number}", summary="get passport info by series and number")
def get_passport_info_by_series_and_number_route(series_and_number: str, session: Session = Depends(get_session)) -> PassportInfo:
    if not validate_seires_and_number_format(series_and_number):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="invalid format (use SSSS-NNNNNN)")

    passport_info = PassportInfoController.get_by_series_and_number(session, int(splitted[0]), int(splitted[1]))

    if passport_info is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="not found")

    return passport_info

@router.get("/search", summary="search passport info by series and/or number")
def search_passport_info_route(series: int = Query(default=""), number: int = Query(default=""), session: Session = Depends(get_session)) -> list[PassportInfo]:
    return PassportInfoController.search(session, series, number)

@router.put("/{id}", summary="update passport info")
def update_passport_info_route(id: int, passport_info: PassportInfoNoIDSchema, session: Session = Depends(get_session)) -> PassportInfo:
    return PassportInfoController.update_passport_info(session, id, passport_info)

@router.post("", summary="add passport info")
def add_passport_info_route(passport_info: PassportInfoNoIDSchema, session: Session = Depends(get_session)) -> PassportInfo:
    return PassportInfoController.add_passport_info(session, passport_info)

@router.delete("/{id}", summary="delete passport info by id")
def delete_passport_info_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if PassportInfoController.delete_passport_info(session, id) else 0))
