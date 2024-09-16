from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import LeaveRequestCreate, LeaveRequestOut, LeaveRequestUpdate
from models import LeaveRequest
from database import get_db

leave_request_router = APIRouter()

@leave_request_router.post("/", response_model=LeaveRequestOut)
def create_leave_request(leave_request: LeaveRequestCreate, db: Session = Depends(get_db)):
    db_leave_request = LeaveRequest.create(leave_request, db)
    if not db_leave_request:
        raise HTTPException(status_code=400, detail="Leave Request creation failed")
    return db_leave_request

@leave_request_router.get("/{leave_id}", response_model=LeaveRequestOut)
def get_leave_request(leave_id: int, db: Session = Depends(get_db)):
    db_leave_request = LeaveRequest.get(leave_id, db)
    if not db_leave_request:
        raise HTTPException(status_code=404, detail="Leave Request not found")
    return db_leave_request

@leave_request_router.put("/{leave_id}", response_model=LeaveRequestOut)
def update_leave_request(leave_id: int, leave_request: LeaveRequestUpdate, db: Session = Depends(get_db)):
    db_leave_request = LeaveRequest.update(leave_id, leave_request, db)
    if not db_leave_request:
        raise HTTPException(status_code=404, detail="Leave Request not found")
    return db_leave_request

@leave_request_router.delete("/{leave_id}", response_model=dict)
def delete_leave_request(leave_id: int, db: Session = Depends(get_db)):
    result = LeaveRequest.delete(leave_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Leave Request not found")
    return {"status": "Leave Request deleted"}
