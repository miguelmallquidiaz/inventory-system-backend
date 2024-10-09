from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import category_crud
from app.schemas import category_schema, users_schema

router = APIRouter()

@router.post("/", response_model=category_schema.Category)
async def create_category(category: category_schema.CategoryCreate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return category_crud.create_category(db=db, category=category)

@router.patch("/disable/{category_id}", response_model=category_schema.Category)
async def disable_category(category_id: int, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return category_crud.disable_category(db=db, category_id=category_id)

@router.patch("/enable/{category_id}", response_model=category_schema.Category)
async def enable_category(category_id: int, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return category_crud.enable_category(db=db, category_id=category_id)

@router.get("/{category_id}", response_model=category_schema.Category)
async def read_category(category_id: int, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    category = category_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=List[category_schema.Category])
async def read_categories(db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "employee"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    categories = category_crud.get_all_categories(db=db)
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories found"
        )
    return categories