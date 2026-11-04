from pydantic import BaseModel, Field


class CountSchema(BaseModel):
    count: int = Field(default=None, examples=[0, 2, 99])
