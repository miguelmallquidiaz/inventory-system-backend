from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, field_validator
from .reservation_item_schema import ReservationItemCreate, ReservationItem, ReservationItemUpdate
import re
# Base class for Reservation
class ReservationBase(BaseModel):
    client_dni: str
    reservation_status: str
    payment_date: date  # Fecha de pago
    delivery_date: date  # Fecha de entrega

# Schema for creating a Reservation
class ReservationCreate(ReservationBase):
    items: List[ReservationItemCreate]

# Validator for DNI
    @field_validator('client_dni')
    def validate_dni(cls, value):
        # Valida que el DNI contenga exactamente 8 dígitos numéricos
        if not re.match(r'^\d{8}$', value):
            raise ValueError("El DNI debe tener exactamente 8 dígitos numéricos.")
        return value

    # Validators for Status
    @field_validator('reservation_status')
    def validate_status(cls, value):
        valid_statuses = ['pending', 'confirmed', 'cancelled']
        if value not in valid_statuses:
            raise ValueError(f"El estado debe ser uno de los siguientes: {', '.join(valid_statuses)}.")
        return value

# Schema for updating a Reservation
class ReservationUpdate(BaseModel):
    user_id: Optional[int] = None
    reservation_status: Optional[str] = None
    items: Optional[List[ReservationItemUpdate]] = None
    payment_date: Optional[date] = None  # Opcional, en caso se quiera actualizar
    delivery_date: Optional[date] = None  # Opcional, en caso se quiera actualizar

# Schema to retrieve a Reservation
class Reservation(ReservationBase):
    id: int
    items: List[ReservationItem]

    class Config:
        from_attributes = True
