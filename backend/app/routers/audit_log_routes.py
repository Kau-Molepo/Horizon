from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import AuditLogCreate, AuditLogOut
from models import AuditLog
from database import get_db

audit_log_router = APIRouter()

@audit_log_router.post("/", response_model=AuditLogOut)
def create_audit_log(audit_log: AuditLogCreate, db: Session = Depends(get_db)):
    db_audit_log = AuditLog.create(audit_log, db)
    if not db_audit_log:
        raise HTTPException(status_code=400, detail="Audit Log creation failed")
    return db_audit_log

@audit_log_router.get("/{audit_id}", response_model=AuditLogOut)
def get_audit_log(audit_id: int, db: Session = Depends(get_db)):
    db_audit_log = AuditLog.get(audit_id, db)
    if not db_audit_log:
        raise HTTPException(status_code=404, detail="Audit Log not found")
    return db_audit_log
