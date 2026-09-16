from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.crud.user import (
    authenticate_user,
    create_user,
    get_user_by_email,
)
from app.database.database import get_db
from app.schemas.user import Token, UserCreate, UserOut


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def registrar_usuario(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    user_db = get_user_by_email(
        db,
        email=user.email,
    )

    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )

    # El registro público siempre crea un cliente.
    user.role = "cliente"

    return create_user(
        db=db,
        user=user,
    )


@router.post(
    "/login",
    response_model=Token,
)
def iniciar_sesion(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }