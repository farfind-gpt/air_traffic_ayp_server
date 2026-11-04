from sqlmodel import SQLModel, Field, Relationship


class Country(SQLModel, table=True):
    __tablename__ = "countries"
    country_id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)

    cities: list["City"] = Relationship(back_populates="country")
