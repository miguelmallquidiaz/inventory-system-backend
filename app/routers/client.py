from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import client_crud
from app.schemas import client_schema, users_schema

router = APIRouter()

# Crear un cliente
@router.post("/", response_model=client_schema.Client)
async def create_client(client: client_schema.ClientCreate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    return client_crud.create_client(db=db, client=client)

# Actualizar un cliente
@router.patch("/{dni}", response_model=client_schema.Client)
async def update_client(dni: str, client: client_schema.ClientUpdate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    return client_crud.update_client(db=db, dni=dni, client=client)

# Leer un cliente específico
@router.get("/{dni}", response_model=client_schema.Client)
async def read_client(dni: str, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    client = client_crud.get_client(db, dni)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

# Leer todos los clientes
@router.get("/", response_model=List[client_schema.Client])
async def read_clients(db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    clients = client_crud.get_all_clients(db=db)
    if not clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron clientes"
        )
    return clients