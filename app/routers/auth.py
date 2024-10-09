from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import auth, database
from ..schemas import users_schema

router = APIRouter()

@router.post("/token", response_model=users_schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return auth.login_for_access_token(db, form_data)