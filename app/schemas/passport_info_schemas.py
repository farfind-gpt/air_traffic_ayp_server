from app.models.passport_info import PassportInfo

from pydantic import BaseModel, Field

from datetime import date


class PassportInfoNoIDSchema(BaseModel):
    fk_user_id: int = Field(default=None, examples=[1])
    first_name: str = Field(default=None, examples=["Олег"])
    last_name: str = Field(default=None, examples=["Иванов"])
    patronymic: str | None = Field(default=None, examples=["Сергеевич"])
    birth_date: date = Field(default=None, examples=[date(2002, 2, 2)]) # TODO: will this example work??
    series: int = Field(default=None, ge=0, le=9999, examples=[4321])
    number: int = Field(default=None, ge=0, le=999999, examples=[654321])
    confirmed: bool = Field(default=False, examples=[False])

    def apply_to_passport_info(self, passport_info: PassportInfo):
        passport_info.fk_user_id = self.fk_user_id
        passport_info.first_name = self.first_name
        passport_info.last_name = self.last_name
        passport_info.patronymic = self.patronymic
        passport_info.birth_date = self.birth_date
        passport_info.series = self.series
        passport_info.number = self.number
        passport_info.confirmed = self.confirmed
