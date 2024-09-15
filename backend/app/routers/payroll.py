from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db import crud
from models import payroll as payroll_model
from database import get_db

router = APIRouter()

@router.post("/payroll", response_model=payroll_model.Payroll)
def create_payroll(payroll: payroll_model.PayrollCreate, db: Session = Depends(get_db)):
    return crud.create_payroll(db=db, payroll=payroll)

@router.get("/payrolls/{employee_id}")
def get_payrolls(employee_id: int, db: Session = Depends(get_db)):
    return crud.get_payrolls(db=db, employee_id=employee_id)
