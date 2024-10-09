from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re
# Base class for Product
class ProductBase(BaseModel):
    name: str
    total_stock: int
    unit_price: float
    is_active: bool = True

# Schema for creating a Product
class ProductCreate(ProductBase):
    subcategory_id: int

    # Validators for Name
    @field_validator('name')
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('El nombre no debe estar vacío.')
        if len(value) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres.')
        if len(value) > 100:
            raise ValueError('El nombre no debe exceder los 100 caracteres.')
        if not re.match(r'^[a-z\s]+$', value):
            raise ValueError('El nombre debe ser solo letras y minúsculas.')
        return value

    # Validators for Stock
    @field_validator('total_stock')
    def validate_stock(cls, value):
        if value < 0:
            raise ValueError('El stock no puede ser negativo.')
        return value
    
    # Validador para el Precio
    @field_validator('unit_price')
    def validate_unit_price(cls, value):
        if value < 0:
            raise ValueError('El precio no puede ser negativo.')
        return value

# Schema for updating a Product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    total_stock: Optional[int] = None
    unit_price: Optional[float] = None
    is_active: Optional[bool] = None

# Schema to retrieve a Product
class Product(ProductBase):
    code: int
    subcategory_id: int

    class Config:
        from_attributes = True