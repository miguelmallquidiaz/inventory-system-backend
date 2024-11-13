from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import reservation_crud 
from app.schemas import reservation_schema, users_schema

router = APIRouter()

# Verificar permisos del usuario (puedes usar un dependiente común)
def check_permissions(current_user: users_schema.User):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")

# Crear una nueva reserva
@router.post("/", response_model=reservation_schema.Reservation, status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation: reservation_schema.ReservationCreate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    check_permissions(current_user)
    return reservation_crud.create_reservation(db=db, reservation_data=reservation)

# Eliminar una reserva
@router.delete("/{reservation_id}", response_model=reservation_schema.Reservation)
async def delete_reservation(reservation_id: int, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    check_permissions(current_user)
    return reservation_crud.delete_reservation(db=db, reservation_id=reservation_id)

@router.get("/", response_model=List[reservation_schema.Reservation])
async def get_reservations(
    db: Session = Depends(database.get_db), 
    current_user: users_schema.User = Depends(auth.get_current_user)
):
    check_permissions(current_user)
    return reservation_crud.get_reservations(db=db)

@router.get("/{client_dni}", response_model=List[reservation_schema.Reservation])
async def get_reservations_by_dni(client_dni: str, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    check_permissions(current_user)
    return reservation_crud.get_reservations_by_dni(db=db, client_dni=client_dni)

@router.put("/{reservation_id}", response_model=reservation_schema.Reservation)
async def update_reservation(reservation_id: int, reservation_update: reservation_schema.ReservationUpdate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    check_permissions(current_user)
    return reservation_crud.update_reservation(db=db, reservation_id=reservation_id, update_data=reservation_update)

@router.get("/items/{reservation_id}", response_model=reservation_schema.Reservation)
async def get_reservation_by_id(
    reservation_id: int,
    db: Session = Depends(database.get_db),
    current_user: users_schema.User = Depends(auth.get_current_user)
):
    check_permissions(current_user)
    return reservation_crud.get_reservation_by_id(db=db, reservation_id=reservation_id)