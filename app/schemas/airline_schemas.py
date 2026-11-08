from pydantic import BaseModel, Field


class AirlineNoIdShema(BaseModel):
    airline_code: str = Field(examples=["SAL"])
    name: str = Field(examples=["Some Airlines"])
