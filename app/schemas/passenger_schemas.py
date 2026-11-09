from app.models.passenger import Passenger

from pydantic import BaseModel, Field

from datetime import date


class PassengerNoIdSchema(BaseModel):
    first_name: str = Field(examples=["Иван"])
    last_name: str = Field(examples=["Иванов"])
    patronymic: str | None = Field(default=None, examples=["Иванович", None])
    birth_date: date = Field(examples=[date(2002, 5, 20)])
    series: int = Field(ge=0, le=9999, examples=[1234])
    number: int = Field(ge=0, le=999999, examples=[123456])
    issuer: str = Field(examples=["Организация"])
    issurance_date: date = Field(examples=[date(2016, 6, 24)])

    """
    sets Passenger model fields to contain values from this object
    """
    def apply_to_model(self, passenger: Passenger):
        passenger.first_name = self.first_name
        passenger.last_name = self.last_name
        passenger.patronymic = self.patronymic
        passenger.birth_date = self.birth_date
        passenger.series = self.series
        passenger.number = self.number
        passenger.issuer = self.issuer
        passenger.issurance_date = self.issurance_date

    """
    creates Passenger model based on data from this objec
    """
    def to_model(self) -> Passenger:
        return Passenger(
            first_name=self.first_name,
            last_name=self.last_name,
            patronymic=self.patronymic,
            birth_date=self.birth_date,
            series=self.series,
            number=self.number,
            issuer=self.issuer,
            issurance_date=self.issurance_date,
        )
