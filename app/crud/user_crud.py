from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import users_schema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def get_user_by_role(db: Session, role: str):
    user = db.query(models.User).filter(models.User.role == role).first()
    return user

def create_user(db: Session, user: users_schema.UserCreate):
    if user.role == "admin":
        existing_admin = get_user_by_role(db, role="admin")
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con el rol 'admin'."
            )

    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )
    
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        first_surname=user.first_surname,
        second_last_name=user.second_last_name,
        phone=user.phone,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user is None:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user