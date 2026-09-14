from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
  email: EmailStr


class UserCreate(UserBase):
  password: str
  role: str = "cliente"


class UserOut(UserBase):
  id: int
  role: str

  class Config:
    from_attributes = True


class Token(BaseModel):
  access_token: str
  token_type: str