from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, auth
from app.crud import product_crud
from app.schemas import employee_schema, product_schema

router = APIRouter()

# Crear un producto
@router.post("/", response_model=product_schema.Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: product_schema.ProductCreate, db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role != "almacen":
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    return product_crud.create_product(db=db, product=product)

# Leer todos los productos
@router.get("/", response_model=List[product_schema.Product])
async def read_products(db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role not in ["almacen", "local"]:
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    products = product_crud.get_all_products(db=db)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron productos"
        )
    return products

@router.put("/{product_id}", response_model=product_schema.Product)
async def update_product(product_id: int, product: product_schema.ProductUpdate, db: Session = Depends(database.get_db), current_user: employee_schema.Employee = Depends(auth.get_current_user)):
    if current_user.role != "almacen":
        raise HTTPException(status_code=403, detail="No tienes suficientes permisos")
    return product_crud.update_product(db=db, product_id=product_id, product=product)