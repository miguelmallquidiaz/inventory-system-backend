from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

# Base class for Subcategory
class SubcategoryBase(BaseModel):
    name: str
    measures: str
    is_active: bool = True

# Schema for creating a Subcategory
class SubcategoryCreate(SubcategoryBase):
    name: str
    measures: str
    category_id: int

    # Validators for name
    @field_validator('name')
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('El campo no debe ser vacío')
        if len(value) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres')
        if len(value) > 50:
            raise ValueError('El nombre no debe exceder los 50 caracteres')
        if not re.match(r'^[a-z\s]+$', value):
            raise ValueError('El nombre debe ser solo letras y minúsculas.')
        return value

    # Validators for measures
    @field_validator('measures')
    def validate_measures(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('Las medidas no deben estar vacías')
        if len(value) > 100:
            raise ValueError('Las medidas no deben exceder los 100 caracteres')
        return value

# Schema for updating a Subcategory
class SubcategoryUpdate(BaseModel):
    name: Optional[str] = None
    measures: Optional[str] = None
    is_active: Optional[bool] = None

# Schema to retrieve a Subcategory
class Subcategory(SubcategoryBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True
