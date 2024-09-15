from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db import crud
from models import recruitment as recruitment_model
from database import get_db


router = APIRouter()

@router.post("/candidate", response_model=recruitment_model.Candidate)
def create_candidate(candidate: recruitment_model.CandidateCreate, db: Session = Depends(get_db)):
    return crud.create_candidate(db=db, candidate=candidate)

@router.get("/candidates")
def get_candidates(db: Session = Depends(get_db)):
    return crud.get_candidates(db=db)

@router.put("/candidates/{candidate_id}")
def update_candidate_status(candidate_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_candidate_status(db=db, candidate_id=candidate_id, status=status)
