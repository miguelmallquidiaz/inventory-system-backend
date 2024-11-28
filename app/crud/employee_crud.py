from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import employee_schema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_employee_by_email(db: Session, email: str):
    employee = db.query(models.Employee).filter(models.Employee.email == email).first()
    return employee

def get_employee_by_role(db: Session, role: str):
    employee = db.query(models.Employee).filter(models.Employee.role == role).first()
    return employee

def create_employee(db: Session, employee: employee_schema.EmployeeCreate):
    if employee.role == "almacen":
        existing_admin = get_employee_by_role(db, role="almacen")
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un empleado con este rol."
            )

    existing_user = get_employee_by_email(db, email=employee.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )
    
    hashed_password = pwd_context.hash(employee.password)
    db_user = models.Employee(
        first_name = employee.first_name,
        last_name = employee.last_name,
        email = employee.email,
        hashed_password = hashed_password,
        role = employee.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_employee_by_email(db, email)
    if user is None:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user