from app.core.config import JWK
from app.models.user import User

from typing import Literal, Self
from datetime import datetime, timedelta

from jose import jwt, JWTError
from pydantic import BaseModel, Field, ValidationError


class TokenInfo(BaseModel):
    user_id: int = Field()
    type: Literal["access", "refresh"] = Field()

    def __str__(self) -> str:
        """
        convert to JWT string

        tokens are issued during this convertion, for
        example when you do str(token_info), not on
        creation of TokenInfo object

        access tokens are valid within 2 days after
        issurance, refresh ones are valid within 5 days
        """

        now: datetime = datetime.now()

        data: dict = {
            "exp": now + timedelta(days=(2 if type == "access" else 5)),
            "iat": now,
            "type": self.type,
            "user_id": self.user_id
        }

        return jwt.encode(data, JWK, algorithm="HS256")

    @staticmethod
    def decode(token: str) -> Self | None:
        """
        decodes JWT string, returns TokenInfo or None on fail
        """

        try:
            data: dict = jwt.decode(token, JWK, algorithms=["HS256"])
        except JWTError:
            return None

        if any(k not in data.keys() for k in {"type", "user_id"}):
            return None

        try:
            return TokenInfo(
                type=data.get("type"),
                user_id=data.get("user_id")
            )
        except ValidationError:
            return None

    @staticmethod
    def create_for_user(user: User, type: Literal["access", "refresh"]) -> Self:
        """
        creates JWT based on User model

        raises TypeError if args have invalid types
        """

        if not isinstance(user, User):
            raise TypeError("user arg is not User model")

        if not isinstance(type, str) or type not in {"access", "refresh"}:
            raise TypeError("type must be string \"access\" or \"refresh\"")

        return TokenInfo(
            user_id=user.user_id,
            type=type
        )
