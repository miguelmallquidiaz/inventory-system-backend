from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import reservation_crud
from app.schemas import reservation_schema, users_schema

router = APIRouter()

# Crear una nueva reserva
@router.post("/", response_model=reservation_schema.Reservation)
async def create_reservation(reservation: reservation_schema.ReservationCreate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    return reservation_crud.create_reservation(db=db, reservation_data=reservation)

# Leer una reserva específica
@router.get("/{reservation_id}", response_model=reservation_schema.Reservation)
async def read_reservation(reservation_id: int, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    reservation = reservation_crud.get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reservation

# Actualizar una reserva
@router.patch("/{reservation_id}", response_model=reservation_schema.Reservation)
async def update_reservation(reservation_id: int, reservation: reservation_schema.ReservationUpdate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    return reservation_crud.update_reservation(db=db, reservation_id=reservation_id, reservation_data=reservation)

# Leer todas las reservas
@router.get("/", response_model=List[reservation_schema.Reservation])
async def read_reservations(db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    reservations = reservation_crud.get_all_reservations(db=db)
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron reservas"
        )
    return reservations

# Obtener todos los ítems de una reserva
@router.get("/{reservation_id}/items", response_model=List[reservation_schema.ReservationItem])
async def read_reservation_items(reservation_id: int, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")

    items = reservation_crud.get_reservation_items(db, reservation_id)
    if not items:
        raise HTTPException(status_code=404, detail="No se encontraron ítems en la reserva")
    return items
