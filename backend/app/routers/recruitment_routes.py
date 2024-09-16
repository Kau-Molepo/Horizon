from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import RecruitmentCreate, RecruitmentOut, RecruitmentUpdate
from models import Recruitment
from database import get_db

recruitment_router = APIRouter()

@recruitment_router.post("/", response_model=RecruitmentOut)
def create_recruitment(recruitment: RecruitmentCreate, db: Session = Depends(get_db)):
    db_recruitment = Recruitment.create(recruitment, db)
    if not db_recruitment:
        raise HTTPException(status_code=400, detail="Recruitment creation failed")
    return db_recruitment

@recruitment_router.get("/{recruitment_id}", response_model=RecruitmentOut)
def get_recruitment(recruitment_id: int, db: Session = Depends(get_db)):
    db_recruitment = Recruitment.get(recruitment_id, db)
    if not db_recruitment:
        raise HTTPException(status_code=404, detail="Recruitment not found")
    return db_recruitment

@recruitment_router.put("/{recruitment_id}", response_model=RecruitmentOut)
def update_recruitment(recruitment_id: int, recruitment: RecruitmentUpdate, db: Session = Depends(get_db)):
    db_recruitment = Recruitment.update(recruitment_id, recruitment, db)
    if not db_recruitment:
        raise HTTPException(status_code=404, detail="Recruitment not found")
    return db_recruitment

@recruitment_router.delete("/{recruitment_id}", response_model=dict)
def delete_recruitment(recruitment_id: int, db: Session = Depends(get_db)):
    result = Recruitment.delete(recruitment_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Recruitment not found")
    return {"status": "Recruitment deleted"}
