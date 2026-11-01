from pydantic import BaseModel, Field


class CountryNoIDShema(BaseModel):
    name: str = Field(default=None, examples=["Russia"])
