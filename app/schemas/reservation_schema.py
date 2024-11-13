from typing import List, Optional
from datetime import date, timedelta
from pydantic import BaseModel, field_validator
from .reservation_item_schema import ReservationItemCreate, ReservationItem, ReservationItemUpdate

# Base class for Reservation
class ReservationBase(BaseModel):
    client_dni: Optional[str] = None
    reservation_status: str = "pending"
    payment_date: Optional[date] = None  # Fecha de pago
    delivery_date: date  # Fecha de entrega

    # Validator for client_dni to ensure it's numeric and 8 digits long
    @field_validator('client_dni')
    def validate_client_dni(cls, value):
        if not value.isdigit() or len(value) != 8:
            raise ValueError("El DNI debe contener solo 8 dígitos numéricos.")
        return value
    
    # Validator for reservation_status
    @field_validator('reservation_status')
    def validate_reservation_status(cls, value):
        if value not in ["pending", "completed"]:
            raise ValueError('El estado debe ser "pending", "completed"')
        return value
    
    # Validator for delivery_date to ensure it's within 2 months from today
    @field_validator('delivery_date')
    def validate_delivery_date(cls, value):
        today = date.today()
        max_date = today + timedelta(weeks=1)
        if value < today:
            raise ValueError("La fecha de entrega no puede ser anterior a la fecha actual.")
        if value > max_date:
            raise ValueError("La fecha de entrega no puede exceder los 2 meses desde la fecha actual.")
        return value

# Schema for creating a Reservation
class ReservationCreate(ReservationBase):
    items: List[ReservationItemCreate]

# Schema to retrieve a Reservation
class Reservation(ReservationBase):
    id: int  # Asegúrate de que este campo esté presente
    items: List[ReservationItem]  # Aquí asegúrate de que ReservationItem incluya `id` y `reservation_id`

    class Config:
        from_attributes = True

class ReservationUpdate(ReservationBase):
    reservation_status: Optional[str] = None
    delivery_date: Optional[date] = None