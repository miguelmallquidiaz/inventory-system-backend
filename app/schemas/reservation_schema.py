from typing import List, Optional
from datetime import date
from pydantic import BaseModel, field_validator
from .reservation_item_schema import ReservationItemCreate, ReservationItem, ReservationItemUpdate

# Base class for Reservation
class ReservationBase(BaseModel):
    client_dni: str
    reservation_status: str = "pending"  # Valor predeterminado
    payment_date: date  # Fecha de pago
    delivery_date: date  # Fecha de entrega

    # Validator for reservation_status
    @field_validator('reservation_status')
    def validate_reservation_status(cls, value):
        if value not in ["pending", "completed", "confirmed"]:
            raise ValueError('reservation_status must be either "pending", "completed", or "confirmed"')
        return value

# Schema for creating a Reservation
class ReservationCreate(ReservationBase):
    items: List[ReservationItemCreate]

# Schema for updating a Reservation
class ReservationUpdate(BaseModel):
    reservation_status: Optional[str] = None
    items: Optional[List[ReservationItemUpdate]] = None
    payment_date: Optional[date] = None  # Opcional, en caso se quiera actualizar
    delivery_date: Optional[date] = None  # Opcional, en caso se quiera actualizar

    # Validator for reservation_status
    @field_validator('reservation_status')
    def validate_update_reservation_status(cls, value):
        if value and value not in ["pending", "completed"]:
            raise ValueError('reservation_status must be either "pending" or "completed"')
        return value

    # Validator for payment_date and delivery_date
    @field_validator('payment_date', 'delivery_date', mode='after')
    def validate_dates(cls, value, values):
        if value is not None:
            if 'delivery_date' in values and value < values['delivery_date']:
                raise ValueError('La fecha de entrega no puede ser anterior a la fecha de pago.')
            if 'payment_date' in values and value < date.today():
                raise ValueError('La fecha de pago no puede ser en el pasado.')
        return value

class DeliveryDateUpdate(BaseModel):
    delivery_date: date  # Nueva fecha de entrega

# Schema to retrieve a Reservation
class Reservation(ReservationBase):
    id: int  # Asegúrate de que este campo esté presente
    items: List[ReservationItem]  # Aquí asegúrate de que ReservationItem incluya `id` y `reservation_id`

    class Config:
        from_attributes = True
