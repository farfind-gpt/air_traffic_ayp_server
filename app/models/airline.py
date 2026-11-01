from sqlmodel import SQLModel, Field, Relationship


class Airline(SQLModel, table=True):
    __tablename__ = "airlines"
    airline_id: int = Field(default=None, primary_key=True)
    airline_code: str = Field(default=None, max_length=3, unique=True)
    name: str = Field(default=None, unique=True)

    flights: list["Flight"] = Relationship(back_populates="airline")
