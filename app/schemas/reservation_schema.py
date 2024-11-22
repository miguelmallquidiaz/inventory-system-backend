from typing import List, Optional
from datetime import date, timedelta
from pydantic import BaseModel, field_validator
from .reservation_item_schema import ReservationItemCreate, ReservationItem, ReservationItemUpdate

# Base class for Reservation
class ReservationBase(BaseModel):
    reservation_status: str = "pending"
    payment_date: Optional[date] = None  # Fecha de pago
    delivery_date: date  # Fecha de entrega

    # Validator for reservation_status
    @field_validator('reservation_status')
    def validate_reservation_status(cls, value):
        if value not in ["pending", "completed"]:
            raise ValueError('El estado debe ser "pending", "completed"')
        return value
    
    # Validator for delivery_date to ensure it's within 2 months from today

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