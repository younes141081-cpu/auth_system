
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class UserRegister(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="3-50 characters: letters, numbers, _, . or -",
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=72,
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if value.isspace():
            raise ValueError("Password cannot contain only spaces.")
        return value


class UserLogin(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=72)
