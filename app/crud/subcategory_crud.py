from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from ..models import Category
from ..schemas import subcategory_schema

# Obtener subcategoría por ID
def get_subcategory(db: Session, subcategory_id: int):
    subcategory = db.query(models.Subcategory).filter(models.Subcategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategoría no encontrada")
    return subcategory

# Obtener subcategoría por nombre
def get_subcategory_by_name(db: Session, name: str):
    return db.query(models.Subcategory).filter(models.Subcategory.name == name).first()

# Crear una nueva subcategoría
def create_subcategory(db: Session, subcategory: subcategory_schema.SubcategoryCreate):
    existing_category = db.query(Category).filter(Category.id == subcategory.category_id).first()
    if not existing_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La categoría no existe."
        )

    existing_subcategory = db.query(models.Subcategory).filter(models.Subcategory.name == subcategory.name).first()
    if existing_subcategory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La subcategoría ya existe."
        )
    
    db_subcategory = models.Subcategory(
        name=subcategory.name,
        measures=subcategory.measures,
        is_active=subcategory.is_active,
        category_id=subcategory.category_id
    )
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

# Actualizar una subcategoría
def update_subcategory(db: Session, subcategory_id: int, subcategory: subcategory_schema.SubcategoryUpdate):
    db_subcategory = get_subcategory(db, subcategory_id)
    if not db_subcategory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategoría no encontrada")

    if subcategory.name is not None:
        db_subcategory.name = subcategory.name
    if subcategory.measures is not None:
        db_subcategory.measures = subcategory.measures
    if subcategory.is_active is not None:
        db_subcategory.is_active = subcategory.is_active
    if subcategory.category_id is not None:
        db_subcategory.category_id = subcategory.category_id

    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

# Deshabilitar una subcategoría
def disable_subcategory(db: Session, subcategory_id: int):
    return update_subcategory(db, subcategory_id, subcategory_schema.SubcategoryUpdate(is_active=False))

# Habilitar una subcategoría
def enable_subcategory(db: Session, subcategory_id: int):
    return update_subcategory(db, subcategory_id, subcategory_schema.SubcategoryUpdate(is_active=True))

# Obtener todas las subcategorías
def get_all_subcategories(db: Session):
    return db.query(models.Subcategory).all()
