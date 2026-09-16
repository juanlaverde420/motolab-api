from pydantic import BaseModel, field_validator


class MotoCreate(BaseModel):
    placa: str
    marca: str
    modelo: str

    @field_validator("placa")
    @classmethod
    def validate_placa(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError(
                "La placa debe contener al menos 6 caracteres"
            )
        return v.upper()


class MotoUpdate(BaseModel):
    placa: str | None = None
    marca: str | None = None
    modelo: str | None = None

    @field_validator("placa")
    @classmethod
    def validate_placa(
        cls, v: str | None
    ) -> str | None:
        if v is not None:
            if len(v) < 6:
                raise ValueError(
                    "La placa debe contener al menos 6 caracteres"
                )
            return v.upper()
        return v


class MotoOut(BaseModel):
    id: int
    placa: str
    marca: str
    modelo: str
    owner_id: int

    class Config:
        from_attributes = True