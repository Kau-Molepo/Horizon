from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db import schemas
from db import crud
from database import get_db
from firebase.auth import *

user_router = APIRouter()

@user_router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User creation failed")
    return {"message": "Registration successful", "username": db_user.username, "registered": db_user.created_at}

@user_router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    
    db_user = crud.authenticate_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Login failed")
    
    # Create JWT token
    access_token = db_user.access_token
    
    return {"message": "Login successful", "user_id": db_user.user_id, "access_token": access_token, "token_type": "bearer", "role": db_user.role}

@user_router.get("/user", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.put("/update", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.delete("/delete", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = crud.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted"}

