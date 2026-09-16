from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers import moto_controller
from app.core.security import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.moto import MotoCreate, MotoOut


router = APIRouter(
    prefix="/motos",
    tags=["Motos"],
)


@router.get(
    "",
    response_model=List[MotoOut],
)
def list_motos(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return moto_controller.get_motos(
        db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{moto_id}",
    response_model=MotoOut,
)
def get_moto(
    moto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    moto = moto_controller.get_moto_by_id(
        db,
        moto_id,
    )

    if not moto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado",
        )

    return moto


@router.post(
    "",
    response_model=MotoOut,
    status_code=status.HTTP_201_CREATED,
)
def create_moto(
    moto: MotoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return moto_controller.create_moto(
        db,
        moto,
        current_user.id,
    )


@router.put(
    "/{moto_id}",
    response_model=MotoOut,
)
def update_moto(
    moto_id: int,
    moto: MotoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    moto_db = moto_controller.update_moto(
        db,
        moto_id,
        moto.model_dump(),
    )

    if not moto_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado",
        )

    return moto_db


@router.delete(
    "/{moto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_moto(
    moto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar vehículos",
        )

    success = moto_controller.delete_moto(
        db,
        moto_id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado",
        )