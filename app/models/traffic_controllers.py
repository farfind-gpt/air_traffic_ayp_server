from sqlmodel import SQLModel, Field


class TrafficController(SQLModel, table=True):
    __tablename__ = "traffic_controllers"
    traffic_controller_id: int = Field(default=None, primary_key=True)
    password_hash: str = Field(default=None)
    real_id: str = Field(default=None)
