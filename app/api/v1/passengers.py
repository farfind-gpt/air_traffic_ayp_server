from app.models.passenger import Passenger
from app.schemas.passenger_schemas import PassengerNoIdSchema
from app.schemas.count_shema import CountSchema
from app.controllers.passengers_controller import PassengersController
from app.utils.passengers import get_series_and_number_from_string
from app.db.session import get_session
from app.config import PAGE_LIMIT

from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlmodel import Session


router = APIRouter(prefix="/passengers", tags=["Passengers"])


@router.get("", summary="get passengers paginated")
def get_passengers_paginated_route(offset: int = Query(default=0), limit: int = Query(default=0, le=PAGE_LIMIT), session: Session = Depends(get_session)) -> list[Passenger]:
    return PassengersController.get_paginated(session, offset, limit)

@router.get("/{id}", summary="get passenger by id")
def get_passenger_by_id_route(id: int, session: Session = Depends(get_session)) -> Passenger:
    if passenger := PassengersController.get_by_id(session, id):
        return passenger

    raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")

@router.get("/by_passport/{query}", summary="get passenger by passport series and number")
def get_passenger_by_passport_route(query: str, session: Session = Depends(get_session)) -> Passenger:
    converted: tuple[int, int] | None = get_series_and_number_from_string(query)

    if converted is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "passport series and number format is not valid")

    series, number = converted
    passenger = PassengersController.get_by_series_and_number(session, series, number)

    if passenger is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")

    return passenger

@router.get("/search/by_passport", summary="search passenger by passport series and number")
def search_passenger_by_passport_route(series: str = Query(default=""), number: str = Query(default=""), offset: int = Query(default=0), limit: int = Query(default=0, le=PAGE_LIMIT), session: Session = Depends(get_session)) -> list[Passenger]:
    return PassengersController.search_by_series_and_number(session, series, number, offset, limit)

@router.get("/search/by_name", summary="search passenger by first name, last name and patronymic")
def search_passenger_by_name(first_name: str = Query(default=""), last_name: str = Query(default=""), patronymic: str = Query(default=""), offset: int = Query(default=0), limit: int = Query(default=0, le=PAGE_LIMIT), session: Session = Depends(get_session)) -> list[Passenger]:
    return PassengersController.search_by_name(session, first_name, last_name, patronymic, offset, limit)

@router.put("/{id}", summary="update passenger")
def update_passenger_route(id: int, data: PassengerNoIdSchema, session: Session = Depends(get_session)) -> Passenger:
    return PassengersController.update_passenger(session, id, data)

@router.post("", summary="add passenger")
def add_passenger_route(data: PassengerNoIdSchema, session: Session = Depends(get_session)) -> Passenger:
    return PassengersController.add_passenger(session, data)

@router.delete("/{id}", summary="delete passenger by id")
def delete_passenger_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if PassengersController.delete_passenger(session, id) else 0))
