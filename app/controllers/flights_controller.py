from app.models.flight import Flight
from app.models.plane import Plane
from app.models.airport import Airport
from app.models.airline import Airline
from app.models.countries import Country
from app.models.city import City
from app.models.plane_seat import PlaneSeat
from app.schemas.flight_schemas import *
from app.utils.flights import parse_flight_code
from app.config import PAGE_LIMIT

from fastapi import HTTPException, status
from sqlmodel import Session, select, delete
from sqlalchemy.exc import IntegrityError

from datetime import date


class FlightsController:

    @staticmethod
    def get_paginated(session: Session, offset: int = 0, limit: int = 0) -> list[Flight]:
        if limit > PAGE_LIMIT:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"maximal limit is {PAGE_LIMIT}")

        return list(session.exec(select(Flight).offset(offset).limit(limit)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> Flight | None:
        return session.get(Flight, id)

    # TODO: PROBABLY TERRIBLE PERFORMANCE, SHOULD BE IMPROVED
    @staticmethod
    def search(
        session: Session,
        dest_airport_name: str,
        orig_airport_name: str,
        flight_code: str,
        dest_airport_id: int | None,
        orig_airport_id: int | None,
        dest_country_id: int | None,
        orig_country_id: int | None,
        dest_city_id: int | None,
        orig_city_id: int | None,
        date_from: date | None,
        date_to: date | None,
        offset: int = 0,
        limit: int = 0
    ) -> list[Flight]:
        if limit > PAGE_LIMIT:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"maximal limit is {PAGE_LIMIT}")

        query = select(Flight)

        if orig_airport_id is not None:
            query = query.where(Flight.fk_orig_airport_id == orig_airport_id)

        if dest_airport_id is not None:
            query = query.where(Flight.fk_dest_airport_id == dest_airport_id)

        if date_from is not None:
            query = query.where(Flight.departure_datetime > date_from and Flight.planed_arrival_datetime > date_from)

        if date_to is not None:
            query = query.where(Flight.departure_datetime < date_to and Flight.planed_arrival_datetime < date_to)

        flights: list[Flight] = list(session.exec(query).all())

        countries: dict[int, Country] = {c.country_id, c for c in session.exec(select(Country)).all()}
        citites: dict[int, City] = {c.city_id, c for c in session.exec(select(City)).all()}
        airports: dict[int, Airport] = {a.airport_id, a for a in session.exec(select(Airport)).all()}
        airlines: dict[int, Airline] = {a.airline_id, a for a in session.exec(select(Airline)).all()}

        to_exclude: list[Flight] = []
        def exclude():
            nonlocal to_exclude, flights

            for flight in to_exclude:
                flights.remove(flight)

            to_exclude.clear()

        if orig_airport_id is None:
            if orig_city_id is not None:
                for flight in flights:
                    if orig_city_id != citites[airports[flight.fk_orig_airport_id].fk_city_id].city_id:
                        to_exclude.append(flight)

                exclude()
            elif orig_country_id is not None:
                for flight in flights:
                    if orig_country_id != countries[citites[airports[flight.fk_orig_airport_id].fk_city_id].city_id].country_id:
                        to_exclude.append(flight)

                exclude()

            if orig_airport_name:
                for flight in flights:
                    if orig_airport_name not in airports[flight.fk_orig_airport_id].name:
                        to_exclude.append(flight)

                exclude()

        if dest_airport_id is None:
            if dest_city_id is not None:
                for flight in flights:
                    if dest_city_id != citites[airports[flight.fk_dest_airport_id].fk_city_id].city_id:
                        to_exclude.append(flight)

                exclude()
            elif dest_country_id is not None:
                for flight in flights:
                    if dest_country_id != countries[citites[airports[flight.fk_dest_airport_id].fk_city_id].city_id].country_id:
                        to_exclude.append(flight)

                exclude()

            if dest_airport_name:
                for flight in flights:
                    if dest_airport_name not in airports[flight.fk_dest_airport_id].name:
                        to_exclude.append(flight)

                exclude()

        if flight_code:
            for flight in flights:
                code = f"{airlines[flight.fk_airline_id].airline_code}-{flight.flight_num:04}"

                if flight_code not in code:
                    to_exclude.append(flight)

            exclude()

        return flights[offset:offset+limit]

    @staticmethod
    def add_flight(session: Session, data: FlightCreationSchema) -> Flight:
        if data.fk_orig_airport_id == data.fk_dest_airport_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "original and destination airports must have different IDs")

        if data.departure_datetime > data.planed_arrival_datetime:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "departure datetime should be earlier than arrival one")

        if session.get(Plane, data.fk_plane_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"plane with id {data.fk_plane_id} not found")

        for airport_id in [data.fk_orig_airport_id, data.fk_dest_airport_id]:
            if session.get(Airport, airport_id) is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"airport with id {airport_id} not found")

        if session.get(Airline, data.fk_airline_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"airline with id {data.fk_airline_id} not found")

        required_plane_seat_numbers: list[int] = []
        given_plane_seat_numbers: list[int] = []

        plane_seats: list[PlaneSeat] = list(session.exec(
                select(PlaneSeat).where(PlaneSeat.fk_plane_id == data.fk_plane_id
            )).all())

        required_plane_seat_numbers = [ps.number for ps in plane_seats]

        for flight_seat in data.flight_seats:
            number = None

            for plane_seat in plane_seats:
                if plane_seat.seat_id == flight_seat.fk_plane_seat_id:
                    number = plane_seat.number

            if number is None:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, f"invalid seat id {flight_seat.fk_plane_seat_id}")

            given_plane_seat_numbers.append(number)

        if len(given_plane_seat_numbers) != len(required_plane_seat_numbers):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "wrong amount of flight seats")

        if set(given_plane_seat_numbers) != set(required_plane_seat_numbers):
            # TODO: better error
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "wrong seat id(s)")

        flight = data.to_model()

        session.add(flight)
        session.commit()
        session.refresh(flight)
        return flight

    @staticmethod
    def update_flight(session: Session, id: int, data: FlightEditSchema) -> Flight:
        flight = session.get(Flight, id)

        if not flight:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "flight with this id not found")

        if flight.fk_orig_airport_id != data.fk_orig_airport_id or flight.fk_dest_airport_id != data.fk_dest_airport_id:
            if data.fk_orig_airport_id == data.fk_dest_airport_id:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "original and destination airports must have different IDs")

            if flight.fk_orig_airport_id != data.fk_orig_airport_id:
                if session.get(Airport, data.fk_orig_airport_id) is None:
                    raise HTTPException(status.HTTP_404_NOT_FOUND, f"airport with id {data.fk_orig_airport_id} not found")

            if flight.fk_dest_airport_id != data.fk_dest_airport_id:
                if session.get(Airport, data.fk_dest_airport_id) is None:
                    raise HTTPException(status.HTTP_404_NOT_FOUND, f"airport with id {data.fk_dest_airport_id} not found")

        if flight.fk_airline_id != data.fk_airline_id:
            if session.get(Airline, data.fk_airline_id) is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"airline with id {data.fk_airline_id} not found")

        if flight.departure_datetime != data.departure_datetime or flight.planed_arrival_datetime != data.planed_arrival_datetime:
            if data.departure_datetime > data.planed_arrival_datetime:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "departure datetime should be earlier than arrival one")

        data.apply_to_model(flight)

        session.add(flight)
        session.commit()
        session.refresh(flight)
        return flight

    @staticmethod
    def delete_flight(session: Session, flight_id: int) -> bool:
        flight: Flight | None = FlightsController.get_by_id(session, flight_id)

        if not flight:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "flight with this id not found")

        try:
            cnt: int = session.exec(delete(Flight).where(Flight.flight_id == flight_id)).rowcount
            session.commit()
            return cnt == 1
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "db integiry error, brobably flight is used somewhere")
