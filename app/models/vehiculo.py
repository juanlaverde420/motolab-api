from app.database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Vehiculo(Base):
  __tablename__ = "vehiculos"

  id = Column(Integer, primary_key=True, index=True)
  placa = Column(String, unique=True, index=True, nullable=False)
  marca = Column(String, nullable=False)
  modelo = Column(Integer, nullable=False)
  propietario = Column(String, nullable=False)

  # Relación con el usuario creador/mecanico
  user_id = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User")