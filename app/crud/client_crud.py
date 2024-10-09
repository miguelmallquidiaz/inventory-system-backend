from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from ..schemas import client_schema

# Obtener cliente por DNI
def get_client(db: Session, client_dni: str):
    client = db.query(models.Client).filter(models.Client.dni == client_dni).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return client

# Obtener cliente por nombre
def get_client_by_name(db: Session, name: str):
    return db.query(models.Client).filter(models.Client.name == name).first()

# Crear un nuevo cliente
def create_client(db: Session, client: client_schema.ClientCreate):
    existing_client = db.query(models.Client).filter(models.Client.dni == client.dni).first()
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El cliente ya existe."
        )

    db_client = models.Client(
        dni=client.dni,
        name=client.name,
        phone=client.phone,
        address=client.address,
        email=client.email
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Actualizar un cliente
def update_client(db: Session, client_dni: str, client: client_schema.ClientUpdate):
    db_client = get_client(db, client_dni)
    if not db_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

    if client.name is not None:
        db_client.name = client.name
    if client.phone is not None:
        db_client.phone = client.phone
    if client.address is not None:
        db_client.address = client.address
    if client.email is not None:
        db_client.email = client.email

    db.commit()
    db.refresh(db_client)
    return db_client

# Obtener todos los clientes
def get_all_clients(db: Session):
    return db.query(models.Client).all()