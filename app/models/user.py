from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(default=None, primary_key=True)
    user_name: str = Field(default=None, unique=True)
    password_hash: str = Field(default=None)
    real_id: str = Field(default=None)
    is_admin: bool = Field(default=False)
