from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db import crud
from models import user as user_model
from database import get_db


router = APIRouter()

@router.get("/user/{user_id}", response_model=user_model.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)
