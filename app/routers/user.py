from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, auth, models
from ..crud import user_crud
from ..schemas import users_schema

router = APIRouter()

def check_admin_permissions(current_user: users_schema.User):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permisos insuficientes")

@router.post("/", response_model=users_schema.User)
async def create_user(user: users_schema.UserCreate, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    check_admin_permissions(current_user)
    if user_crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    return user_crud.create_user(db=db, user=user)

@router.get("/", response_model=list[users_schema.User])
async def list_users(db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    check_admin_permissions(current_user)
    users = db.query(models.User).all()
    return users

@router.delete("/delete/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: str, db: Session = Depends(database.get_db), current_user: users_schema.User = Depends(auth.get_current_user)):
    check_admin_permissions(current_user)
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"msg": f"Usuario eliminado exitosamente"}