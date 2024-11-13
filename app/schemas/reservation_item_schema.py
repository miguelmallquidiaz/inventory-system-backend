from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Base class for ReservationItem
class ReservationItemBase(BaseModel):
    product_code: int
    quantity: int

    # Validators for Quantity
    @field_validator('quantity')
    def validate_quantity(cls, value):
        if value < 1:
            raise ValueError('La cantidad debe ser al menos 1.')
        return value

# Schema for creating a ReservationItem
class ReservationItemCreate(ReservationItemBase):
    pass

class ReservationItemList(ReservationItemBase):
    product_code: int
    quantity: int

# Schema for updating a ReservationItem
class ReservationItemUpdate(BaseModel):
    product_code: Optional[int] = None
    quantity: Optional[int] = None

# Schema to retrieve a ReservationItem
class ReservationItem(ReservationItemBase):
    id: int
    reservation_id: int

    class Config:
        from_attributes = True