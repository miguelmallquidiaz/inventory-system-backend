from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import date

class OrderBase(BaseModel):
    full_name: Optional[str] = None
    delivery_date: Optional[date] = None
    order_status: str

    @field_validator('order_status')
    def validate_status(cls, value: str) -> str:
        if value not in ['pendiente', 'completado']:
            raise ValueError('El estado del pedido debe ser uno de: pendiente y completado.')
        return value

class OrderCreate(OrderBase):
    order_details: List['OrderDetailCreate']

class OrderDetailCreate(BaseModel):
    product_code: int
    quantity: int

    @field_validator('quantity')
    def validate_quantity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError('La cantidad debe ser mayor a 0.')
        return value

class OrderUpdate(BaseModel):
    order_status: Optional[str] = None

    @field_validator('order_status')
    def validate_status(cls, value: str):
        if value is not None and value not in ['pendiente', 'completado']:
            raise ValueError('El estado del pedido debe ser uno de: pendiente y completado.')
        return value

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True

class OrderDetail(OrderDetailCreate):
    id: int
    product_name: str

    class Config:
        from_attributes = True
