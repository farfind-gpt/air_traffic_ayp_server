from pydantic import BaseModel, Field


class AirlineNoIdShema(BaseModel):
    airline_code: str = Field(max_length=3, min_length=3, examples=["SAL"])
    name: str = Field(examples=["Some Airlines"])
