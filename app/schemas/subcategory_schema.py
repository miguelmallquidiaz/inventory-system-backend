from pydantic import BaseModel, field_validator
from typing import Optional
import re

class SubcategoryBase(BaseModel):
    name: str
    measures: str
    is_active: bool = True

    @classmethod
    def check_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('El campo no debe ser vacío')
        if len(value) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres')
        if len(value) > 50:
            raise ValueError('El nombre no debe exceder los 50 caracteres')
        if not re.match(r'^[a-záéíóúüñ\s]+$', value):
            raise ValueError('El nombre debe ser solo letras y minúsculas.')
        return value

    @classmethod
    def check_measures(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('Las medidas no deben estar vacías')
        if len(value) > 100:
            raise ValueError('Las medidas no deben exceder los 100 caracteres')
        return value

class SubcategoryCreate(SubcategoryBase):
    category_id: int

    @field_validator('name')
    def validate_name(cls, value):
        return cls.check_name(value)
    @field_validator('measures')
    def validate_measures(cls, value):
        return cls.check_measures(value)

class SubcategoryUpdate(BaseModel):
    name: Optional[str] = None
    measures: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator('name')
    def validate_name(cls, value):
        if value is not None:
            return SubcategoryBase.check_name(value)
        return value

    @field_validator('measures')
    def validate_measures(cls, value):
        if value is not None:
            return SubcategoryBase.check_measures(value)
        return value

class Subcategory(SubcategoryBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True
