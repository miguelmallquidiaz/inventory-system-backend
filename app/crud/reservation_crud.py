from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from ..schemas import reservation_schema

# Crear una nueva reserva con productos
def create_reservation(db: Session, reservation_data: reservation_schema.ReservationCreate):
    # Validar si el client_dni existe
    client = db.query(models.Client).filter(models.Client.dni == reservation_data.client_dni).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente no encontrado"
        )

    
    # Crear la reserva
    db_reservation = models.Reservation(
        client_dni=reservation_data.client_dni,
        reservation_status=reservation_data.reservation_status,
        payment_date=reservation_data.payment_date,
        delivery_date=reservation_data.delivery_date
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    # Crear los ítems de la reserva y reducir stock
    for item in reservation_data.items:
        product = db.query(models.Product).filter(models.Product.code == item.product_code).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con código {item.product_code} no encontrado"
            )
        if product.total_stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el producto {product.name}"
            )

        # Reducir el stock del producto
        product.total_stock -= item.quantity
        db.commit()

        # Crear ítem de reserva
        reservation_item = models.ReservationItem(
            reservation_id=db_reservation.id,
            product_code=item.product_code,
            quantity=item.quantity
        )
        db.add(reservation_item)
        db.commit()

    return db_reservation

# Obtener una reserva por ID
def get_reservation(db: Session, reservation_id: int):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    return reservation

# Actualizar una reserva
def update_reservation(db: Session, reservation_id: int, reservation_data: reservation_schema.ReservationUpdate):
    reservation = get_reservation(db, reservation_id)
    
    if reservation_data.reservation_status:
        reservation.reservation_status = reservation_data.reservation_status
    
    # Actualizar los ítems si es necesario (por simplicidad, no se actualizan ítems en este ejemplo)
    db.commit()
    db.refresh(reservation)
    return reservation

# Obtener todas las reservas
def get_all_reservations(db: Session):
    return db.query(models.Reservation).all()

# Obtener todos los ítems de una reserva
def get_reservation_items(db: Session, reservation_id: int):
    reservation_items = db.query(models.ReservationItem).filter(models.ReservationItem.reservation_id == reservation_id).all()
    if not reservation_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron ítems en la reserva"
        )
    return reservation_items
