from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import date

# Base schema for Order
class OrderBase(BaseModel):
    delivery_date: Optional[date] = None
    order_status: str

    @field_validator('order_status')
    def validate_status(cls, value: str) -> str:
        if value not in ['pendiente', 'completado']:
            raise ValueError('El estado del pedido debe ser uno de: pendiente y completado.')
        return value

# Schema for creating a new Order
class OrderCreate(OrderBase):
    order_details: List['OrderDetailCreate']  # List of order details (product_code and quantity)

# Schema for creating an order detail
class OrderDetailCreate(BaseModel):
    product_code: int  # The product's code (ID)
    quantity: int      # Quantity of the product

# Schema for updating an Order's status
class OrderUpdate(BaseModel):
    order_status: Optional[str] = None

    @field_validator('order_status')
    def validate_status(cls, value: str):
        if value is not None and value not in ['pendiente', 'completado']:
            raise ValueError('El estado del pedido debe ser uno de: pendiente y completado.')
        return value

# Schema to retrieve an Order with basic information
class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True

# Schema to retrieve Order details (including product name, quantity, etc.)
class OrderDetail(OrderDetailCreate):
    id: int
    product_name: str  # Assuming the product name is included from the product table

    class Config:
        from_attributes = True
