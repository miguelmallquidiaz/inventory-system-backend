from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from ..schemas import reservation_schema

def create_reservation(db: Session, reservation_data: reservation_schema.ReservationCreate):
    db_reservation = models.Reservation(
        reservation_status="pending",
        payment_date=reservation_data.payment_date,
        delivery_date=reservation_data.delivery_date
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    # Crear los ítems de la reserva, con verificación de stock
    items = []
    for item in reservation_data.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_code).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con código {item.product_code} no encontrado"
            )
        reservation_item = models.ReservationItem(
            reservation_id=db_reservation.id,
            product_code=item.product_code,
            quantity=item.quantity
        )
        db.add(reservation_item)
        items.append(reservation_item)
    db.commit()
    # Responder con todos los datos necesarios
    return {
        "id": db_reservation.id,
        "status": db_reservation.reservation_status,
        "delivery_date": db_reservation.delivery_date,
        "items": [{
            "id": item.id,  # Agregar el id del item
            "reservation_id": item.reservation_id,  # Agregar el reservation_id
            "product_code": item.product_code,
            "quantity": item.quantity
        } for item in items]
    }


def get_reservations(db: Session):
    # Obtener todas las reservas con estado "pending" o "completed"
    reservations = db.query(models.Reservation).filter(
        models.Reservation.reservation_status.in_(["pendiente", "completado"])
    ).all()
    
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay reservas pendientes ni completadas")
    
    return reservations

def delete_reservation(db: Session, reservation_id: int):
    # Obtener la reserva por su ID
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")

    # Obtener y eliminar los ítems asociados a la reserva
    items = db.query(models.ReservationItem).filter(models.ReservationItem.reservation_id == reservation_id).all()
    for item in items:
        db.delete(item)  # Eliminar cada ítem

    # Eliminar la reserva
    db.delete(reservation)
    db.commit()  # Confirmar eliminación en la base de datos

    # Devolver información sobre la reserva eliminada y sus ítems
    return {
        "id": reservation.id,
        "delivery_date": reservation.delivery_date,
        "items": [{
            "id": item.id,
            "reservation_id": item.reservation_id,
            "product_code": item.product_code,
            "quantity": item.quantity
        } for item in items]
    }

def update_reservation(db: Session, reservation_id: int, update_data: reservation_schema.ReservationUpdate):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    
    if not db_reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    
    # Actualizar el estado de la reserva si se proporciona
    if update_data.reservation_status:
        if update_data.reservation_status not in ["pending", "completed"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado inválido para la reserva")
        db_reservation.reservation_status = update_data.reservation_status
    
    # Actualizar la fecha de entrega si se proporciona
    if update_data.delivery_date is not None:
        db_reservation.delivery_date = update_data.delivery_date
    
    db.commit()
    db.refresh(db_reservation)

    items = db.query(models.ReservationItem).filter(models.ReservationItem.reservation_id == reservation_id).all()

    return {
        "id": db_reservation.id,
        "reservation_status": db_reservation.reservation_status,
        "delivery_date": db_reservation.delivery_date,
        "items": [{"id": item.id, "reservation_id": item.reservation_id, "product_code": item.product_code, "quantity": item.quantity} for item in items]
    }

def get_reservation_by_id(db: Session, reservation_id: int):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    
    # Obtener los ítems de la reserva
    items = db.query(models.ReservationItem).filter(models.ReservationItem.reservation_id == reservation_id).all()
    
    return {
        "id": reservation.id,
        "reservation_status": reservation.reservation_status,
        "delivery_date": reservation.delivery_date,
        "items": [
            {
                "id": item.id,
                "reservation_id": item.reservation_id,
                "product_code": item.product_code,
                "quantity": item.quantity
            }
            for item in items
        ]
    }
