from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import PayrollCreate, PayrollOut, PayrollUpdate
from models import Payroll
from database import get_db

payroll_router = APIRouter()

@payroll_router.post("/", response_model=PayrollOut)
def create_payroll(payroll: PayrollCreate, db: Session = Depends(get_db)):
    db_payroll = Payroll.create(payroll, db)
    if not db_payroll:
        raise HTTPException(status_code=400, detail="Payroll creation failed")
    return db_payroll

@payroll_router.get("/{payroll_id}", response_model=PayrollOut)
def get_payroll(payroll_id: int, db: Session = Depends(get_db)):
    db_payroll = Payroll.get(payroll_id, db)
    if not db_payroll:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return db_payroll

@payroll_router.put("/{payroll_id}", response_model=PayrollOut)
def update_payroll(payroll_id: int, payroll: PayrollUpdate, db: Session = Depends(get_db)):
    db_payroll = Payroll.update(payroll_id, payroll, db)
    if not db_payroll:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return db_payroll

@payroll_router.delete("/{payroll_id}", response_model=dict)
def delete_payroll(payroll_id: int, db: Session = Depends(get_db)):
    result = Payroll.delete(payroll_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return {"status": "Payroll deleted"}
