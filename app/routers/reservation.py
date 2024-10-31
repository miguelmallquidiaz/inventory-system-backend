from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import reservation_crud 
from app.schemas import reservation_schema, users_schema, reservation_item_schema

router = APIRouter()

# Crear una nueva reserva
@router.post("/", response_model=reservation_schema.Reservation)
async def create_reservation(reservation: reservation_schema.ReservationCreate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    return reservation_crud.create_reservation(db=db, reservation_data=reservation)

@router.delete("/{reservation_id}", response_model=reservation_schema.Reservation)
async def delete_reservation(
    reservation_id: int,
    db: Session = Depends(database.get_db),
    current_user: users_schema.User = Depends(auth.get_current_user)
):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    # Eliminar la reserva y sus ítems
    reservation = reservation_crud.delete_reservation(db, reservation_id)
    return reservation  # Aquí puedes retornar la reserva eliminada o un mensaje de éxito


@router.get("/{reservation_id}/items", response_model=List[reservation_schema.ReservationItem])
async def read_reservation_items(
    reservation_id: int,
    db: Session = Depends(database.get_db),
    current_user: users_schema.User = Depends(auth.get_current_user)
):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    items = reservation_crud.get_reservation_items(db, reservation_id)
    if not items:
        raise HTTPException(status_code=404, detail="No se encontraron ítems en la reserva")
    
    return items

@router.patch("/{reservation_id}", response_model=reservation_schema.Reservation)
async def update_reservation(
    reservation_id: int, 
    db: Session = Depends(database.get_db),
    current_user: users_schema.User = Depends(auth.get_current_user)  # Asegúrate de tener esta función
):
    # Verificar permisos del usuario
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")

    try:
        updated_reservation = reservation_crud.complete_reservation(db, reservation_id)
        return updated_reservation
    except HTTPException as e:  
        raise e  # Si se lanza una excepción, simplemente re-lanzamos

@router.get("/{client_dni}", response_model=List[reservation_schema.Reservation])
async def get_reservations_by_dni(
    client_dni: str,
    db: Session = Depends(database.get_db),
    current_user: users_schema.User = Depends(auth.get_current_user)
):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")

    return reservation_crud.get_reservations_by_dni(db=db, client_dni=client_dni)

@router.patch("/{reservation_id}/delivery_date", response_model=reservation_schema.Reservation)
async def update_reservation_delivery_date(
    reservation_id: int,
    delivery_date_data: reservation_schema.DeliveryDateUpdate,  # Esquema para la actualización de la fecha de entrega
    db: Session = Depends(database.get_db),
    current_user: users_schema.User = Depends(auth.get_current_user)
):
    # Verificar permisos del usuario
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")

    # Actualizar la fecha de entrega en la base de datos
    updated_reservation = reservation_crud.update_delivery_date(db, reservation_id, delivery_date_data)
    if not updated_reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    return updated_reservation

@router.get("/{reservation_id}/items", response_model=List[reservation_schema.ReservationItem])
async def read_reservation_items(
    reservation_id: int,
    db: Session = Depends(database.get_db),
    current_user: users_schema.User = Depends(auth.get_current_user)
):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    items = reservation_crud.get_reservation_items(db, reservation_id)
    if not items:
        raise HTTPException(status_code=404, detail="No se encontraron ítems en la reserva")
    
    return items