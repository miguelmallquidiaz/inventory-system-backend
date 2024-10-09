from pydantic import BaseModel, EmailStr, field_validator
import re

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    name: str
    first_surname: str
    second_last_name: str
    phone: str
    role: str

    @field_validator('password')
    def check_password_length(cls, value):
        if '-' in value:
            raise ValueError('La contraseña no debe contener "-"')
        if len(value) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return value

    @field_validator('name','first_surname','second_last_name')
    def check_text_only(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('El campo no debe ser vacío')
        if not re.match(r'^[a-z\s]+$', value):
            raise ValueError('El campo solo debe contener letras')
        return value
    
    @field_validator('phone')
    def check_phone_format(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('El campo no debe ser vacío')
        if not (value.isdigit() and len(value) == 9 and value.startswith('9')):
            raise ValueError('El número de teléfono debe contener exactamente 9 dígitos numéricos y comenzar con 9')
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
    name: str
    first_surname: str
    second_last_name: str
    phone: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str