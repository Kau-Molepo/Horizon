from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import crud
from app.models import user as user_model
from app.db.database import get_db

router = APIRouter()

@router.get("/user/{user_id}", response_model=user_model.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id=user_id)
