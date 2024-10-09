from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from typing import Optional

# Base class for Client
class ClientBase(BaseModel):
    name: str
    phone: str
    address: str
    email: EmailStr

# Schema for creating a Client
class ClientCreate(ClientBase):
    dni: str

    # Validators for DNI
    @field_validator('dni')
    def validate_dni(cls, value):
        if not re.match(r'^\d{8}$', value):
            raise ValueError('El DNI debe tener 8 dígitos.')
        return value

    # Validators for Name
    @field_validator('name')
    def validate_name(cls, value):
        value = value.strip()
        if len(value) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres.')
        if len(value) > 50:
            raise ValueError('El nombre no debe exceder los 50 caracteres.')
        return value

    # Validators for Phone
    @field_validator('phone')
    def validate_phone(cls, value):
        if not re.match(r'^\d{9}$', value):
            raise ValueError('El número de teléfono debe tener 9 dígitos.')
        return value

    # Validators for Address
    @field_validator('address')
    def validate_address(cls, value):
        value = value.strip()
        if len(value) > 100:
            raise ValueError('La dirección no debe exceder los 100 caracteres.')
        return value

# Schema for updating a Client
class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None

# Schema to retrieve a Client
class Client(ClientBase):
    dni: str

    class Config:
        from_attributes = True
