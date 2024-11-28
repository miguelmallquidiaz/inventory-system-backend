from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, auth
from ..crud import employee_crud
from ..schemas import employee_schema

router = APIRouter()

def check_admin_permissions(current_user: employee_schema.Employee):
    if current_user.role != "almacen":
        raise HTTPException(status_code=403, detail="Permisos insuficientes")

@router.post("/", response_model=employee_schema.Employee, status_code=status.HTTP_201_CREATED)
async def create_user(employee: employee_schema.EmployeeCreate, db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    check_admin_permissions(current_user)
    if employee_crud.get_employee_by_email(db, email=employee.email):
        raise HTTPException(status_code=400, detail="Empleado ya registrado")
    return employee_crud.create_employee(db=db, employee=employee)