from typing import Optional
from pydantic import BaseModel, Field


class VehiculoBase(BaseModel):
  placa: str = Field(..., min_length=6, max_length=6)
  marca: str
  modelo: int
  propietario: str


class VehiculoCreate(VehiculoBase):
  pass


class VehiculoUpdate(BaseModel):
  marca: Optional[str] = None
  modelo: Optional[int] = None
  propietario: Optional[str] = None


class VehiculoOut(VehiculoBase):
  id: int
  user_id: Optional[int] = None

  class Config:
    from_attributes = True