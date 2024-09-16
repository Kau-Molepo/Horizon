from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import UserCreate, UserOut, UserUpdate
from db import crud
from database import get_db

user_router = APIRouter()

@user_router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(user=user, db=db)
    if not db_user:
        raise HTTPException(status_code=400, detail="User creation failed")
    return db_user

@user_router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(user_id=user_id, user=user, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = crud.delete_user(user_id=user_id, db=db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted"}
