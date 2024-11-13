from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from ..schemas import category_schema

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def create_category(db: Session, category: category_schema.CategoryCreate):
    existing_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría ya existe."
        )
    
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: category_schema.CategoryUpdate):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if category.name is not None:
        db_category.name = category.name
    if category.is_active is not None:
        db_category.is_active = category.is_active

    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_categories(db: Session):
    return db.query(models.Category).all()
