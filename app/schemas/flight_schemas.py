from app.models.flight import Flight
from app.schemas.plane_schemas import PlaneWithSeatsSchema

from pydantic import BaseModel, Field

from datetime import datetime


class FlightSeatInFlightSchema(BaseModel):
    fk_plane_seat_id: int = Field(examples=[43])
    price: int = Field(examples=[0, 400000])

class FlightCreationSchema(BaseModel):
    fk_plane_id: int = Field(examples=[4])
    flight_num: int = Field(ge=0, le=9999, examples=[67])
    fk_orig_airport_id: int = Field(examples=[30])
    fk_dest_airport_id: int = Field(examples=[39])
    fk_airline_id: int = Field(examples=[5])
    departure_datetime: datetime = Field(examples=[datetime(2021, 1, 1, 12, 30, 00)])
    planed_arrival_datetime: datetime = Field(examples=[datetime(2021, 1, 1, 14, 30, 00)])
    flight_seats: list[FlightSeatInFlightSchema] = Field()

    def to_model(self) -> Flight:
        """
        creates Flight model based on data from this objec
        """
        return Flight(
            flight_num=self.flight_num,
            fk_plane_id=self.fk_plane_id,
            fk_orig_airport_id=self.fk_orig_airport_id,
            fk_dest_airport_id=self.fk_dest_airport_id,
            fk_airline_id=self.fk_airline_id,
            departure_datetime=self.departure_datetime,
            planed_arrival_datetime=self.planed_arrival_datetime
        )

class FlightSeatInFlightDetailsSchema(BaseModel):
    fk_plane_seat_id: int = Field(examples=[43])
    price: int = Field(examples=[0, 400000])
    reservation_id: int | None = Field(examples=[934, None])
    reservation_group_code: str | None = Field(min_length=5, max_length=6, examples=["UIF77Q", "FJ33E", None])

class FlightDetailsSchema(BaseModel):
    flight_id: int = Field(examples=[33])
    plane: PlaneWithSeatsSchema = Field()
    flight_code: str = Field(max_length=7, min_length=7)
    fk_orig_airport_id: int = Field(examples=[30])
    fk_dest_airport_id: int = Field(examples=[39])
    departure_datetime: datetime = Field(examples=[datetime(2021, 1, 1, 12, 30, 00)])
    planed_arrival_datetime: datetime = Field(examples=[datetime(2021, 1, 1, 14, 30, 00)])
    flight_seats: list[FlightSeatInFlightSchema] = Field()

class FlightEditSchema(BaseModel):
    flight_num: int = Field(ge=0, le=9999, examples=[67])
    fk_orig_airport_id: int = Field(examples=[30])
    fk_dest_airport_id: int = Field(examples=[39])
    fk_airline_id: int = Field(examples=[5])
    departure_datetime: datetime = Field(examples=[datetime(2021, 1, 1, 12, 30, 00)])
    planed_arrival_datetime: datetime = Field(examples=[datetime(2021, 1, 1, 14, 30, 00)])

    def apply_to_model(self, flight: Flight):
        """
        sets Flight model fields to contain values from this object
        """
        flight.flight_num = self.flight_num
        flight.fk_orig_airport_id = self.fk_orig_airport_id
        flight.fk_dest_airport_id = self.fk_dest_airport_id
        flight.fk_airline_id = self.fk_airline_id
        flight.departure_datetime = self.departure_datetime
        flight.planed_arrival_datetime = self.planed_arrival_datetime
