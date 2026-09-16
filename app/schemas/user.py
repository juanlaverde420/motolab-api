from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(
        min_length=6,
        max_length=100
    )

    role: Literal[
        "admin",
        "mecanico",
        "cliente"
    ] = "cliente"


class UserOut(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str