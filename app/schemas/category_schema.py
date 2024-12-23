from pydantic import BaseModel, field_validator
import re
from typing import Optional

class CategoryBase(BaseModel):
    name: str

    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('El campo no debe ser vacío')
        if len(value) < 5:
            raise ValueError('El nombre debe tener al menos 5 caracteres')
        if len(value) > 30:
            raise ValueError('El nombre no debe exceder los 30 caracteres')
        if not re.match(r'^[a-záéíóúüñ\s]+$', value):
            raise ValueError('El nombre debe ser solo letras y minúsculas.')
        return value

class CategoryCreate(CategoryBase):
    @field_validator('name')
    def validate_name(cls, value):
        return CategoryBase.validate_name(value)

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('name')
    def validate_name(cls, value):
        if value is not None:
            return CategoryBase.validate_name(value)
        return value

class Category(CategoryBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
