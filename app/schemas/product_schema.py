from pydantic import BaseModel, field_validator
from typing import Optional
import re

class ProductBase(BaseModel):
    name: str
    total_stock: int
    is_active: bool = True

    @classmethod
    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('El nombre no debe estar vacío.')
        if len(value) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres.')
        if len(value) > 100:
            raise ValueError('El nombre no debe exceder los 100 caracteres.')
        if not re.match(r'^[a-záéíóúüñ\s]+$', value):
            raise ValueError('El nombre debe ser solo letras y minúsculas.')
        return value

    @classmethod
    @field_validator('total_stock')
    def validate_stock(cls, value: int) -> int:
        if value < 0:
            raise ValueError('El stock no puede ser negativo.')
        return value

class ProductCreate(ProductBase):
    subcategory_id: int

    @field_validator('name')
    def validate_name(cls, value):
        if value is not None:
            return ProductBase.validate_name(value)
        return value

    @field_validator('total_stock')
    def validate_stock(cls, value):
        if value is not None:
            return ProductBase.validate_stock(value)
        return value

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    total_stock: Optional[int] = None
    is_active: Optional[bool] = None
    subcategory_id: Optional[int] = None

    @field_validator('name')
    def validate_name(cls, value):
        if value is not None:
            return ProductBase.validate_name(value)
        return value

    @field_validator('total_stock')
    def validate_stock(cls, value):
        if value is not None:
            return ProductBase.validate_stock(value)
        return value

class Product(ProductBase):
    id: int
    subcategory_id: int

    class Config:
        from_attributes = True
