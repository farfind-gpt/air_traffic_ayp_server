from pydantic import BaseModel, Field


class TokensSchema(BaseModel):
    access_token: str = Field(description="JWT")
    refresh_token: str = Field(description="JWT")

class RefreshTokenSchema(BaseModel):
    refresh_token: str = Field(description="JWT")
