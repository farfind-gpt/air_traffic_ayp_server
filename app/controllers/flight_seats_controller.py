from app.models.flight_seat import FlightSeat
from app.models.plane_seat import PlaneSeat
from app.models.flight import Flight

from fastapi import HTTPException, status
from sqlmodel import Session, select


class FlightSeatsController:

    @staticmethod
    def get_all_for_flight(session: Session, flight_id: int) -> list[FlightSeat]:
        if session.get(Flight, flight_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"there is no flight with id {flight_id}")

        return list(session.exec(select(FlightSeat).where(FlightSeat.fk_flight_id == flight_id)))

    @staticmethod
    def get_by_id(session: Session, id: int) -> FlightSeat | None:
        return session.get(FlightSeat, id)

    @staticmethod
    def add_flight_seat(session: Session, plane_seat_id: int, flight_id: int, price: int) -> FlightSeat:
        if session.get(Flight, flight_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"there is no flight with id {flight_id}")

        if session.get(PlaneSeat, plane_seat_id) is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"no plane seat with id {plane_seat_id}")

        if price < 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "negative price not allowed")

        search_res = session.exec(
            select(PlaneSeat).where(
                FlightSeat.fk_plane_seat_id == plane_seat_id
                and
                FlightSeat.fk_flight_id == flight_id
            )
        ).first()

        if search_res:
            raise HTTPException(status.HTTP_409_CONFLICT, "entry for this plane seat already exists for this flight")

        flight_seat = FlightSeat(fk_flight_id=flight_id, fk_plane_seat_id=plane_seat_id, price=price)

        session.add(flight_seat)
        session.commit()
        session.refresh(flight_seat)

        return flight_seat

    @staticmethod
    def change_price(session: Session, id: int, price: int) -> FlightSeat:
        flight_seat = session.get(FlightSeat, id)

        if flight_seat is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "flight seat not found")

        if price < 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "negative price not allowed")

        flight_seat.price = price

        session.add(flight_seat)
        session.commit()
        session.refresh(flight_seat)
        return flight_seat
