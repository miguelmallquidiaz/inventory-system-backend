from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from ..models import Subcategory
from ..schemas import product_schema

# Obtener producto por ID
def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product

# Obtener producto por nombre
def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()

# Crear un nuevo producto
def create_product(db: Session, product: product_schema.ProductCreate):
    existing_subcategory = db.query(Subcategory).filter(Subcategory.id == product.subcategory_id).first()
    if not existing_subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La subcategoría no existe."
        )
    
    existing_product = db.query(models.Product).filter(models.Product.name == product.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El producto ya existe."
        )
    
    db_product = models.Product(
        name=product.name,
        total_stock=product.total_stock,
        unit_price=product.unit_price,
        is_active=product.is_active,
        subcategory_id=product.subcategory_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Actualizar un producto
def update_product(db: Session, product_id: int, product: product_schema.ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    if product.name is not None:
        db_product.name = product.name
    if product.total_stock is not None:
        db_product.total_stock = product.total_stock  # Solo usar total_stock
    if product.unit_price is not None:  # Agregar validación para unit_price
        db_product.unit_price = product.unit_price
    if product.is_active is not None:
        db_product.is_active = product.is_active
    if product.subcategory_id is not None:
        db_product.subcategory_id = product.subcategory_id

    db.commit()
    db.refresh(db_product)
    return db_product

# Obtener todos los productos
def get_all_products(db: Session):
    return db.query(models.Product).all()
