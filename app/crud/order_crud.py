from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import HTTPException, status, Depends
from datetime import timedelta
from .. import models
from ..schemas import order_schema
from ..auth import get_current_user

# Function to get an Order by ID
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

# Function to create a new Order
def create_order(db: Session, order: order_schema.OrderCreate, current_user: models.Employee = Depends(get_current_user)):

    for detail in order.order_details:
        product = db.query(models.Product).filter(models.Product.id == detail.product_code).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Producto con código {detail.product_code} no encontrado")
    
    # Crear la orden
    delivery_date_plus_3 = order.delivery_date + timedelta(days=3)
    db_order = models.Order(delivery_date=delivery_date_plus_3, order_status='pendiente', employee_id=current_user.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for detail in order.order_details:
        db_order_detail = models.OrderDetail(
            order_id=db_order.id,
            product_code=detail.product_code,
            quantity=detail.quantity
        )
        db.add(db_order_detail)

    db.commit()
    return db_order


# Function to update an Order's status
def update_order_status(db: Session, order_id: int, order_update: order_schema.OrderUpdate):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")

    if order_update.order_status:
        db_order.order_status = order_update.order_status

    db.commit()
    db.refresh(db_order)
    return db_order

# Function to list orders with basic information (id, delivery_date, order_status)
def get_orders(db: Session):
    return (
        db.query(
            models.Order.id,
            models.Order.delivery_date,
            models.Order.order_status,
            func.concat(models.Employee.first_name, " ", models.Employee.last_name).label("full_name"),  # Concatenación
        )
        .join(models.Employee, models.Order.employee_id == models.Employee.id)
        .all()
    )

# Function to get all details of a specific order
def get_order_details(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")

    # Query for details of the order, include product details like name, etc.
    return db.query(
        models.OrderDetail.id, models.OrderDetail.product_code, models.OrderDetail.quantity,
        models.Product.name.label("product_name")
    ).join(models.Product).filter(models.OrderDetail.order_id == order_id).all()
