from sqlalchemy.orm import Session

from app.models.moto import Moto
from app.schemas.moto import MotoCreate


def get_motos(
    db: Session,
    skip: int = 0,
    limit: int = 10,
):
    return (
        db.query(Moto)
        .order_by(Moto.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_moto_by_id(
    db: Session,
    moto_id: int,
):
    return (
        db.query(Moto)
        .filter(Moto.id == moto_id)
        .first()
    )


def create_moto(
    db: Session,
    moto: MotoCreate,
    user_id: int,
):
    db_moto = Moto(
        **moto.model_dump(),
        owner_id=user_id,
    )

    db.add(db_moto)
    db.commit()
    db.refresh(db_moto)

    return db_moto


def update_moto(
    db: Session,
    moto_id: int,
    moto_data: dict,
):
    moto = get_moto_by_id(
        db,
        moto_id,
    )

    if not moto:
        return None

    for field, value in moto_data.items():
        setattr(
            moto,
            field,
            value,
        )

    db.commit()
    db.refresh(moto)

    return moto


def delete_moto(
    db: Session,
    moto_id: int,
):
    moto = get_moto_by_id(
        db,
        moto_id,
    )

    if not moto:
        return False

    db.delete(moto)
    db.commit()

    return True