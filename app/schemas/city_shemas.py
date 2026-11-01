from app.models.city import City

from pydantic import BaseModel, Field


class CityNoIDSchema(BaseModel):
    name: str = Field(default=None, examples=["London"])
    fk_country_id: int = Field(default=None, examples=[1])

    def apply_to_city(self, city: City):
        city.name = self.name
        city.fk_country_id = self.fk_country_id
