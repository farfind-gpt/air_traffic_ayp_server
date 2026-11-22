from app.api.v1.planes import create_plane_with_seats_schema_for_plane
from app.models.flight import Flight
from app.schemas.flight_schemas import *
from app.schemas.count_shema import CountSchema
from app.controllers.flight_seats_controller import FlightSeatsController
from app.controllers.flights_controller import FlightsController
from app.utils.flights import build_flight_code
from app.db.session import get_session
from app.core.config import PAGE_LIMIT

from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlmodel import Session

from datetime import date


def create_details_for_flight(session: Session, flight: Flight) -> FlightDetailsSchema:
    """
    creates FlightDetailsSchema for Flight model
    """

    code = build_flight_code(flight.airline.airline_code, flight.flight_num)

    if code is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal error")

    return FlightDetailsSchema(
        flight_id=flight.flight_id,
        plane=create_plane_with_seats_schema_for_plane(session, flight.plane),
        flight_code=code,
        fk_orig_airport_id=flight.fk_orig_airport_id,
        fk_dest_airport_id=flight.fk_dest_airport_id,
        departure_datetime=flight.departure_datetime,
        planed_arrival_datetime=flight.planed_arrival_datetime,
        flight_seats=[
            FlightSeatInFlightDetailsSchema(
                fk_plane_seat_id=flight_seat.fk_plane_seat_id,
                price=flight_seat.price,
                reservation_id=None,
                reservation_group_code=None
            )
            for flight_seat in
            FlightSeatsController.get_all_for_flight(session, flight.flight_id)
        ]
    )


router = APIRouter(prefix="/flights", tags=["Flights"])


@router.get("", summary="get flights paginated")
def get_flights_paginated_route(offset: int = Query(default=0), limit: int = Query(default=0, le=PAGE_LIMIT), session: Session = Depends(get_session)) -> list[Flight]:
    return FlightsController.get_paginated(session, offset, limit)

@router.get("/search", summary="search flights")
def search_flights_route(
    dest_airport_name: str = Query(default=""),
    orig_airport_name: str = Query(default=""),
    flight_code: str = Query(default=""),
    dest_airport_id: int | None = Query(default=None),
    orig_airport_id: int | None = Query(default=None),
    dest_city_id: int | None = Query(default=None),
    orig_city_id: int | None = Query(default=None),
    dest_country_id: int | None = Query(default=None),
    orig_country_id: int | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    offset: int = Query(default=0),
    limit: int = Query(default=0, le=PAGE_LIMIT),
    session: Session = Depends(get_session)
) -> list[Flight]:
    return FlightsController.search(
        dest_airport_name=dest_airport_name,
        orig_airport_name=orig_airport_name,
        flight_code=flight_code,
        dest_airport_id=dest_airport_id,
        orig_airport_id=orig_airport_id,
        dest_city_id=dest_city_id,
        orig_city_id=orig_city_id,
        dest_country_id=dest_country_id,
        orig_country_id=orig_country_id,
        date_from=date_from,
        date_to=date_to,
        offset=offset, limit=limit,
        session=session
    )

@router.get("/{id}", summary="get flight details by id")
def get_by_id_route(id: int, session: Session = Depends(get_session)) -> FlightDetailsSchema:
    flight = FlightsController.get_by_id(session, id)

    if flight is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "flight not found")

    return create_details_for_flight(session, flight)

@router.post("", summary="add flight")
def add_flight_route(data: FlightCreationSchema, session: Session = Depends(get_session)) -> Flight:
    return FlightsController.add_flight(session, data)

@router.put("/{id}", summary="update flight by id")
def update_flight_by_id(id: int, data: FlightEditSchema, session: Session = Depends(get_session)) -> FlightDetailsSchema:
    return create_details_for_flight(session, FlightsController.update_flight(session, id, data))

@router.delete("/{id}", summary="delete flight by id")
def delete_flight_by_id_route(id: int, session: Session = Depends(get_session)) -> CountSchema:
    return CountSchema(count=(1 if FlightsController.delete_flight(session, id) else 0))
