from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import subcategory_crud
from app.schemas import subcategory_schema, users_schema

router = APIRouter()

# Crear una subcategoría
@router.post("/", response_model=subcategory_schema.Subcategory, status_code=status.HTTP_201_CREATED)
async def create_subcategory(subcategory: subcategory_schema.SubcategoryCreate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    return subcategory_crud.create_subcategory(db=db, subcategory=subcategory)

# Leer una subcategoría específica
@router.get("/{subcategory_id}", response_model=subcategory_schema.Subcategory)
async def read_subcategory(subcategory_id: int, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    subcategory = subcategory_crud.get_subcategory(db, subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    return subcategory

# Leer todas las subcategorías
@router.get("/", response_model=List[subcategory_schema.Subcategory])
async def read_subcategories(db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    subcategories = subcategory_crud.get_all_subcategories(db=db)
    if not subcategories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron subcategorías"
        )
    return subcategories

@router.put("/{subcategory_id}", response_model=subcategory_schema.Subcategory)
async def update_subcategory(subcategory_id: int, subcategory: subcategory_schema.SubcategoryUpdate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    updated_subcategory = subcategory_crud.update_subcategory(db=db, subcategory_id=subcategory_id, subcategory=subcategory)
    return updated_subcategory
