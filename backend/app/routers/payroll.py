from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import crud
from app.models import payroll as payroll_model
from app.db.database import get_db

router = APIRouter()

@router.post("/payroll", response_model=payroll_model.Payroll)
def create_payroll(payroll: payroll_model.PayrollCreate, db: Session = Depends(get_db)):
    return crud.create_payroll(db=db, payroll=payroll)

@router.get("/payrolls/{employee_id}")
def get_payrolls(employee_id: int, db: Session = Depends(get_db)):
    return crud.get_payrolls(db=db, employee_id=employee_id)
