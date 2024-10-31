from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from ..schemas import reservation_schema
from ..schemas.reservation_schema import DeliveryDateUpdate

def create_reservation(db: Session, reservation_data: reservation_schema.ReservationCreate):
    # Crear la reserva en la base de datos con estado inicial 'pending'
    db_reservation = models.Reservation(
        client_dni=reservation_data.client_dni,
        reservation_status="pending",
        payment_date=reservation_data.payment_date,
        delivery_date=reservation_data.delivery_date
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    # Variable para rastrear el estado final de la reserva
    all_items_in_stock = True
    items_created = []  # Lista para almacenar los ítems creados

    # Crear los ítems de la reserva
    for item in reservation_data.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_code).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con código {item.product_code} no encontrado"
            )

        # Verificar el stock del producto y ajustar pending_quantity
        if product.total_stock < item.quantity:
            pending_quantity = item.quantity - product.total_stock  # Calcular la cantidad pendiente
            product.total_stock = 0  # Agotar el stock
            all_items_in_stock = False
        else:
            pending_quantity = 0
            product.total_stock -= item.quantity  # Reducir el stock del producto

        db.commit()  # Hacer commit para asegurar que el stock se actualiza antes de crear el ítem

        # Crear ítem de reserva
        reservation_item = models.ReservationItem(
            reservation_id=db_reservation.id,
            product_code=item.product_code,
            quantity=item.quantity,
            pending_quantity=pending_quantity
        )
        db.add(reservation_item)
        items_created.append(reservation_item)  # Agregar ítem a la lista de ítems creados

    # Hacer commit para los ítems creados
    db.commit()

    # Actualizar el estado de la reserva
    db_reservation.reservation_status = "completed" if all_items_in_stock else "pending"
    db.commit()  # Commit para actualizar el estado de la reserva

    # Retornar la reserva con los ítems incluidos, pero solo los campos deseados
    return {
        "id": db_reservation.id,  # Incluir el ID de la reserva
        "client_dni": db_reservation.client_dni,
        "reservation_status": db_reservation.reservation_status,
        "payment_date": db_reservation.payment_date,
        "delivery_date": db_reservation.delivery_date,
        "items": [
            {
                "id": item.id,  # Incluir el ID del ítem de reserva
                "product_code": item.product_code,
                "quantity": item.quantity,
                "pending_quantity": item.pending_quantity,
                "reservation_id": item.reservation_id  # Incluir el reservation_id
            }
            for item in items_created  # Usar la lista de ítems creados
        ]
    }

def get_reservations_by_dni(db: Session, client_dni: str):
    reservations = db.query(models.Reservation).filter(models.Reservation.client_dni == client_dni).all()
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron reservas para este DNI")
    return reservations

def get_reservation(db: Session, reservation_id: int):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    return reservation

def update_reservation_status(db: Session, reservation_id: int, new_status: str):
    reservation = get_reservation(db, reservation_id)
    
    # Cambiar el estado de la reserva
    reservation.reservation_status = new_status
    
    # Si el nuevo estado es 'confirmed', establecer pending_quantity a 0 en los ítems
    if new_status == "confirmed":
        items = db.query(models.ReservationItem).filter(models.ReservationItem.reservation_id == reservation_id).all()
        for item in items:
            item.pending_quantity = 0  # Cambia la cantidad pendiente a 0
    
    db.commit()


def update_delivery_date(db: Session, reservation_id: int, update_data: DeliveryDateUpdate):
    reservation = get_reservation(db, reservation_id)  # Obtener la reserva por ID
    reservation.delivery_date = update_data.delivery_date  # Actualizar la fecha de entrega
    db.commit()  # Realizar el commit para guardar los cambios

def complete_reservation(db: Session, reservation_id: int):
    reservation = get_reservation(db, reservation_id)
    if reservation.reservation_status == "completed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La reserva ya está completada")

    items = db.query(models.ReservationItem).filter(models.ReservationItem.reservation_id == reservation_id).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron ítems para esta reserva")

    for item in items:
        item.pending_quantity = 0  # Cambia la cantidad pendiente a 0

    reservation.reservation_status = "completed"  # Cambia el estado a "completed"
    db.commit()

    # Retornar la reserva completada con todos los campos requeridos
    return {
        "id": reservation.id,
        "client_dni": reservation.client_dni,
        "reservation_status": reservation.reservation_status,
        "payment_date": reservation.payment_date,
        "delivery_date": reservation.delivery_date,
        "items": [
            {
                "id": item.id,
                "product_code": item.product_code,
                "quantity": item.quantity,
                "pending_quantity": item.pending_quantity,
                "reservation_id": item.reservation_id
            }
            for item in items
        ]
    }


def delete_reservation(db: Session, reservation_id: int):
    # Obtener la reserva por ID
    reservation = get_reservation(db, reservation_id)
    
    # Obtener los ítems de la reserva
    items = db.query(models.ReservationItem).filter(models.ReservationItem.reservation_id == reservation_id).all()
    
    # Eliminar cada ítem
    for item in items:
        db.delete(item)  # Elimina el ítem de la base de datos

    # Eliminar la reserva en sí
    db.delete(reservation)  
    db.commit()  # Realizar el commit para guardar los cambios
    
    return reservation  # Retorna la reserva eliminada

def get_reservation_items(db: Session, reservation_id: int):
    items = db.query(models.ReservationItem).filter(models.ReservationItem.reservation_id == reservation_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="No se encontraron ítems para esta reserva")
    return items