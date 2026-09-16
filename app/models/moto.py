from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Moto(Base):
    __tablename__ = "motos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    placa = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    marca = Column(
        String,
        nullable=False,
    )

    modelo = Column(
        String,
        nullable=False,
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    owner = relationship(
        "User",
    )