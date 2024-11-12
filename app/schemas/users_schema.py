from pydantic import BaseModel, EmailStr, field_validator
import re

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str

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
        if value not in ['admin', 'employee']:
            raise ValueError('El rol debe ser "admin" o "employee"')
        return value

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str