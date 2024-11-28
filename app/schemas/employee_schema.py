from pydantic import BaseModel, EmailStr, field_validator
import re

class EmployeeBase(BaseModel):
    email: EmailStr

class EmployeeCreate(EmployeeBase):
    first_name: str
    last_name: str
    password: str
    role: str

    @field_validator('first_name', 'last_name')
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('El nombre o apellido no debe estar vacío.')
        if len(value) > 50:
            raise ValueError('El nombre o apellido no debe exceder los 50 caracteres.')
        if not re.match(r'^[a-záéíóúüñ\s]+$', value):
            raise ValueError('El nombre o apellido debe ser solo letras y minúsculas.')
        return value
    @field_validator('password')
    def check_password_length(cls, value):
        if '-' in value:
            raise ValueError('La contraseña no debe contener "-"')
        if len(value) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return value
    @field_validator('role')
    def check_role(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('El campo no debe ser vacío')
        if value not in ['local', 'almacen']:
            raise ValueError('El rol debe ser local o almacen')
        return value

class Employee(EmployeeBase):
    id: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str