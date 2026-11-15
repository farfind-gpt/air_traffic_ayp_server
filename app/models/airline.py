from sqlmodel import SQLModel, Field, Relationship


class Airline(SQLModel, table=True):
    __tablename__ = "airlines"
    airline_id: int = Field(default=None, primary_key=True)
    # https://en.wikipedia.org/wiki/Airline_codes#ICAO_airline_designator
    airline_code: str = Field(default=None, max_length=3, min_length=3)
    name: str = Field(default=None, unique=True)

    flights: list["Flight"] = Relationship(back_populates="airline")
