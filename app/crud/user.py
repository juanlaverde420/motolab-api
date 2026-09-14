from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session


def get_user_by_email(db: Session, email: str):
  return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
  hashed_pwd = hash_password(user.password)
  db_user = User(
      email=user.email, hashed_password=hashed_pwd, role=user.role
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


def authenticate_user(db: Session, email: str, password: str):
  user = get_user_by_email(db, email)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user