from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, models
from models import user as user_model
from database import get_db
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register", response_model=user_model.UserResponse)
def register(user: user_model.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    db_user = crud.create_user(db, user)
    return db_user

@router.post("/login")
def login(user: user_model.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": db_user.email, "token_type": "bearer"}
