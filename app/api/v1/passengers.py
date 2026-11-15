from app.models.passenger import Passenger
from app.schemas.passenger_schemas import PassengerNoIdSchema, PassengerDetailsSchema
from app.schemas.count_shema import CountSchema
from app.controllers.passengers_controller import PassengersController
from app.controllers.reservation_groups_controller import ReservationGroupsController
from app.utils.passengers import get_series_and_number_from_string
from app.db.session import get_session
from app.config import PAGE_LIMIT

from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlmodel import Session


def create_details_for_passenger(session: Session, passenger: Passenger) -> PassengerDetailsSchema:
    """
    creates PassengerDetailsSchema for Passanger model
    """
    return PassengerDetailsSchema(
        passenger_id=passenger.passenger_id,
        first_name=passenger.first_name,
        last_name=passenger.last_name,
        patronymic=passenger.patronymic,
        birth_date=passenger.birth_date,
        series=passenger.series,
        number=passenger.number,
        issuer=passenger.issuer,
        issurance_date=passenger.issurance_date,
        owned_groups=ReservationGroupsController.get_by_owner(session, passenger.passenger_id),
        member_of_groups=ReservationGroupsController.get_by_passenger_in_members(session, passenger.passenger_id)
    )


router = APIRouter(prefix="/passengers", tags=["Passengers"])


@router.get("", summary="get passengers paginated")
def get_passengers_paginated_route(offset: int = Query(default=0), limit: int = Query(default=0, le=PAGE_LIMIT), session: Session = Depends(get_session)) -> list[Passenger]:
    return PassengersController.get_paginated(session, offset, limit)

@router.get("/{id}", summary="get passenger by id")
def get_passenger_by_id_route(id: int, session: Session = Depends(get_session)) -> PassengerDetailsSchema:
    if passenger := PassengersController.get_by_id(session, id):
        return create_details_for_passenger(session, passenger)

    raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")

@router.get("/by_passport/{query}", summary="get passenger by passport series and number")
def get_passenger_by_passport_route(query: str, session: Session = Depends(get_session)) -> PassengerDetailsSchema:
    converted: tuple[int, int] | None = get_series_and_number_from_string(query)

    if converted is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "passport series and number format is not valid")

    series, number = converted
    passenger = PassengersController.get_by_series_and_number(session, series, number)

    if passenger is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")

    return create_details_for_passenger(session, passenger)

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
