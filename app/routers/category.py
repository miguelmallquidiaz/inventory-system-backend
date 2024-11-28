from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import category_crud
from app.schemas import category_schema, employee_schema

router = APIRouter()

@router.post("/", response_model=category_schema.Category, status_code=status.HTTP_201_CREATED)
async def create_category(category: category_schema.CategoryCreate, db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role != "almacen":
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    return category_crud.create_category(db=db, category=category)

@router.get("/", response_model=List[category_schema.Category])
async def read_categories(db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role not in ["local", "almacen"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    categories = category_crud.get_all_categories(db=db)
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron categorías"
        )
    return categories

@router.put("/{category_id}", response_model=category_schema.Category)
async def update_category(category_id: int, category: category_schema.CategoryUpdate, db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role != "almacen":
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    
    updated_category = category_crud.update_category(db=db, category_id=category_id, category=category)
    return updated_category
