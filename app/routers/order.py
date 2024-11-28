from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import order_crud
from app.schemas import employee_schema, order_schema
from ..models import Employee 

router = APIRouter()

@router.post("/", response_model=order_schema.Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: order_schema.OrderCreate, db: Session = Depends(database.get_db), current_user: Employee = Depends(auth.get_current_user)):
    if current_user.role not in ["local", "almacen"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    return order_crud.create_order(db=db, order=order, current_user=current_user)


# Leer un pedido por su ID
@router.get("/{order_id}", response_model=order_schema.Order)
async def read_order(order_id: int, db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role not in ["local", "almacen"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    order = order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order

# Listar todos los pedidos (con solo fecha y estado)
@router.get("/", response_model=List[order_schema.Order])
async def read_orders(db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role not in ["local", "almacen"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    orders = order_crud.get_orders(db=db)
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron pedidos"
        )
    return orders

# Leer los detalles de un pedido por su ID
@router.get("/{order_id}/details", response_model=List[order_schema.OrderDetail])
async def read_order_details(order_id: int, db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role not in ["local", "almacen"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    order_details = order_crud.get_order_details(db=db, order_id=order_id)
    if not order_details:
        raise HTTPException(status_code=404, detail="Detalles del pedido no encontrados")
    return order_details

# Actualizar el estado de un pedido
@router.patch("/{order_id}", response_model=order_schema.Order)
async def update_order_status(order_id: int, order: order_schema.OrderUpdate, db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role != "almacen":
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    updated_order = order_crud.update_order_status(db=db, order_id=order_id, order_update=order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return updated_order
