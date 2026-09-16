from typing import Optional

from pydantic import BaseModel, Field, field_validator


class VehiculoBase(BaseModel):
    placa: str = Field(
        min_length=6,
        max_length=6
    )

    marca: str = Field(
        min_length=1,
        max_length=50
    )

    modelo: int = Field(
        ge=1900,
        le=2100
    )

    propietario: str = Field(
        min_length=1,
        max_length=100
    )

    @field_validator("placa")
    @classmethod
    def validar_placa(cls, value: str):
        value = value.strip().upper()

        if len(value) != 6:
            raise ValueError(
                "La placa debe tener exactamente 6 caracteres"
            )

        return value

    @field_validator("marca", "propietario")
    @classmethod
    def validar_texto(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "Este campo no puede estar vacío"
            )

        return value


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoUpdate(BaseModel):
    marca: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    modelo: Optional[int] = Field(
        default=None,
        ge=1900,
        le=2100
    )

    propietario: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    @field_validator("marca", "propietario")
    @classmethod
    def validar_texto(cls, value):
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError(
                    "Este campo no puede estar vacío"
                )

            return value

        return value


class VehiculoOut(VehiculoBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True