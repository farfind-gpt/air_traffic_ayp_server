from sqlmodel import CheckConstraint, SQLModel, Field, Relationship, UniqueConstraint
from datetime import date


class PassportInfo(SQLModel, table=True):
    __tablename__ = "passport_info"
    entry_id: int = Field(default=None, primary_key=True)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    patronymic: str | None = Field(default=None)
    birth_date: date = Field(default=None)
    series: int = Field(default=None, ge=0, le=9999)
    number: int = Field(default=None, ge=0, le=999999)
    confirmed: bool = Field(default=False)

    __table_args__ = (
        UniqueConstraint("serial", "number"),
        CheckConstraint("series > 0 and series <= 9999"),
        CheckConstraint("number > 0 and number <= 999999")
    )

    user: "User" | None = Relationship(back_populates="passport_info")

    """
    returns passport's series and number as string.
    format: "SSSS-NNNNNN"
    """
    def get_id_string(self) -> str:
        return f"{self.series:04}-{self.number:06}"
