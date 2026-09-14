from app.models.vehiculo import Vehiculo
from app.schemas.vehiculo import VehiculoCreate, VehiculoUpdate
from sqlalchemy.orm import Session


def get_vehiculo(db: Session, vehiculo_id: int):
  return db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()


def get_vehiculo_by_placa(db: Session, placa: str):
  return db.query(Vehiculo).filter(Vehiculo.placa == placa).first()


def get_vehiculos(db: Session, skip: int = 0, limit: int = 10):
  return db.query(Vehiculo).offset(skip).limit(limit).all()


def create_vehiculo(db: Session, vehiculo: VehiculoCreate, user_id: int = None):
  db_vehiculo = Vehiculo(**vehiculo.model_dump(), user_id=user_id)
  db.add(db_vehiculo)
  db.commit()
  db.refresh(db_vehiculo)
  return db_vehiculo


def update_vehiculo(
    db: Session, vehiculo_id: int, vehiculo_update: VehiculoUpdate
):
  db_vehiculo = get_vehiculo(db, vehiculo_id)
  if not db_vehiculo:
    return None

  update_data = vehiculo_update.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(db_vehiculo, key, value)

  db.commit()
  db.refresh(db_vehiculo)
  return db_vehiculo


def delete_vehiculo(db: Session, vehiculo_id: int):
  db_vehiculo = get_vehiculo(db, vehiculo_id)
  if not db_vehiculo:
    return None
  db.delete(db_vehiculo)
  db.commit()
  return db_vehiculo