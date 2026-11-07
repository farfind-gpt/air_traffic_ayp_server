from app.models.user import User

from pydantic import BaseModel, Field

from typing import Self


class UserRegisterSchema(BaseModel):
    email: str = Field(default=None, examples=["user@mail.net"])
    password: str = Field(default=None, examples=["securepassword123"])

class UserNoPasswordSchema(BaseModel):
    user_id: int = Field(default=None, examples=[143])
    email: str | None = Field(default=None, examples=["user@mail.net", None])

    @staticmethod
    def from_user(user: User) -> Self:
        return UserNoPasswordSchema(
            user_id=user.user_id,
            email=user.email
        )

class UserEmailSchema(BaseModel):
    email: str = Field(default=None, examples=["user@mail.net"])

class UserPasswordSchema(BaseModel):
    password: str = Field(default=None, examples=["securepassword123"])
