from typing import List
from app.core.config import ALGORITHM, SECRET_KEY
from app.crud import vehiculo as crud_vehiculo
from app.crud.user import get_user_by_email
from app.database.database import get_db
from app.models.user import User
from app.schemas.vehiculo import VehiculoCreate, VehiculoOut, VehiculoUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="No se pudieron validar las credenciales",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = get_user_by_email(db, email=email)
  if user is None:
    raise credentials_exception
  return user


@router.get("/", response_model=List[VehiculoOut])
def listar_vehiculos(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
  return crud_vehiculo.get_vehiculos(db, skip=skip, limit=limit)


@router.post(
    "/", response_model=VehiculoOut, status_code=status.HTTP_201_CREATED
)
def registrar_vehiculo(
    vehiculo: VehiculoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
  db_vehiculo = crud_vehiculo.get_vehiculo_by_placa(db, placa=vehiculo.placa)
  if db_vehiculo:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Un vehículo con esta placa ya está registrado",
    )
  return crud_vehiculo.create_vehiculo(
      db=db, vehiculo=vehiculo, user_id=current_user.id
  )


@router.put("/{vehiculo_id}", response_model=VehiculoOut)
def actualizar_vehiculo(
    vehiculo_id: int,
    vehiculo_update: VehiculoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
  vehiculo = crud_vehiculo.update_vehiculo(db, vehiculo_id, vehiculo_update)
  if not vehiculo:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Vehículo no encontrado",
    )
  return vehiculo


@router.delete("/{vehiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
  if current_user.role != "admin":
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos suficientes para realizar esta acción",
    )
  vehiculo = crud_vehiculo.delete_vehiculo(db, vehiculo_id)
  if not vehiculo:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Vehículo no encontrado",
    )
  return None