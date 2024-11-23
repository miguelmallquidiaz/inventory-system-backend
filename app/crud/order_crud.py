from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from .. import models
from ..schemas import order_schema

# Function to get an Order by ID
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

# Function to create a new Order
def create_order(db: Session, order: order_schema.OrderCreate):
    # Ensure all products exist in the order_details
    # (Check if product_code exists in the products table, optional depending on implementation)
    delivery_date_plus_3 = order.delivery_date + timedelta(days=3)

    db_order = models.Order(delivery_date=delivery_date_plus_3, order_status='pendiente')
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add the order details, including both product_code and quantity
    for detail in order.order_details:
        db_order_detail = models.OrderDetail(
            order_id=db_order.id,
            product_code=detail.product_code,
            quantity=detail.quantity  # Use the quantity provided in the order details
        )
        db.add(db_order_detail)

    db.commit()  # Commit all changes after adding order and details
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
    return db.query(models.Order.id, models.Order.delivery_date, models.Order.order_status).all()

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
