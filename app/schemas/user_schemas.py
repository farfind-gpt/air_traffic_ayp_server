from app.models.user import User
from app.utils.passwords import hash as hash_password

from pydantic import BaseModel, Field

from typing import Self


class UserCreationSchema(BaseModel):
    user_name: str = Field(examples=["user12"])
    password: str = Field(examples=["rfj(jf0ekK0@$kf"])
    real_id: str = Field(examples=["station 4, emp. id 435"])
    is_admin: bool = Field(default=False)

    def to_model(self) -> User:
        """creates User model based on data from this object"""

        return User(
            user_name=self.user_name,
            real_id=self.real_id,
            password_hash=hash_password(self.password),
            is_admin=self.is_admin
        )

class UserChangePasswordSchema(BaseModel):
    old_password: str = Field(examples=["rfj(jf0ekK0@$kf"])
    new_password: str = Field(examples=["rfj(jf0ekK"])

class UserEditSchema(BaseModel):
    user_name: str = Field(examples=["user12"])
    real_id: str = Field(examples=["station 4, emp. id 435"])
    is_admin: bool = Field(default=False)

    def apply_to_model(self, user: User):
        """
        sets User model fields to contain values from this object
        """

        user.user_name = self.user_name
        user.real_id = self.real_id
        user.is_admin = self.is_admin

class UserNoPasswordSchema(BaseModel):
    user_id: int = Field(examples=[43])
    user_name: str = Field(examples=["user12"])
    real_id: str = Field(examples=["station 4, emp. id 435"])
    is_admin: bool = Field(default=False)

    @staticmethod
    def from_model(user: User) -> Self:
        """
        creates UserNoPasswordSchema object based on given User model
        """

        return UserNoPasswordSchema(
            user_id=user.user_id,
            user_name=user.user_name,
            real_id=user.real_id,
            is_admin=user.is_admin
        )
