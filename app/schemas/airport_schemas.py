from app.models.airport import Airport

from pydantic import BaseModel, Field


class AirportNoIdSchema(BaseModel):
    name: str = Field(examples=["Koltsovo"])
    icao_index: str = Field(min_length=4, max_length=4, examples=["USSS"])
    fk_city_id: int = Field(examples=[4])

    """
    sets Airport model fields to contain values from this object
    """
    def apply_to_model(self, airport: Airport):
        airport.name = self.name
        airport.icao_index = self.icao_index
        airport.fk_city_id = self.fk_city_id

    """
    creates Airport model based on data from this objec
    """
    def to_airport(self) -> Airport:
        return Airport(
            name=self.name,
            icao_index=self.icao_index,
            fk_city_id=self.fk_city_id
        )
